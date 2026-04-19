# CHANGELOG: https://developers.asana.com/docs/change-log  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/Asana/openapi
# SANDBOX:   https://app.asana.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class AsanaMock(BaseMock):
    prefix = "/asana"
    spec_url = "https://github.com/Asana/openapi"
    sandbox_base = "https://app.asana.com"

    @route("GET", "/api/1.0/workspaces", writes=False)
    async def list_workspaces(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"gid": "12345", "resource_type": "workspace", "name": "Mock Workspace"},
                    {"gid": "67890", "resource_type": "workspace", "name": "Verifiabl Dev"},
                ],
            }
        )

    @route("GET", "/api/1.0/users/me", writes=False)
    async def get_current_user(self, request, **kw):
        return MockResponse(
            body={
                "data": {
                    "gid": "1111",
                    "resource_type": "user",
                    "name": "Mock User",
                    "email": "mock@verifiabl.dev",
                },
            }
        )

    @route("GET", "/api/1.0/tasks", writes=False)
    async def list_tasks(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "gid": "task_mock_001",
                        "resource_type": "task",
                        "name": "Mock task one",
                        "resource_subtype": "default_task",
                    },
                    {
                        "gid": "task_mock_002",
                        "resource_type": "task",
                        "name": "Mock task two",
                        "resource_subtype": "default_task",
                    },
                ],
            }
        )

    @route("POST", "/api/1.0/tasks")
    async def create_task(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "data": {
                    "gid": "task_mock_new",
                    "resource_type": "task",
                    "name": "New task",
                    "resource_subtype": "default_task",
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            },
        )

    @route("GET", "/api/1.0/tasks/{task_gid}", writes=False)
    async def get_task(self, request, task_gid="", **kw):
        return MockResponse(
            body={
                "data": {
                    "gid": task_gid or "task_mock_001",
                    "resource_type": "task",
                    "name": "Mock task",
                    "resource_subtype": "default_task",
                    "completed": False,
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            }
        )

    @route("GET", "/api/1.0/workspaces/{workspace_gid}/projects", writes=False)
    async def list_projects_for_workspace(self, request, workspace_gid="", **kw):
        return MockResponse(
            body={
                "data": [
                    {"gid": "proj_mock_001", "resource_type": "project", "name": "Mock Project A"},
                    {"gid": "proj_mock_002", "resource_type": "project", "name": "Mock Project B"},
                ],
            }
        )

    @route("GET", "/api/1.0/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "gid": "proj_mock_001",
                        "resource_type": "project",
                        "name": "Mock Project A",
                        "archived": False,
                    },
                    {
                        "gid": "proj_mock_002",
                        "resource_type": "project",
                        "name": "Mock Project B",
                        "archived": False,
                    },
                ],
            }
        )

    @route("GET", "/api/1.0/projects/{project_gid}", writes=False)
    async def get_project(self, request, project_gid="", **kw):
        return MockResponse(
            body={
                "data": {
                    "gid": project_gid or "proj_mock_001",
                    "resource_type": "project",
                    "name": "Mock Project",
                    "archived": False,
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            }
        )

    @route("POST", "/api/1.0/projects")
    async def create_project(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "data": {
                    "gid": "proj_mock_new",
                    "resource_type": "project",
                    "name": "New project",
                    "archived": False,
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            },
        )
