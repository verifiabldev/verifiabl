# CHANGELOG: https://docs.gitlab.com/ee/update/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/openapi/openapi.yaml
# SANDBOX:   https://gitlab.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class GitLabMock(BaseMock):
    prefix = "/gitlab"
    spec_url = "https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/openapi/openapi.yaml"
    sandbox_base = "https://gitlab.com"

    @route("GET", "/api/v4/user", writes=False)
    async def current_user(self, request, **kw):
        return MockResponse(
            body={
                "id": 1,
                "username": "mockuser",
                "email": "mock@verifiabl.dev",
                "name": "Mock User",
            }
        )

    @route("GET", "/api/v4/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 1,
                    "name": "mock-project",
                    "path_with_namespace": "group/mock-project",
                    "default_branch": "main",
                    "web_url": "https://gitlab.com/group/mock-project",
                },
                {
                    "id": 2,
                    "name": "other-repo",
                    "path_with_namespace": "group/other-repo",
                    "default_branch": "main",
                    "web_url": "https://gitlab.com/group/other-repo",
                },
            ]
        )

    @route("POST", "/api/v4/projects")
    async def create_project(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": 3,
                "name": "new-project",
                "path_with_namespace": "group/new-project",
                "default_branch": "main",
                "web_url": "https://gitlab.com/group/new-project",
            },
        )

    @route("GET", "/api/v4/projects/{id}", writes=False)
    async def get_project(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1,
                "name": "mock-project",
                "path_with_namespace": "group/mock-project",
                "default_branch": "main",
                "web_url": "https://gitlab.com/group/mock-project",
            }
        )

    @route("GET", "/api/v4/projects/{id}/issues", writes=False)
    async def list_issues(self, request, id="", **kw):
        return MockResponse(
            body=[
                {
                    "id": 1,
                    "iid": 1,
                    "title": "Mock issue",
                    "state": "opened",
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
                {
                    "id": 2,
                    "iid": 2,
                    "title": "Another issue",
                    "state": "opened",
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            ]
        )

    @route("POST", "/api/v4/projects/{id}/issues")
    async def create_issue(self, request, id="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": 3,
                "iid": 3,
                "title": "New issue",
                "state": "opened",
                "created_at": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/api/v4/projects/{id}/merge_requests", writes=False)
    async def list_merge_requests(self, request, id="", **kw):
        return MockResponse(
            body=[
                {
                    "id": 1,
                    "iid": 1,
                    "title": "Mock MR",
                    "state": "opened",
                    "source_branch": "feature",
                    "target_branch": "main",
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
            ]
        )

    @route("GET", "/api/v4/projects/{id}/pipelines", writes=False)
    async def list_pipelines(self, request, id="", **kw):
        return MockResponse(
            body=[
                {
                    "id": 1,
                    "status": "success",
                    "ref": "main",
                    "sha": "abc123_mock",
                    "created_at": "2024-03-14T12:00:00.000Z",
                },
                {
                    "id": 2,
                    "status": "pending",
                    "ref": "main",
                    "sha": "def456_mock",
                    "created_at": "2024-03-14T12:01:00.000Z",
                },
            ]
        )
