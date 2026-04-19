# CHANGELOG: https://developers.linear.app/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developers.linear.app/docs/graphql/working-with-the-graphql-api
# SANDBOX:   https://linear.app (API at api.linear.app/graphql; this mock is a REST facade for common operations)
# SKILL:     —
# MCP:       https://mcp.linear.app/mcp
# LLMS:      —
# AUTH:      API key or Bearer token in Authorization header (per Linear docs)
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: REST facade over GraphQL needs 10 routes for teams, projects, issues, and workflow states.
class LinearMock(BaseMock):
    prefix = "/linear"
    spec_url = "https://developers.linear.app/docs/graphql/working-with-the-graphql-api"
    sandbox_base = "https://api.linear.app"

    @route("GET", "/api/v1/me", writes=False)
    async def me(self, request, **kw):
        return MockResponse(
            body={"id": "user_mock_verifiabl", "name": "Mock User", "email": "mock@verifiabl.dev"}
        )

    @route("GET", "/api/v1/teams", writes=False)
    async def list_teams(self, request, **kw):
        return MockResponse(
            body={
                "nodes": [
                    {"id": "team_mock_001", "key": "ENG", "name": "Engineering"},
                    {"id": "team_mock_002", "key": "PD", "name": "Product"},
                ],
            }
        )

    @route("GET", "/api/v1/teams/{id}", writes=False)
    async def get_team(self, request, id="", **kw):
        return MockResponse(body={"id": id or "team_mock_001", "key": "ENG", "name": "Engineering"})

    @route("GET", "/api/v1/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "nodes": [
                    {"id": "project_mock_001", "name": "Q1 Roadmap", "state": "started"},
                    {"id": "project_mock_002", "name": "Backlog", "state": "planned"},
                ],
            }
        )

    @route("GET", "/api/v1/projects/{id}", writes=False)
    async def get_project(self, request, id="", **kw):
        return MockResponse(
            body={"id": id or "project_mock_001", "name": "Q1 Roadmap", "state": "started"}
        )

    @route("GET", "/api/v1/issues", writes=False)
    async def list_issues(self, request, **kw):
        return MockResponse(
            body={
                "nodes": [
                    {
                        "id": "issue_mock_001",
                        "identifier": "ENG-1",
                        "title": "Mock issue",
                        "state": {"id": "state_mock_001", "name": "Todo"},
                        "createdAt": 1710400000,
                    },
                    {
                        "id": "issue_mock_002",
                        "identifier": "ENG-2",
                        "title": "Another issue",
                        "state": {"id": "state_mock_002", "name": "In Progress"},
                        "createdAt": 1710400000,
                    },
                ],
            }
        )

    @route("GET", "/api/v1/issues/{id}", writes=False)
    async def get_issue(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "issue_mock_001",
                "identifier": "ENG-1",
                "title": "Mock issue",
                "state": {"id": "state_mock_001", "name": "Todo"},
                "createdAt": 1710400000,
                "updatedAt": 1710400000,
            }
        )

    @route("POST", "/api/v1/issues")
    async def create_issue(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "issue_mock_new",
                "identifier": "ENG-3",
                "title": "New issue",
                "state": {"id": "state_mock_001", "name": "Todo"},
                "createdAt": 1710400000,
            },
        )

    @route("PATCH", "/api/v1/issues/{id}")
    async def update_issue(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "issue_mock_001",
                "identifier": "ENG-1",
                "title": "Updated",
                "updatedAt": 1710400000,
            }
        )

    @route("GET", "/api/v1/workflow-states", writes=False)
    async def list_workflow_states(self, request, **kw):
        return MockResponse(
            body={
                "nodes": [
                    {"id": "state_mock_001", "name": "Todo", "type": "unstarted"},
                    {"id": "state_mock_002", "name": "In Progress", "type": "started"},
                    {"id": "state_mock_003", "name": "Done", "type": "completed"},
                ],
            }
        )
