from __future__ import annotations

import os
import re
from typing import Optional, Tuple

from itsdangerous import URLSafeTimedSerializer
from starlette.requests import Request

from models import Tier
from store import store

ANON_LIMIT = 60
FREE_LIMIT = 1000
PAID_LIMIT = 10000
MAGIC_LINK_LIMIT = 5
WINDOW = 3600
_DEFAULT_SECRETS = {"", "dev-secret", "change-me-in-production"}
_EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class AuthRejected(Exception):
    def __init__(
        self,
        error: str = "invalid_api_key",
        status: int = 401,
        message: str = "Invalid or revoked API key.",
    ):
        self.error = error
        self.status = status
        self.message = message
        super().__init__(message)


class RateLimitRejected(Exception):
    def __init__(self, scope: str, message: str):
        self.scope = scope
        self.error = "rate_limit_exceeded"
        self.status = 429
        self.message = message
        super().__init__(message)


def _env_value(request: Request | None, name: str, default: Optional[str] = None) -> Optional[str]:
    env = None
    if request is not None:
        env = (getattr(request, "scope", None) or {}).get("env")
    value = getattr(env, name, None) if env else None
    if value not in (None, ""):
        return value
    return os.environ.get(name, default)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("cf-connecting-ip") or request.headers.get(
        "x-forwarded-for", ""
    )
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


def _extract_key(request: Request) -> Optional[str]:
    key = request.headers.get("x-verifiabl-key")
    if key:
        return key
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer vrf_"):
        return auth[7:]
    return None


def _signer(request: Request | None = None) -> URLSafeTimedSerializer:
    secret = _env_value(request, "SECRET_KEY")
    if secret not in _DEFAULT_SECRETS:
        return URLSafeTimedSerializer(secret)
    if request is None or not (getattr(request, "scope", None) or {}).get("env"):
        return URLSafeTimedSerializer(secret or "dev-secret")
    raise RuntimeError("SECRET_KEY must be set to a non-default value in production")


async def check_magic_link_request(request: Request) -> None:
    allowed = await store.hit_rate_limit(
        "magic", _client_ip(request), MAGIC_LINK_LIMIT, WINDOW, request=request
    )
    if not allowed:
        raise RateLimitRejected("magic", "Too many sign-in emails requested. Try again later.")


async def resolve_request(request: Request) -> Tuple[Tier, Optional[str]]:
    key = _extract_key(request)
    if not key:
        allowed = await store.hit_rate_limit(
            "anon", _client_ip(request), ANON_LIMIT, WINDOW, request=request
        )
        if not allowed:
            raise RateLimitRejected("anon", "Get a free API key to continue.")
        return Tier.ANON, None
    admin_key = _env_value(request, "ADMIN_API_KEY")
    if admin_key and key == admin_key:
        return Tier.ADMIN, None
    credential = await store.get_credential(key, request=request)
    if not credential or credential.get("revoked"):
        raise AuthRejected()
    tier = Tier(credential["tier"])
    if tier in (Tier.FREE, Tier.PAID):
        allowed = await store.hit_rate_limit(
            tier.value, credential["account_id"], rate_limit_for(tier), WINDOW, request=request
        )
        if not allowed:
            raise RateLimitRejected(
                tier.value, f"{tier.value.capitalize()} tier hourly limit exceeded."
            )
    return tier, credential["account_id"]


def make_magic_token(data: dict, request: Request | None = None) -> str:
    return _signer(request).dumps(data)


def verify_magic_token(
    token: str, request: Request | None = None, max_age: int = 86400
) -> Optional[dict]:
    try:
        return _signer(request).loads(token, max_age=max_age)
    except Exception:
        return None


def rate_limit_for(tier: Tier) -> int:
    return {Tier.ANON: ANON_LIMIT, Tier.FREE: FREE_LIMIT, Tier.PAID: PAID_LIMIT, Tier.ADMIN: 0}[
        tier
    ]


def validate_email(raw: str) -> Optional[str]:
    email = raw.strip()[:254]
    return email if _EMAIL_RE.fullmatch(email) else None
