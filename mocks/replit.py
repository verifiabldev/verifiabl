# CHANGELOG: https://docs.replit.com/updates/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.replit.com/ (Extensions/GraphQL; no public OpenAPI)
# SANDBOX:   https://replit.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _data_me():
    return {
        "currentUser": {
            "id": "user_mock_verifiabl",
            "username": "verifiabl",
            "firstName": "Mock",
            "lastName": "User",
            "image": None,
            "isLoggedIn": True,
        }
    }


def _data_repl():
    return {
        "repl": {
            "id": "repl_mock_001",
            "slug": "my-app",
            "title": "My App",
            "language": "python3",
            "isOwner": True,
            "timeCreated": "1710400000",
            "url": "https://replit.com/@verifiabl/my-app",
        }
    }


def _data_repls():
    return {
        "repls": [
            {
                "id": "repl_mock_001",
                "slug": "my-app",
                "title": "My App",
                "language": "python3",
                "url": "https://replit.com/@verifiabl/my-app",
            },
            {
                "id": "repl_mock_002",
                "slug": "other-app",
                "title": "Other App",
                "language": "nodejs",
                "url": "https://replit.com/@verifiabl/other-app",
            },
        ]
    }


def _data_deployment():
    return {
        "deployment": {
            "id": "deploy_mock_001",
            "status": "live",
            "url": "https://my-app.verifiabl.repl.co",
            "createdAt": 1710400000,
            "repl": {"id": "repl_mock_001", "slug": "my-app"},
        }
    }


def _data_deployments():
    return {
        "deployments": [
            {
                "id": "deploy_mock_001",
                "status": "live",
                "url": "https://my-app.verifiabl.repl.co",
                "createdAt": 1710400000,
            },
            {"id": "deploy_mock_002", "status": "building", "url": None, "createdAt": 1710400100},
        ]
    }


class ReplitMock(BaseMock):
    prefix = "/replit"
    spec_url = "https://docs.replit.com/"
    sandbox_base = "https://replit.com"

    @route("POST", "/graphql", writes=False)
    async def graphql(self, request, **kw):
        try:
            body = await request.json()
        except Exception:
            body = {}
        q = (body.get("query") or "").strip()
        op = body.get("operationName") or ""
        if "currentUser" in q or "me " in q or op in ("currentUser", "Me", "me"):
            return MockResponse(body={"data": _data_me()})
        if (
            "deployments(" in q
            or "deployment(" in q
            or "deployments " in q
            or op in ("deployments", "Deployments")
        ):
            return MockResponse(body={"data": _data_deployments()})
        if "deployment(" in q and "deployments(" not in q or op == "deployment":
            return MockResponse(body={"data": _data_deployment()})
        if "repls(" in q or "repls " in q or op in ("repls", "Repls"):
            return MockResponse(body={"data": _data_repls()})
        if "repl(" in q or "repl " in q or op in ("repl", "Repl"):
            return MockResponse(body={"data": _data_repl()})
        return MockResponse(body={"data": _data_me()})
