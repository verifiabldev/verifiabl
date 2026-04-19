# CHANGELOG: https://render.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://api-docs.render.com/v1.0/openapi/render-public-api-1.json
# SANDBOX:   https://dashboard.render.com/u/settings?add-api-key
# SKILL:     https://render.com/docs/llm-support
# MCP:       https://mcp.render.com/mcp
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per OpenAPI BearerAuth)
from mocks.base import BaseMock, route
from models import MockResponse


def _owner(oid: str = "owner_mock_verifiabl", name: str = "Mock User", typ: str = "user"):
    o = {"id": oid, "name": name, "type": typ}
    if typ == "user":
        o["email"] = "mock@verifiabl.dev"
    return o


def _service(id_: str = "srv_mock_001", name: str = "my-web-service"):
    return {
        "id": id_,
        "name": name,
        "type": "web_service",
        "ownerId": "owner_mock_verifiabl",
        "repo": "https://github.com/render-examples/flask-hello-world",
        "branch": "main",
        "createdAt": "2024-03-14T12:00:00.000Z",
        "slug": name,
        "dashboardUrl": "https://dashboard.render.com/web/srv_mock_001",
        "environmentId": "env_mock_001",
    }


def _deploy(id_: str = "dpl_mock_001", status: str = "live"):
    return {
        "id": id_,
        "status": status,
        "trigger": "manual",
        "commit": {
            "id": "abc123",
            "message": "Deploy via API",
            "createdAt": "2024-03-14T12:00:00.000Z",
        },
        "createdAt": "2024-03-14T12:00:00.000Z",
        "updatedAt": "2024-03-14T12:00:00.000Z",
        "startedAt": "2024-03-14T12:00:00.000Z",
        "finishedAt": "2024-03-14T12:01:00.000Z",
    }


def _project(pid: str = "prj_mock_001", name: str = "my-app"):
    return {
        "id": pid,
        "name": name,
        "owner": _owner(),
        "environmentIds": ["env_mock_001"],
        "createdAt": "2024-03-14T12:00:00.000Z",
        "updatedAt": "2024-03-14T12:00:00.000Z",
    }


# LOC EXCEPTION: 13 routes + cursor envelope (owner/service/deploy/project list) per OpenAPI.
class RenderMock(BaseMock):
    prefix = "/render"
    spec_url = "https://api-docs.render.com/v1.0/openapi/render-public-api-1.json"
    sandbox_base = "https://api.render.com/v1"

    @route("GET", "/v1/owners", writes=False)
    async def list_owners(self, request, **kw):
        return MockResponse(
            body=[
                {"owner": _owner("owner_mock_verifiabl", "Mock User", "user"), "cursor": "c1"},
                {"owner": _owner("owner_mock_team", "Mock Team", "team"), "cursor": "c2"},
            ]
        )

    @route("GET", "/v1/owners/{ownerId}", writes=False)
    async def get_owner(self, request, ownerId="", **kw):
        return MockResponse(body=_owner(ownerId or "owner_mock_verifiabl"))

    @route("GET", "/v1/services", writes=False)
    async def list_services(self, request, **kw):
        return MockResponse(
            body=[
                {"service": _service("srv_mock_001", "my-web-service"), "cursor": "c1"},
                {"service": _service("srv_mock_002", "api"), "cursor": "c2"},
            ]
        )

    @route("POST", "/v1/services")
    async def create_service(self, request, **kw):
        return MockResponse(
            status=201,
            body={"service": _service("srv_mock_new", "new-service"), "deployId": "dpl_mock_new"},
        )

    @route("GET", "/v1/services/{serviceId}", writes=False)
    async def get_service(self, request, serviceId="", **kw):
        return MockResponse(body=_service(serviceId or "srv_mock_001", "my-web-service"))

    @route("PATCH", "/v1/services/{serviceId}")
    async def update_service(self, request, serviceId="", **kw):
        return MockResponse(body=_service(serviceId or "srv_mock_001", "my-web-service"))

    @route("GET", "/v1/services/{serviceId}/deploys", writes=False)
    async def list_deploys(self, request, serviceId="", **kw):
        return MockResponse(
            body=[
                {"deploy": _deploy("dpl_mock_001", "live"), "cursor": "c1"},
                {"deploy": _deploy("dpl_mock_002", "building"), "cursor": "c2"},
            ]
        )

    @route("POST", "/v1/services/{serviceId}/deploys")
    async def create_deploy(self, request, serviceId="", **kw):
        return MockResponse(status=201, body=_deploy("dpl_mock_new", "building"))

    @route("GET", "/v1/services/{serviceId}/deploys/{deployId}", writes=False)
    async def get_deploy(self, request, serviceId="", deployId="", **kw):
        return MockResponse(body=_deploy(deployId or "dpl_mock_001", "live"))

    @route("GET", "/v1/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body=[
                {"project": _project("prj_mock_001", "my-app"), "cursor": "c1"},
                {"project": _project("prj_mock_002", "docs-site"), "cursor": "c2"},
            ]
        )

    @route("POST", "/v1/projects")
    async def create_project(self, request, **kw):
        return MockResponse(status=201, body=_project("prj_mock_new", "new-project"))

    @route("GET", "/v1/projects/{projectId}", writes=False)
    async def get_project(self, request, projectId="", **kw):
        return MockResponse(body=_project(projectId or "prj_mock_001", "my-app"))

    @route("PATCH", "/v1/projects/{projectId}")
    async def update_project(self, request, projectId="", **kw):
        return MockResponse(body=_project(projectId or "prj_mock_001", "my-app"))
