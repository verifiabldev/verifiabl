from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional

from models import MockResponse

_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        created_at INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS credentials (
        api_key TEXT PRIMARY KEY,
        account_id TEXT NOT NULL,
        tier TEXT NOT NULL,
        revoked INTEGER NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usage_totals (
        account_id TEXT PRIMARY KEY,
        requests INTEGER NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usage_by_integration (
        account_id TEXT NOT NULL,
        integration TEXT NOT NULL,
        requests INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (account_id, integration)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workspace (
        account_id TEXT NOT NULL,
        integration TEXT NOT NULL,
        path TEXT NOT NULL,
        body TEXT NOT NULL,
        updated_at INTEGER NOT NULL,
        PRIMARY KEY (account_id, integration, path)
    )
    """,
)


class Store:
    def __init__(self):
        self.cassettes: dict[str, dict] = {}
        self.universal: dict[str, dict] = {}
        self.workspace: dict[str, dict] = {}
        self.usage: dict[str, int] = {}
        self.usage_detail: dict[str, int] = {}
        self.accounts: dict[str, dict] = {}
        self.credentials: dict[str, dict] = {}
        self.exchange_codes: dict[str, tuple[int, dict]] = {}
        self.rate_hits: dict[str, int] = {}
        self._schema_ready = False

    @staticmethod
    def _key(*parts: str) -> str:
        return ":".join(parts)

    @staticmethod
    def _row_value(row: Optional[dict], name: str, default=None):
        if not row:
            return default
        if hasattr(row, "get"):
            return row.get(name, default)
        try:
            return row[name]
        except Exception:
            return default

    @staticmethod
    def _row(row):
        if row is None:
            return None
        to_py = getattr(row, "to_py", None)
        if callable(to_py):
            row = to_py()
        if isinstance(row, dict):
            return row
        items = getattr(row, "items", None)
        if callable(items):
            return dict(items())
        try:
            return dict(row)
        except Exception:
            return row

    @staticmethod
    def _env(request=None, env=None):
        if env is not None:
            return env
        if request is None:
            return None
        scope = getattr(request, "scope", None) or {}
        return scope.get("env")

    async def _ensure_schema(self, env) -> None:
        if not env or not getattr(env, "DB", None) or self._schema_ready:
            return
        for statement in _SCHEMA:
            await env.DB.prepare(statement).run()
        self._schema_ready = True

    async def _run(self, env, sql: str, *args):
        await self._ensure_schema(env)
        stmt = env.DB.prepare(sql)
        if args:
            stmt = stmt.bind(*args)
        return await stmt.run()

    async def _first(self, env, sql: str, *args) -> Optional[dict]:
        result = await self._run(env, sql, *args)
        rows = getattr(result, "results", None) or []
        return self._row(rows[0]) if rows else None

    async def _rows(self, env, sql: str, *args) -> list[dict]:
        result = await self._run(env, sql, *args)
        return [self._row(row) for row in (getattr(result, "results", None) or [])]

    async def read(
        self,
        integration: str,
        method: str,
        path: str,
        account_id: Optional[str] = None,
        request=None,
    ) -> MockResponse:
        env = self._env(request)
        if account_id:
            if env and getattr(env, "DB", None):
                row = await self._first(
                    env,
                    "SELECT body FROM workspace WHERE account_id = ? AND integration = ? AND path = ?",
                    account_id,
                    integration,
                    path,
                )
                if row and row.get("body"):
                    return MockResponse(body=json.loads(row["body"]))
            ws_key = self._key(account_id, integration, path)
            if ws_key in self.workspace:
                return MockResponse(body=self.workspace[ws_key])
        cas_key = self._key(integration, method, path)
        if cas_key in self.cassettes:
            return MockResponse(body=self.cassettes[cas_key])
        uni_key = self._key(integration, path)
        if uni_key in self.universal:
            return MockResponse(body=self.universal[uni_key])
        return MockResponse(body={"message": f"No mock data for {method} {path}"})

    async def write(
        self, account_id: str, integration: str, path: str, data: dict, request=None
    ) -> MockResponse:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            await self._run(
                env,
                """
                INSERT INTO workspace (account_id, integration, path, body, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(account_id, integration, path)
                DO UPDATE SET body = excluded.body, updated_at = excluded.updated_at
                """,
                account_id,
                integration,
                path,
                json.dumps(data),
                int(time.time()),
            )
        else:
            self.workspace[self._key(account_id, integration, path)] = data
        return MockResponse(status=201, body=data)

    async def delete(
        self, account_id: str, integration: str, path: str, request=None
    ) -> MockResponse:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            await self._run(
                env,
                "DELETE FROM workspace WHERE account_id = ? AND integration = ? AND path = ?",
                account_id,
                integration,
                path,
            )
        else:
            self.workspace.pop(self._key(account_id, integration, path), None)
        return MockResponse(body={"deleted": True})

    async def increment_usage(self, account_id: str, request=None) -> int:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            await self._run(
                env,
                """
                INSERT INTO usage_totals (account_id, requests)
                VALUES (?, 1)
                ON CONFLICT(account_id)
                DO UPDATE SET requests = usage_totals.requests + 1
                """,
                account_id,
            )
            row = await self._first(
                env, "SELECT requests FROM usage_totals WHERE account_id = ?", account_id
            )
            return int(self._row_value(row, "requests", 0))
        self.usage[account_id] = self.usage.get(account_id, 0) + 1
        return self.usage[account_id]

    async def add_usage_by_integration(
        self, account_id: str, integration: str, request=None
    ) -> None:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            await self._run(
                env,
                """
                INSERT INTO usage_by_integration (account_id, integration, requests)
                VALUES (?, ?, 1)
                ON CONFLICT(account_id, integration)
                DO UPDATE SET requests = usage_by_integration.requests + 1
                """,
                account_id,
                integration,
            )
            return
        detail_key = self._key(account_id, integration)
        self.usage_detail[detail_key] = self.usage_detail.get(detail_key, 0) + 1

    async def _by_integration(self, account_id: Optional[str], request=None) -> dict[str, int]:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            if account_id is None:
                rows = await self._rows(
                    env,
                    """
                    SELECT integration, SUM(requests) AS requests
                    FROM usage_by_integration
                    GROUP BY integration
                    ORDER BY requests DESC, integration ASC
                    """,
                )
            else:
                rows = await self._rows(
                    env,
                    """
                    SELECT integration, requests
                    FROM usage_by_integration
                    WHERE account_id = ?
                    ORDER BY requests DESC, integration ASC
                    """,
                    account_id,
                )
            return {row["integration"]: int(row["requests"]) for row in rows}
        out: dict[str, int] = {}
        for key, value in self.usage_detail.items():
            acct, integration = key.split(":", 1)
            if account_id and acct != account_id:
                continue
            out[integration] = out.get(integration, 0) + value
        return dict(sorted(out.items(), key=lambda item: -item[1]))

    async def get_usage(self, account_id: str, request=None) -> dict:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            row = await self._first(
                env, "SELECT requests FROM usage_totals WHERE account_id = ?", account_id
            )
            count = int(self._row_value(row, "requests", 0))
            detail = await self._by_integration(account_id, request=request)
            return {
                "account_id": account_id,
                "requests": count,
                "cost_cents": count,
                "by_integration": detail,
            }
        count = self.usage.get(account_id, 0)
        return {
            "account_id": account_id,
            "requests": count,
            "cost_cents": count,
            "by_integration": await self._by_integration(account_id, request=request),
        }

    async def get_usage_all(self, request=None) -> dict:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            total_row = await self._first(
                env, "SELECT COALESCE(SUM(requests), 0) AS requests FROM usage_totals"
            )
            anon_row = await self._first(
                env, "SELECT requests FROM usage_totals WHERE account_id = ?", "anon"
            )
            return {
                "account_id": None,
                "requests": int(self._row_value(total_row, "requests", 0)),
                "cost_cents": int(self._row_value(total_row, "requests", 0)),
                "by_integration": await self._by_integration(None, request=request),
                "anon_requests": int(self._row_value(anon_row, "requests", 0)),
                "anon_by_integration": await self._by_integration("anon", request=request),
            }
        total = sum(self.usage.values())
        anon_requests = self.usage.get("anon", 0)
        return {
            "account_id": None,
            "requests": total,
            "cost_cents": total,
            "by_integration": await self._by_integration(None, request=request),
            "anon_requests": anon_requests,
            "anon_by_integration": await self._by_integration("anon", request=request),
        }

    async def seed_test_account(self, account_id: str, key: str, email: str, request=None) -> None:
        await self.save_account_and_credential(account_id, email, key, "free", request=request)

    async def find_account_by_email(self, email: str, request=None) -> Optional[dict]:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            return await self._first(
                env, "SELECT account_id, email FROM accounts WHERE email = ?", email
            )
        for account in self.accounts.values():
            if account.get("email") == email:
                return account
        return None

    async def find_active_credential(self, account_id: str, request=None) -> Optional[dict]:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            return await self._first(
                env,
                """
                SELECT api_key AS key, account_id, tier, revoked
                FROM credentials
                WHERE account_id = ? AND revoked = 0
                ORDER BY created_at DESC
                LIMIT 1
                """,
                account_id,
            )
        for credential in self.credentials.values():
            if credential.get("account_id") == account_id and not credential.get("revoked"):
                return credential
        return None

    async def get_credential(self, key: str, request=None) -> Optional[dict]:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            return await self._first(
                env,
                "SELECT api_key AS key, account_id, tier, revoked FROM credentials WHERE api_key = ?",
                key,
            )
        return self.credentials.get(key)

    async def save_account_and_credential(
        self, account_id: str, email: str, key: str, tier: str, request=None
    ) -> None:
        env = self._env(request)
        if env and getattr(env, "DB", None):
            now = int(time.time())
            await self._run(
                env,
                """
                INSERT INTO accounts (account_id, email, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(account_id)
                DO UPDATE SET email = excluded.email
                """,
                account_id,
                email,
                now,
            )
            await self._run(
                env,
                """
                INSERT INTO credentials (api_key, account_id, tier, revoked, created_at)
                VALUES (?, ?, ?, 0, ?)
                ON CONFLICT(api_key)
                DO UPDATE SET account_id = excluded.account_id, tier = excluded.tier, revoked = 0
                """,
                key,
                account_id,
                tier,
                now,
            )
            return
        self.accounts[account_id] = {"account_id": account_id, "email": email}
        self.credentials[key] = {
            "key": key,
            "account_id": account_id,
            "tier": tier,
            "revoked": False,
        }

    async def store_exchange_code(
        self, code: str, data: dict, ttl_seconds: int, request=None
    ) -> None:
        env = self._env(request)
        kv = getattr(env, "STATE_KV", None) if env else None
        if kv:
            await kv.put(f"exchange:{code}", json.dumps(data), {"expirationTtl": ttl_seconds})
            return
        self.exchange_codes[code] = (int(time.time()) + ttl_seconds, data)

    async def consume_exchange_code(self, code: str, request=None) -> Optional[dict]:
        env = self._env(request)
        kv = getattr(env, "STATE_KV", None) if env else None
        if kv:
            key = f"exchange:{code}"
            payload = await kv.get(key)
            if not payload:
                return None
            await kv.delete(key)
            return json.loads(payload)
        entry = self.exchange_codes.pop(code, None)
        if not entry:
            return None
        expires_at, data = entry
        if expires_at < int(time.time()):
            return None
        return data

    async def hit_rate_limit(
        self, scope: str, bucket: str, limit: int, window_seconds: int, request=None
    ) -> bool:
        window = int(time.time()) // window_seconds
        key = f"rate:{scope}:{bucket}:{window}"
        env = self._env(request)
        kv = getattr(env, "STATE_KV", None) if env else None
        if kv:
            current = int(await kv.get(key) or "0")
            if current >= limit:
                return False
            await kv.put(key, str(current + 1), {"expirationTtl": window_seconds + 60})
            return True
        current = self.rate_hits.get(key, 0)
        if current >= limit:
            return False
        self.rate_hits[key] = current + 1
        return True

    def load_fixtures(self, fixtures_dir: Path):
        for path in fixtures_dir.glob("*.json"):
            integration = path.stem
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
            for route_path, body in data.items():
                self.universal[self._key(integration, route_path)] = body


store = Store()
