from __future__ import annotations

import asyncio
import html
import importlib
import logging
import os
import pkgutil
import re
import secrets
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response

try:
    import asgi
    from workers import WorkerEntrypoint
except ImportError:  # pragma: no cover - local uvicorn path
    asgi = None
    WorkerEntrypoint = None

load_dotenv()

from auth import (  # noqa: E402
    AuthRejected,
    RateLimitRejected,
    check_magic_link_request,
    make_magic_token,
    resolve_request,
    validate_email,
    verify_magic_token,
)
from models import MockResponse, Tier  # noqa: E402
from mocks.base import BaseMock  # noqa: E402
from store import store  # noqa: E402

import mocks  # noqa: E402

for _info in pkgutil.iter_modules(mocks.__path__):
    importlib.import_module(f"mocks.{_info.name}")

_root = Path(__file__).parent
_SAFE_NAME = re.compile(r"^[a-z0-9_-]+$")
WRITE_NOTICE = "writes-not-persisted-upgrade-at-verifiabl.dev"
GITHUB_REPO = "https://github.com/verifiabldev/verifiabl"
ADD_INTEGRATION_DOC = f"{GITHUB_REPO}/blob/main/.cursor/skills/verifiabl-dev/ADD-INTEGRATION.md"
logger = logging.getLogger(__name__)
_ASSET_PATHS = {
    "/": "/dashboard/index.html",
    "/dashboard": "/dashboard/index.html",
    "/start": "/dashboard/index.html",
    "/privacy": "/dashboard/privacy.html",
    "/tos": "/dashboard/tos.html",
    "/learn": "/dashboard/learn/index.html",
    "/learn/": "/dashboard/learn/index.html",
    "/favicon.ico": "/logo.svg",
    "/logo.png": "/logo.svg",
    "/logo.svg": "/logo.svg",
    "/robots.txt": "/robots.txt",
    "/sitemap.xml": "/sitemap.xml",
}
_LEARN_SLUG = re.compile(r"^/learn/([a-z0-9_-]+)/?$")


def _env_value(request: Request | None, name: str, default: str = "") -> str:
    env = None
    if request is not None:
        env = (getattr(request, "scope", None) or {}).get("env")
    value = getattr(env, name, None) if env else None
    if value not in (None, ""):
        return value
    return os.environ.get(name, default)


def _public_base(request: Request | None = None) -> str:
    return (
        _env_value(request, "PUBLIC_BASE_URL", "https://verifiabl.dev") or "https://verifiabl.dev"
    ).rstrip("/")


def _enabled(value: str | None) -> bool:
    return str(value or "").strip().lower() not in {"", "0", "false", "no", "off"}


def _file_response(path: Path, media_type: str):
    if path.exists():
        return FileResponse(path, media_type=media_type)
    return Response(status_code=404)


def _asset_target(path: str) -> str | None:
    if path in _ASSET_PATHS:
        return _ASSET_PATHS[path]
    if path.startswith("/dashboard/"):
        return path
    learn_match = _LEARN_SLUG.match(path)
    if learn_match:
        return f"/dashboard/learn/{learn_match.group(1)}.html"
    return None


def _mocks():
    return [cls() for cls in BaseMock.__subclasses__()]


def _response_from_mock(resp: MockResponse) -> Response:
    if isinstance(getattr(resp, "body", None), bytes):
        out = Response(content=resp.body, media_type=resp.content_type, status_code=resp.status)
    elif resp.body is None:
        out = Response(status_code=resp.status, media_type=resp.content_type)
    else:
        out = JSONResponse(resp.body, status_code=resp.status)
    for header, value in (resp.headers or {}).items():
        out.headers[header] = value
    return out


def _auth_error_response(request: Request, exc: Exception, path: str) -> JSONResponse:
    if isinstance(exc, RateLimitRejected) and exc.scope == "anon":
        token = make_magic_token({"path": path}, request=request)
        return JSONResponse(
            {
                "error": exc.error,
                "message": exc.message,
                "upgrade_url": f"{_public_base(request)}/start?token={token}",
                "docs": f"{_public_base(request)}/#rate-limits",
            },
            status_code=exc.status,
        )
    if isinstance(exc, RateLimitRejected):
        return JSONResponse(
            {
                "error": exc.error,
                "message": exc.message,
                "docs": f"{_public_base(request)}/#rate-limits",
            },
            status_code=exc.status,
        )
    if isinstance(exc, AuthRejected):
        return JSONResponse({"error": exc.error, "message": exc.message}, status_code=exc.status)
    return JSONResponse(
        {"error": "auth_error", "message": "Authentication failed."}, status_code=401
    )


async def _notify_signup(request: Request, email: str):
    url = _env_value(request, "SLACK_SIGNUP_WEBHOOK")
    if not url:
        logger.warning("Signup Slack webhook is not configured.")
        return False
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"text": f"New signup: {email}"}, timeout=5)
        if response.status_code >= 400:
            logger.warning("Signup Slack webhook returned %s.", response.status_code)
            return False
        return True
    except Exception:
        logger.exception("Signup Slack webhook delivery failed.")
        return False


async def _existing_signup(email: str, request: Request, retries: int = 0):
    account = await store.find_account_by_email(email, request=request)
    if not account:
        return None
    credential = await store.find_active_credential(account["account_id"], request=request)
    while credential is None and retries > 0:
        await asyncio.sleep(0.05)
        credential = await store.find_active_credential(account["account_id"], request=request)
        retries -= 1
    if not credential:
        return None
    return credential["key"], account["account_id"], credential["tier"]


async def _send_magic_email(request: Request, email: str, link: str):
    api_key = _env_value(request, "RESEND_API_KEY")
    if not api_key:
        raise RuntimeError("Email delivery is not configured.")
    safe = html.escape(email)
    sender = _env_value(request, "RESEND_FROM_EMAIL", "verifiabl.dev <noreply@verifiabl.dev>")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "from": sender,
                "to": [email],
                "subject": "Your verifiabl.dev API key",
                "html": f'<p>Click to get your API key for {safe}:</p><p><a href="{link}">{link}</a></p>',
            },
            timeout=10,
        )
    if response.status_code >= 400:
        raise RuntimeError("Email delivery failed.")


async def _safe_json(request: Request):
    try:
        body = await request.json()
    except Exception:
        return None, JSONResponse({"error": "invalid_json"}, status_code=400)
    if not isinstance(body, dict):
        return None, JSONResponse({"error": "invalid_json"}, status_code=400)
    return body, None


@asynccontextmanager
async def lifespan(app: FastAPI):
    fixtures = _root / "fixtures"
    if fixtures.exists():
        store.load_fixtures(fixtures)
    test_key = os.environ.get("TEST_API_KEY")
    if test_key:
        await store.seed_test_account("test_dev", test_key, "test@verifiabl.dev")
    yield


app = FastAPI(title="verifiabl.dev", lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def root():
    return _file_response(_root / "dashboard" / "index.html", "text/html")


@app.get("/start", include_in_schema=False)
async def start():
    return _file_response(_root / "dashboard" / "index.html", "text/html")


@app.get("/dashboard", include_in_schema=False)
async def dashboard_index():
    return _file_response(_root / "dashboard" / "index.html", "text/html")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return _file_response(_root / "logo.svg", "image/svg+xml")


@app.get("/logo.svg", include_in_schema=False)
async def logo_svg():
    return _file_response(_root / "logo.svg", "image/svg+xml")


@app.get("/logo.png", include_in_schema=False)
async def logo_png():
    return RedirectResponse("/logo.svg", status_code=302)


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return _file_response(_root / "robots.txt", "text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return _file_response(_root / "sitemap.xml", "application/xml")


@app.get("/tos", include_in_schema=False)
async def tos():
    return _file_response(_root / "dashboard" / "tos.html", "text/html")


@app.get("/privacy", include_in_schema=False)
async def privacy():
    return _file_response(_root / "dashboard" / "privacy.html", "text/html")


@app.get("/learn", include_in_schema=False)
async def learn_index():
    return _file_response(_root / "dashboard" / "learn" / "index.html", "text/html")


@app.get("/learn/{slug}", include_in_schema=False)
async def learn_article(slug: str):
    if not _SAFE_NAME.fullmatch(slug):
        return Response(status_code=404)
    return _file_response(_root / "dashboard" / "learn" / f"{slug}.html", "text/html")


@app.get("/healthz")
async def healthz(request: Request):
    strict = _enabled(_env_value(request, "STRICT_HEALTH_CHECKS"))
    secret = _env_value(request, "SECRET_KEY")
    slack_webhook = _env_value(request, "SLACK_SIGNUP_WEBHOOK")
    status = "ok"
    checks = {"config": "ok", "signup_webhook": "ok" if slack_webhook else "missing"}
    if strict and secret in {"", "dev-secret", "change-me-in-production"}:
        status = "error"
        checks["config"] = "invalid_secret"
    if strict and not slack_webhook:
        status = "error"
    return JSONResponse(
        {"status": status, "checks": checks}, status_code=200 if status == "ok" else 500
    )


@app.get("/registry")
async def registry(request: Request):
    public_base = _public_base(request)
    items = []
    for mock in _mocks():
        item = mock.registry_entry()
        item["mock_base_url"] = f"{public_base}{mock.prefix}"
        items.append(item)
    return items


@app.post("/auth/magic")
async def auth_magic(request: Request):
    body, err = await _safe_json(request)
    if err:
        return err
    email = validate_email(body.get("email", ""))
    if not email:
        return JSONResponse({"error": "invalid_email"}, status_code=400)
    try:
        await check_magic_link_request(request)
        token = make_magic_token({"email": email}, request=request)
        link = f"{_public_base(request)}/auth/verify?token={token}"
        await _send_magic_email(request, email, link)
    except RateLimitRejected as exc:
        return _auth_error_response(request, exc, "auth/magic")
    except RuntimeError as exc:
        return JSONResponse({"error": "email_send_failed", "message": str(exc)}, status_code=503)
    return {"status": "sent"}


@app.post("/auth/exchange")
async def auth_exchange(request: Request):
    body, err = await _safe_json(request)
    if err:
        return err
    code = body.get("code", "")
    data = await store.consume_exchange_code(code, request=request)
    if not data or "api_key" not in data:
        return JSONResponse({"error": "invalid_code"}, status_code=401)
    return {"api_key": data["api_key"], "account_id": data["account_id"], "tier": data["tier"]}


@app.get("/auth/verify")
async def auth_verify(token: str, request: Request):
    data = verify_magic_token(token, request=request)
    if not data:
        return JSONResponse({"error": "invalid_token"}, status_code=401)
    email = data["email"]
    key = acct_id = tier_val = None
    existing = await _existing_signup(email, request)
    if existing:
        key, acct_id, tier_val = existing
    if key is None:
        acct_id = secrets.token_hex(8)
        key = f"vrf_free_{secrets.token_hex(12)}"
        tier_val = Tier.FREE.value
        try:
            await store.save_account_and_credential(acct_id, email, key, tier_val, request=request)
        except Exception:
            existing = await _existing_signup(email, request, retries=3)
            if not existing:
                raise
            key, acct_id, tier_val = existing
        else:
            await _notify_signup(request, email)
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        exchange_code = secrets.token_urlsafe(24)
        await store.store_exchange_code(
            exchange_code,
            {"api_key": key, "account_id": acct_id, "tier": tier_val},
            60,
            request=request,
        )
        return RedirectResponse(f"/dashboard?code={exchange_code}", status_code=302)
    return {"api_key": key, "account_id": acct_id, "tier": tier_val}


@app.get("/usage")
async def usage(request: Request):
    try:
        tier, account_id = await resolve_request(request)
    except (AuthRejected, RateLimitRejected) as exc:
        return _auth_error_response(request, exc, "usage")
    if tier == Tier.ADMIN:
        return await store.get_usage_all(request=request)
    if not account_id:
        return JSONResponse({"error": "auth_required"}, status_code=401)
    return await store.get_usage(account_id, request=request)


@app.post("/feedback")
async def feedback(request: Request):
    body, err = await _safe_json(request)
    if err:
        return err
    name, route, issue = body.get("integration", ""), body.get("route", ""), body.get("issue", "")
    if not _SAFE_NAME.fullmatch(name):
        return JSONResponse({"error": "invalid_integration_name"}, status_code=400)
    return {
        "message": "Thanks! Fix it and open a PR.",
        "contribute": GITHUB_REPO,
        "prompt": f"Read {ADD_INTEGRATION_DOC} then open a PR to {GITHUB_REPO} fixing the {route} handler in mocks/{name}.py. Issue: {issue}",
    }


@app.get("/preview/{integration}")
async def preview(integration: str, request: Request):
    for mock in _mocks():
        if mock.prefix.strip("/") != integration:
            continue
        gets = [route for route in mock._routes if route.method == "GET"]
        hit = next(
            (route for route in gets if "{" not in route.path_pattern), gets[0] if gets else None
        )
        if not hit:
            return JSONResponse({"error": "no_get_route"}, status_code=404)
        params = {match: "example" for match in re.findall(r"\{(\w+)\}", hit.path_pattern)}
        response = _response_from_mock(await getattr(mock, hit.handler)(request, **params))
        response.headers["Cache-Control"] = "public, s-maxage=86400, max-age=3600"
        return response
    return JSONResponse({"error": "integration_not_found"}, status_code=404)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def mock_router(request: Request, path: str):
    try:
        tier, account_id = await resolve_request(request)
    except (AuthRejected, RateLimitRejected) as exc:
        return _auth_error_response(request, exc, path)

    full = "/" + path
    matched_mock = next((mock for mock in _mocks() if full.startswith(mock.prefix)), None)
    name = path.split("/")[0]
    if not matched_mock:
        return JSONResponse(
            {
                "error": "integration_not_found",
                "integration": name,
                "message": f"No mock for '{name}' yet. Add it and open a PR!",
                "contribute": f"{GITHUB_REPO}/issues/new",
                "prompt": f"Read {ADD_INTEGRATION_DOC} then open a PR to {GITHUB_REPO} adding mocks/{name}.py with schema-faithful mock responses for the {name} API.",
            },
            status_code=404,
        )

    sub = full[len(matched_mock.prefix) :] or "/"
    result = matched_mock.match(request.method, sub)
    integration = matched_mock.prefix.strip("/")

    if account_id:
        await store.increment_usage(account_id, request=request)
        await store.add_usage_by_integration(account_id, integration, request=request)
    elif tier == Tier.ANON:
        await store.increment_usage("anon", request=request)
        await store.add_usage_by_integration("anon", integration, request=request)

    if request.method != "GET" and tier not in (Tier.PAID, Tier.ADMIN):
        if result and not result[0].writes:
            matched_route, params = result
            response = _response_from_mock(
                await getattr(matched_mock, matched_route.handler)(request, **params)
            )
        elif result:
            matched_route, params = result
            response = _response_from_mock(
                await getattr(matched_mock, matched_route.handler)(request, **params)
            )
            response.headers["X-Verifiabl-Notice"] = WRITE_NOTICE
        else:
            response = JSONResponse(
                {"ok": True}, status_code=201 if request.method == "POST" else 200
            )
            response.headers["X-Verifiabl-Notice"] = WRITE_NOTICE
        response.headers["X-Verifiabl-Contribute"] = GITHUB_REPO
        return response

    if not result:
        return JSONResponse(
            {
                "error": "route_not_mocked",
                "integration": name,
                "message": f"The /{name} integration exists but {request.method} {sub} isn't mocked yet.",
                "contribute": GITHUB_REPO,
                "prompt": f"Read {ADD_INTEGRATION_DOC} then open a PR to {GITHUB_REPO} adding a @route('{request.method}', '{sub}') handler to mocks/{name}.py with a schema-faithful mock response.",
            },
            status_code=404,
        )

    matched_route, params = result
    if matched_route.writes and tier in (Tier.PAID, Tier.ADMIN):
        canonical = await getattr(matched_mock, matched_route.handler)(request, **params)
        write_account = account_id or "admin"
        if request.method != "DELETE":
            body, err = await _safe_json(request)
            if err:
                return err
            persisted = canonical.body if isinstance(canonical.body, dict) else body
            await store.write(write_account, integration, sub, persisted, request=request)
        else:
            await store.delete(write_account, integration, sub, request=request)
        response = _response_from_mock(canonical)
    else:
        stored = await store.read(
            integration, request.method, sub, account_id=account_id, request=request
        )
        if (
            stored.body
            and isinstance(stored.body, dict)
            and stored.body.get("message", "").startswith("No mock")
        ):
            stored = await getattr(matched_mock, matched_route.handler)(request, **params)
        response = _response_from_mock(stored)
    response.headers["X-Verifiabl-Contribute"] = GITHUB_REPO
    return response


if WorkerEntrypoint and asgi:  # pragma: no cover - exercised in deployed Worker

    class Default(WorkerEntrypoint):
        async def fetch(self, request):
            path = urlparse(str(request.url)).path
            asset = _asset_target(path)
            if asset:
                return await self.env.ASSETS.fetch(f"https://assets.local{asset}")
            return await asgi.fetch(app, request, self.env)
