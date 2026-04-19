import asyncio
import os
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from auth import make_magic_token
from main import app
from store import store


class FakeResponse:
    def __init__(self, status_code=200, text="ok"):
        self.status_code = status_code
        self.text = text


class FakeAsyncClient:
    def __init__(self, calls, response=None, error=None):
        self.calls = calls
        self.response = response or FakeResponse()
        self.error = error

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, **kwargs):
        self.calls.append({"url": url, **kwargs})
        if self.error:
            raise self.error
        return self.response


class AppTestCase(unittest.TestCase):
    def setUp(self):
        store.cassettes.clear()
        store.universal.clear()
        store.workspace.clear()
        store.usage.clear()
        store.usage_detail.clear()
        store.accounts.clear()
        store.credentials.clear()
        store.exchange_codes.clear()
        store.rate_hits.clear()

    def test_root_serves_dashboard(self):
        with TestClient(app) as client:
            response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("VERIFIABL", response.text)

    def test_invalid_key_is_rejected(self):
        with TestClient(app) as client:
            response = client.get("/usage", headers={"X-Verifiabl-Key": "vrf_free_missing"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "invalid_api_key")

    def test_free_write_is_dropped_with_notice(self):
        asyncio.run(
            store.save_account_and_credential(
                "acct_free", "free@verifiabl.dev", "vrf_free_test", "free"
            )
        )
        with TestClient(app) as client:
            response = client.post(
                "/stripe/v1/customers",
                headers={"X-Verifiabl-Key": "vrf_free_test"},
                json={"email": "alice@example.com"},
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.headers["X-Verifiabl-Notice"], "writes-not-persisted-upgrade-at-verifiabl.dev"
        )

    def test_healthz_is_available(self):
        with TestClient(app) as client:
            response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_healthz_strict_requires_signup_webhook(self):
        with patch.dict(
            os.environ,
            {"STRICT_HEALTH_CHECKS": "1", "SECRET_KEY": "prod-secret", "SLACK_SIGNUP_WEBHOOK": ""},
            clear=False,
        ):
            with TestClient(app) as client:
                response = client.get("/healthz")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["checks"]["signup_webhook"], "missing")

    def test_auth_verify_new_signup_notifies_slack_once(self):
        calls = []
        with (
            patch.dict(
                os.environ,
                {
                    "SECRET_KEY": "test-secret",
                    "SLACK_SIGNUP_WEBHOOK": "https://hooks.slack.test/signup",
                },
                clear=False,
            ),
            patch("main.httpx.AsyncClient", lambda *args, **kwargs: FakeAsyncClient(calls)),
        ):
            token = make_magic_token({"email": "new@verifiabl.dev"})
            with TestClient(app) as client:
                response = client.get("/auth/verify", params={"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["url"], "https://hooks.slack.test/signup")
        self.assertEqual(calls[0]["json"], {"text": "New signup: new@verifiabl.dev"})

    def test_auth_verify_existing_account_does_not_notify_slack(self):
        asyncio.run(
            store.save_account_and_credential(
                "acct_existing", "existing@verifiabl.dev", "vrf_free_existing", "free"
            )
        )
        calls = []
        with (
            patch.dict(
                os.environ,
                {
                    "SECRET_KEY": "test-secret",
                    "SLACK_SIGNUP_WEBHOOK": "https://hooks.slack.test/signup",
                },
                clear=False,
            ),
            patch("main.httpx.AsyncClient", lambda *args, **kwargs: FakeAsyncClient(calls)),
        ):
            token = make_magic_token({"email": "existing@verifiabl.dev"})
            with TestClient(app) as client:
                response = client.get("/auth/verify", params={"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(calls), 0)

    def test_auth_verify_slack_failure_does_not_break_signup(self):
        calls = []
        with (
            patch.dict(
                os.environ,
                {
                    "SECRET_KEY": "test-secret",
                    "SLACK_SIGNUP_WEBHOOK": "https://hooks.slack.test/signup",
                },
                clear=False,
            ),
            patch(
                "main.httpx.AsyncClient",
                lambda *args, **kwargs: FakeAsyncClient(calls, error=httpx.ConnectError("boom")),
            ),
        ):
            token = make_magic_token({"email": "failslack@verifiabl.dev"})
            with TestClient(app) as client:
                response = client.get("/auth/verify", params={"token": token})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["api_key"].startswith("vrf_free_"))
        self.assertEqual(body["tier"], "free")
        self.assertEqual(len(calls), 1)
        self.assertEqual(
            asyncio.run(store.find_account_by_email("failslack@verifiabl.dev"))["account_id"],
            body["account_id"],
        )

    def test_auth_verify_race_recovers_existing_account(self):
        calls = []
        original_save = store.save_account_and_credential

        async def save_then_conflict(account_id, email, key, tier, request=None):
            await original_save("acct_race", email, "vrf_free_race", "free", request=request)
            raise RuntimeError("UNIQUE constraint failed: accounts.email")

        with (
            patch.dict(
                os.environ,
                {
                    "SECRET_KEY": "test-secret",
                    "SLACK_SIGNUP_WEBHOOK": "https://hooks.slack.test/signup",
                    "TEST_API_KEY": "",
                },
                clear=False,
            ),
            patch("main.httpx.AsyncClient", lambda *args, **kwargs: FakeAsyncClient(calls)),
            patch.object(
                store,
                "save_account_and_credential",
                new=save_then_conflict,
            ),
        ):
            token = make_magic_token({"email": "race@verifiabl.dev"})
            with TestClient(app) as client:
                response = client.get(
                    "/auth/verify",
                    params={"token": token},
                    headers={"accept": "text/html"},
                    follow_redirects=False,
                )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["location"].startswith("/dashboard?code="))
        self.assertEqual(len(calls), 0)


if __name__ == "__main__":
    unittest.main()
