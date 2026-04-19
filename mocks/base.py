from __future__ import annotations

import inspect
import re
from abc import ABC
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from models import Route


def route(method: str, path_pattern: str, writes: bool = True):
    def decorator(fn):
        fn._route_method = method.upper()
        fn._route_pattern = path_pattern
        fn._route_writes = writes
        return fn

    return decorator


def _favicon_from_source(cls: type) -> Optional[str]:
    try:
        path = Path(inspect.getfile(cls))
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "# FAVICON:" in line:
                url = line.split("# FAVICON:")[1].strip()
                if url.startswith("http"):
                    return url
                break
    except Exception:
        pass
    return None


class BaseMock(ABC):
    prefix: str = ""
    spec_url: str = ""
    sandbox_base: str = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._routes: list[Route] = []
        cls._favicon_url: Optional[str] = _favicon_from_source(cls)
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if callable(attr) and hasattr(attr, "_route_method"):
                cls._routes.append(
                    Route(
                        method=attr._route_method,
                        path_pattern=attr._route_pattern,
                        handler=name,
                        writes=getattr(attr, "_route_writes", True),
                    )
                )

    def match(self, method: str, path: str) -> Optional[Tuple[Route, dict]]:
        for r in self._routes:
            if r.method != method.upper():
                continue
            parts = re.split(r"(\{\w+\})", r.path_pattern)
            regex = "".join(
                re.escape(p) if not re.match(r"^\{\w+\}$", p) else f"(?P<{p[1:-1]}>[^/]+)"
                for p in parts
            )
            m = re.fullmatch(regex, path)
            if m:
                return r, m.groupdict()
        return None

    def registry_entry(self) -> dict:
        gets = [r for r in self._routes if r.method == "GET"]
        simple = next((r for r in gets if "{" not in r.path_pattern), None)
        preview = simple or (gets[0] if gets else None)
        favicon_url = getattr(self.__class__, "_favicon_url", None)
        favicon_domain = None
        if favicon_url:
            favicon_domain = urlparse(favicon_url).netloc.split(":")[0] or None
        if not favicon_domain and self.sandbox_base:
            favicon_domain = urlparse(self.sandbox_base).netloc.split(":")[0] or None
        return {
            "integration": self.prefix.strip("/"),
            "mock_base_url": f"https://verifiabl.dev{self.prefix}",
            "spec_url": self.spec_url,
            "writes": "paid-only",
            "preview_path": f"{self.prefix}{preview.path_pattern}" if preview else None,
            "favicon_url": favicon_url,
            "favicon_domain": favicon_domain,
        }
