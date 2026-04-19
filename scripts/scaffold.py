#!/usr/bin/env python3
"""Generate a BaseMock subclass from an OpenAPI spec URL or file."""

import argparse
import json
import re
import sys
import urllib.request


def load_spec(source: str) -> dict:
    if source.startswith("http"):
        with urllib.request.urlopen(source) as resp:
            return json.loads(resp.read())
    with open(source) as f:
        return json.load(f)


def to_class_name(name: str) -> str:
    return "".join(w.capitalize() for w in re.split(r"[-_.]", name)) + "Mock"


def to_method_name(method: str, path: str) -> str:
    parts = [p for p in path.strip("/").split("/") if not p.startswith("{")]
    slug = "_".join(parts[-2:]) if len(parts) > 1 else (parts[0] if parts else "root")
    slug = re.sub(r"[^a-z0-9_]", "_", slug.lower())
    return f"{method.lower()}_{slug}"


def generate_response(schema):
    """Generate a mock response string from an OpenAPI schema."""
    if not schema:
        return '{"ok": True}'
    example = schema.get("example")
    if example:
        return repr(example)
    props = schema.get("properties", {})
    if props:
        fields = {}
        for k, v in list(props.items())[:5]:
            if v.get("type") == "string":
                fields[k] = f"mock_{k}"
            elif v.get("type") == "integer":
                fields[k] = 0
            elif v.get("type") == "boolean":
                fields[k] = True
            else:
                fields[k] = f"mock_{k}"
        return repr(fields)
    return '{"ok": True}'


def scaffold(spec: dict, name: str, prefix: str) -> str:
    cls = to_class_name(name)
    base_url = ""
    servers = spec.get("servers", [])
    if servers:
        base_url = servers[0].get("url", "")

    routes = []
    paths = spec.get("paths", {})
    for path, ops in sorted(paths.items()):
        for method in ("get", "post", "put", "patch", "delete"):
            if method not in ops:
                continue
            op = ops[method]
            fn_name = to_method_name(method, path)
            resp_schema = None
            for code in ("200", "201", "default"):
                resp = op.get("responses", {}).get(code, {})
                content = resp.get("content", {}).get("application/json", {})
                resp_schema = content.get("schema")
                if resp_schema:
                    break
            status = 201 if method == "post" else 200
            body = generate_response(resp_schema)
            routes.append(
                f'    @route("{method.upper()}", "{path}")\n    async def {fn_name}(self, request, **kw):\n        return MockResponse(status={status}, body={body})'
            )
        if len(routes) >= 10:
            break

    routes_str = "\n\n".join(routes) if routes else "    pass"
    return f'''from mocks.base import BaseMock, route
from models import MockResponse


class {cls}(BaseMock):
    prefix = "{prefix}"
    spec_url = ""
    sandbox_base = "{base_url}"

{routes_str}
'''


def main():
    parser = argparse.ArgumentParser(description="Scaffold a BaseMock from an OpenAPI spec")
    parser.add_argument("--spec", required=True, help="OpenAPI spec URL or file path")
    parser.add_argument("--name", required=True, help="Integration name (e.g. stripe)")
    parser.add_argument("--prefix", default=None, help="URL prefix (default: /<name>)")
    parser.add_argument("--out", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    prefix = args.prefix or f"/{args.name}"
    spec = load_spec(args.spec)
    code = scaffold(spec, args.name, prefix)

    if args.out:
        with open(args.out, "w") as f:
            f.write(code)
        print(f"Wrote {args.out}")
    else:
        sys.stdout.write(code)


if __name__ == "__main__":
    main()
