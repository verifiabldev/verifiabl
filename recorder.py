import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx

from mocks.base import BaseMock
from store import store

logger = logging.getLogger("verifiabl.recorder")

ENV_KEYS = {
    "stripe": "STRIPE_TEST_KEY",
    "slack": "SLACK_BOT_TOKEN",
    "hubspot": "HUBSPOT_ACCESS_TOKEN",
}

AUTH_HEADERS = {
    "stripe": lambda k: {"Authorization": f"Bearer {k}"},
    "slack": lambda k: {"Authorization": f"Bearer {k}"},
    "hubspot": lambda k: {"Authorization": f"Bearer {k}"},
}

DRIFT_LOG = Path("drift.jsonl")


async def _record_one(mock: BaseMock, client: httpx.AsyncClient):
    name = mock.prefix.strip("/")
    env_var = ENV_KEYS.get(name)
    api_key = os.environ.get(env_var, "") if env_var else ""
    if not api_key:
        logger.info("Skipping %s — no credentials", name)
        return

    headers = AUTH_HEADERS.get(name, lambda k: {})(api_key)
    for r in mock._routes:
        if r.method != "GET":
            continue
        url = f"{mock.sandbox_base}{r.path_pattern}"
        if "{" in url:
            continue
        try:
            resp = await client.get(url, headers=headers, timeout=15)
            key = store._key(name, r.method, r.path_pattern)
            body = resp.json() if resp.status_code < 400 else None
            store.cassettes[key] = body
            store.universal[store._key(name, r.path_pattern)] = body
            if resp.status_code >= 400:
                _log_drift(name, r.method, r.path_pattern, resp.status_code, "non-2xx response")
        except Exception as e:
            _log_drift(name, r.method, r.path_pattern, 0, str(e))


def _log_drift(integration: str, method: str, path: str, status: int, reason: str):
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "integration": integration,
        "method": method,
        "path": path,
        "status": status,
        "reason": reason,
    }
    logger.warning("Drift: %s", entry)
    with open(DRIFT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


async def run_all():
    logger.info("Recorder starting")
    async with httpx.AsyncClient() as client:
        for cls in BaseMock.__subclasses__():
            await _record_one(cls(), client)
    logger.info("Recorder complete")
