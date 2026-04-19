# CHANGELOG: https://developer.atlassian.com/cloud/jira/platform/changelog/
# SPEC:      https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json
# SANDBOX:   https://developer.atlassian.com/cloud/jira/platform/getting-started/
# SKILL:     —
# MCP:       https://mcp.atlassian.com/v1/mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class AtlassianMock(BaseMock):
    prefix = "/atlassian"
    spec_url = "https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json"
    sandbox_base = "https://your-domain.atlassian.net"

    @route("GET", "/rest/api/3/myself", writes=False)
    async def myself(self, request, **kw):
        return MockResponse(
            body={
                "accountId": "mock123",
                "displayName": "Mock User",
                "emailAddress": "mock@verifiabl.dev",
            }
        )

    @route("GET", "/rest/api/3/search", writes=False)
    async def search_issues(self, request, **kw):
        return MockResponse(
            body={
                "total": 2,
                "issues": [
                    {
                        "id": "10001",
                        "key": "MOCK-1",
                        "self": "https://verifiabl.dev/atlassian/rest/api/3/issue/10001",
                        "fields": {"summary": "Mock issue one", "status": {"name": "To Do"}},
                    },
                    {
                        "id": "10002",
                        "key": "MOCK-2",
                        "self": "https://verifiabl.dev/atlassian/rest/api/3/issue/10002",
                        "fields": {"summary": "Mock issue two", "status": {"name": "In Progress"}},
                    },
                ],
            }
        )

    @route("GET", "/rest/api/3/issue/{issueIdOrKey}", writes=False)
    async def get_issue(self, request, issueIdOrKey="", **kw):
        return MockResponse(
            body={
                "id": "10001",
                "key": issueIdOrKey or "MOCK-1",
                "self": f"https://verifiabl.dev/atlassian/rest/api/3/issue/{issueIdOrKey or 'MOCK-1'}",
                "fields": {
                    "summary": "Mock issue",
                    "status": {"id": "1", "name": "To Do"},
                    "issuetype": {"name": "Task"},
                    "project": {"key": "MOCK", "name": "Mock Project"},
                },
            }
        )

    @route("GET", "/rest/api/3/project", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "1",
                    "key": "MOCK",
                    "name": "Mock Project",
                    "self": "https://verifiabl.dev/atlassian/rest/api/3/project/1",
                },
                {
                    "id": "2",
                    "key": "DEMO",
                    "name": "Demo Project",
                    "self": "https://verifiabl.dev/atlassian/rest/api/3/project/2",
                },
            ]
        )

    @route("GET", "/rest/api/3/project/{projectIdOrKey}", writes=False)
    async def get_project(self, request, projectIdOrKey="", **kw):
        return MockResponse(
            body={
                "id": projectIdOrKey or "1",
                "key": "MOCK",
                "name": "Mock Project",
                "self": f"https://verifiabl.dev/atlassian/rest/api/3/project/{projectIdOrKey or '1'}",
            }
        )

    @route("GET", "/rest/api/3/status", writes=False)
    async def list_statuses(self, request, **kw):
        return MockResponse(
            body=[
                {"id": "1", "name": "To Do", "statusCategory": {"key": "new"}},
                {"id": "2", "name": "In Progress", "statusCategory": {"key": "indeterminate"}},
                {"id": "3", "name": "Done", "statusCategory": {"key": "done"}},
            ]
        )

    @route("GET", "/rest/api/3/issue/{issueIdOrKey}/comment", writes=False)
    async def get_comments(self, request, issueIdOrKey="", **kw):
        return MockResponse(
            body={
                "comments": [
                    {
                        "id": "10101",
                        "body": {
                            "type": "doc",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "First comment"}],
                                }
                            ],
                        },
                        "author": {"displayName": "Mock User"},
                        "created": "2024-03-14T12:00:00.000+0000",
                    },
                    {
                        "id": "10102",
                        "body": {
                            "type": "doc",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Second comment"}],
                                }
                            ],
                        },
                        "author": {"displayName": "Mock User"},
                        "created": "2024-03-14T13:00:00.000+0000",
                    },
                ],
                "total": 2,
            }
        )

    @route("POST", "/rest/api/3/issue")
    async def create_issue(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "10003",
                "key": "MOCK-3",
                "self": "https://verifiabl.dev/atlassian/rest/api/3/issue/10003",
            },
        )

    @route("PUT", "/rest/api/3/issue/{issueIdOrKey}")
    async def update_issue(self, request, issueIdOrKey="", **kw):
        return MockResponse(status=204, body=None)

    @route("POST", "/rest/api/3/issue/{issueIdOrKey}/comment")
    async def add_comment(self, request, issueIdOrKey="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "10103",
                "body": {
                    "type": "doc",
                    "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "New comment"}]}
                    ],
                },
                "author": {"displayName": "Mock User"},
                "created": "2024-03-14T14:00:00.000+0000",
            },
        )
