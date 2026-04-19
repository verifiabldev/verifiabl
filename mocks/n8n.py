# CHANGELOG: https://github.com/n8n-io/n8n/releases.atom
# SPEC:      https://github.com/n8n-io/n8n-docs/blob/main/docs/api/v1/openapi.yml
# SANDBOX:   https://app.n8n.io
# SKILL:     —
# MCP:       https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class N8nMock(BaseMock):
    prefix = "/n8n"
    spec_url = "https://github.com/n8n-io/n8n-docs/blob/main/docs/api/v1/openapi.yml"
    sandbox_base = "https://app.n8n.io"

    @route("GET", "/api/v1/workflows", writes=False)
    async def list_workflows(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "wf_mock_001",
                        "name": "Sync to Slack",
                        "active": False,
                        "nodes": [],
                        "connections": {},
                        "settings": {},
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "wf_mock_002",
                        "name": "Daily Report",
                        "active": True,
                        "nodes": [],
                        "connections": {},
                        "settings": {},
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "nextCursor": None,
            }
        )

    @route("POST", "/api/v1/workflows")
    async def create_workflow(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "wf_mock_new",
                "name": "New Workflow",
                "active": False,
                "nodes": [],
                "connections": {},
                "settings": {},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "updatedAt": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/api/v1/workflows/{id}", writes=False)
    async def get_workflow(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "wf_mock_001",
                "name": "Sync to Slack",
                "active": False,
                "nodes": [],
                "connections": {},
                "settings": {},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "updatedAt": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("PATCH", "/api/v1/workflows/{id}")
    async def update_workflow(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "wf_mock_001",
                "name": "Updated Workflow",
                "active": False,
                "nodes": [],
                "connections": {},
                "settings": {},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "updatedAt": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("GET", "/api/v1/executions", writes=False)
    async def list_executions(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": 1000,
                        "finished": True,
                        "mode": "manual",
                        "status": "success",
                        "startedAt": "2024-03-14T12:00:00.000Z",
                        "stoppedAt": "2024-03-14T12:00:05.000Z",
                        "workflowId": "wf_mock_001",
                    },
                    {
                        "id": 1001,
                        "finished": True,
                        "mode": "webhook",
                        "status": "success",
                        "startedAt": "2024-03-14T12:01:00.000Z",
                        "stoppedAt": "2024-03-14T12:01:02.000Z",
                        "workflowId": "wf_mock_001",
                    },
                ],
                "nextCursor": None,
            }
        )

    @route("GET", "/api/v1/executions/{id}", writes=False)
    async def get_execution(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1000,
                "finished": True,
                "mode": "manual",
                "status": "success",
                "startedAt": "2024-03-14T12:00:00.000Z",
                "stoppedAt": "2024-03-14T12:00:05.000Z",
                "workflowId": "wf_mock_001",
            }
        )

    @route("POST", "/api/v1/executions/{id}/retry")
    async def retry_execution(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1000,
                "finished": False,
                "mode": "retry",
                "status": "running",
                "startedAt": "2024-03-14T12:00:00.000Z",
                "stoppedAt": None,
                "workflowId": "wf_mock_001",
            }
        )

    @route("GET", "/api/v1/credentials", writes=False)
    async def list_credentials(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "cred_mock_001",
                        "name": "Slack API",
                        "type": "slackApi",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                        "shared": [],
                    },
                    {
                        "id": "cred_mock_002",
                        "name": "GitHub Token",
                        "type": "githubApi",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                        "shared": [],
                    },
                ],
                "nextCursor": None,
            }
        )

    @route("POST", "/api/v1/credentials")
    async def create_credential(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "cred_mock_new",
                "name": "New Credential",
                "type": "githubApi",
                "createdAt": "2024-03-14T12:00:00.000Z",
                "updatedAt": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/api/v1/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "usr_mock_001",
                        "email": "admin@verifiabl.dev",
                        "firstName": "Admin",
                        "lastName": "User",
                        "role": "global:owner",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "usr_mock_002",
                        "email": "member@verifiabl.dev",
                        "firstName": "Member",
                        "lastName": "User",
                        "role": "global:member",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "nextCursor": None,
            }
        )

    @route("GET", "/api/v1/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "proj_mock_001",
                        "name": "Default",
                        "type": "personal",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                        "updatedAt": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "nextCursor": None,
            }
        )

    @route("GET", "/api/v1/tags", writes=False)
    async def list_tags(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "tag_mock_001",
                        "name": "production",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "tag_mock_002",
                        "name": "staging",
                        "createdAt": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "nextCursor": None,
            }
        )
