# CHANGELOG: https://railway.app/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.railway.com/reference/public-api (GraphQL; schema at backboard.railway.com/graphql/v2)
# SANDBOX:   https://railway.com/account/tokens
# SKILL:     —
# MCP:       https://docs.railway.com/ai/mcp-server
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _data_me():
    return {"me": {"id": "user_mock_verifiabl", "name": "Mock User", "email": "mock@verifiabl.dev"}}


def _data_project():
    return {
        "project": {
            "id": "project_mock_001",
            "name": "my-app",
            "description": None,
            "services": {
                "edges": [
                    {"node": {"id": "svc_mock_001", "name": "api"}},
                    {"node": {"id": "svc_mock_002", "name": "postgres"}},
                ]
            },
            "environments": {"edges": [{"node": {"id": "env_mock_001", "name": "production"}}]},
        }
    }


def _data_projects():
    return {
        "projects": {
            "edges": [
                {"node": {"id": "project_mock_001", "name": "my-app"}},
                {"node": {"id": "project_mock_002", "name": "other-app"}},
            ],
            "pageInfo": {"hasNextPage": False, "endCursor": None},
        },
        "externalWorkspaces": [
            {
                "id": "ws_mock_001",
                "name": "My Workspace",
                "projects": [{"id": "project_mock_001", "name": "my-app"}],
            }
        ],
    }


def _data_deployments():
    return {
        "deployments": {
            "edges": [
                {"node": {"id": "deploy_mock_001", "status": "SUCCESS", "createdAt": "1710400000"}},
                {
                    "node": {
                        "id": "deploy_mock_002",
                        "status": "BUILDING",
                        "createdAt": "1710400100",
                    }
                },
            ],
            "pageInfo": {"hasNextPage": False, "endCursor": None},
        }
    }


def _data_project_create():
    return {"projectCreate": {"id": "project_mock_new", "name": "my-new-project"}}


class RailwayMock(BaseMock):
    prefix = "/railway"
    spec_url = "https://docs.railway.com/reference/public-api"
    sandbox_base = "https://backboard.railway.com"

    @route("POST", "/graphql/v2", writes=False)
    async def graphql(self, request, **kw):
        try:
            body = await request.json()
        except Exception:
            body = {}
        q = (body.get("query") or "").strip()
        op = body.get("operationName") or ""
        if "me" in q and "me {" in q or op == "me":
            return MockResponse(body={"data": _data_me()})
        if "projectCreate" in q or op == "projectCreate":
            return MockResponse(status=201, body={"data": _data_project_create()})
        if (
            "deployments(" in q
            or "deployment(" in q
            or "deployments " in q
            or op in ("deployments", "deployment")
        ):
            return MockResponse(body={"data": _data_deployments()})
        if "project(" in q or "project " in q or op == "project":
            return MockResponse(body={"data": _data_project()})
        if (
            "externalWorkspaces" in q
            or "projects " in q
            or "projects(" in q
            or op in ("projects", "externalWorkspaces")
        ):
            return MockResponse(body={"data": _data_projects()})
        return MockResponse(body={"data": _data_me()})
