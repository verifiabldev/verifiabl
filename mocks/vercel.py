# CHANGELOG: https://vercel.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://vercel.com/docs/rest-api/reference
# SANDBOX:   https://vercel.com/dashboard
# SKILL:     —
# MCP:       https://mcp.vercel.com
# LLMS:      https://vercel.com/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: Vercel uses versioned paths per resource (v2 user/teams, v6/v13 deployments, v10/v11 projects); full set needs 9 routes.
class VercelMock(BaseMock):
    prefix = "/vercel"
    spec_url = "https://vercel.com/docs/rest-api/reference"
    sandbox_base = "https://api.vercel.com"

    @route("GET", "/v2/user", writes=False)
    async def get_user(self, request, **kw):
        return MockResponse(
            body={
                "id": "user_mock_verifiabl",
                "email": "mock@verifiabl.dev",
                "name": "Mock User",
                "username": "mockuser",
                "defaultTeamId": "team_mock_verifiabl",
            }
        )

    @route("GET", "/v2/teams/{team_id}", writes=False)
    async def get_team(self, request, team_id="", **kw):
        return MockResponse(
            body={
                "id": team_id or "team_mock_verifiabl",
                "name": "Mock Team",
                "slug": "mock-team",
                "avatar": "https://verifiabl.dev/team.png",
            }
        )

    @route("GET", "/v10/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "projects": [
                    {
                        "id": "prj_mock_001",
                        "name": "my-app",
                        "framework": "nextjs",
                        "accountId": "team_mock_verifiabl",
                    },
                    {
                        "id": "prj_mock_002",
                        "name": "docs-site",
                        "framework": "vite",
                        "accountId": "team_mock_verifiabl",
                    },
                ],
            }
        )

    @route("GET", "/v10/projects/{id_or_name}", writes=False)
    async def get_project(self, request, id_or_name="", **kw):
        return MockResponse(
            body={
                "id": id_or_name or "prj_mock_001",
                "name": id_or_name or "my-app",
                "framework": "nextjs",
                "accountId": "team_mock_verifiabl",
                "createdAt": 1710400000000,
            }
        )

    @route("POST", "/v11/projects")
    async def create_project(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "prj_mock_new",
                "name": "new-project",
                "framework": "nextjs",
                "accountId": "team_mock_verifiabl",
            },
        )

    @route("GET", "/v6/deployments", writes=False)
    async def list_deployments(self, request, **kw):
        return MockResponse(
            body={
                "deployments": [
                    {
                        "uid": "dpl_mock_001",
                        "name": "my-app",
                        "url": "my-app-mock.vercel.app",
                        "state": "READY",
                        "created": 1710400000000,
                    },
                    {
                        "uid": "dpl_mock_002",
                        "name": "docs-site",
                        "url": "docs-site-mock.vercel.app",
                        "state": "READY",
                        "created": 1710390000000,
                    },
                ],
            }
        )

    @route("GET", "/v13/deployments/{id_or_url}", writes=False)
    async def get_deployment(self, request, id_or_url="", **kw):
        return MockResponse(
            body={
                "id": id_or_url or "dpl_mock_001",
                "uid": id_or_url or "dpl_mock_001",
                "name": "my-app",
                "url": "my-app-mock.vercel.app",
                "readyState": "READY",
                "state": "READY",
                "projectId": "prj_mock_001",
                "created": 1710400000000,
            }
        )

    @route("POST", "/v13/deployments")
    async def create_deployment(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "dpl_mock_new",
                "uid": "dpl_mock_new",
                "name": "my-app",
                "url": "my-app-new.vercel.app",
                "readyState": "QUEUED",
                "projectId": "prj_mock_001",
                "created": 1710400000000,
            },
        )
