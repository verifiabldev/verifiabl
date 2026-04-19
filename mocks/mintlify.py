# CHANGELOG: https://mintlify.com/docs/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://www.mintlify.com/docs/api/introduction
# SANDBOX:   https://dashboard.mintlify.com
# SKILL:     —
# MCP:       —
# LLMS:      https://mintlify.com/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class MintlifyMock(BaseMock):
    prefix = "/mintlify"
    spec_url = "https://www.mintlify.com/docs/api/introduction"
    sandbox_base = "https://api.mintlify.com"

    @route("POST", "/v1/project/update/{projectId}")
    async def trigger_update(self, request, projectId="", **kw):
        return MockResponse(status=202, body={"statusId": "status_mock_verifiabl"})

    @route("GET", "/v1/project/update-status/{statusId}", writes=False)
    async def get_update_status(self, request, statusId="", **kw):
        return MockResponse(
            body={
                "_id": statusId or "status_mock_verifiabl",
                "projectId": "proj_mock_001",
                "createdAt": "2026-03-14T12:00:00.000Z",
                "endedAt": "2026-03-14T12:01:00.000Z",
                "status": "success",
                "summary": "Deployment completed",
                "logs": ["Building...", "Deployed."],
                "subdomain": "docs",
                "source": "api",
                "commit": {
                    "sha": "abc123",
                    "ref": "main",
                    "message": "Update docs",
                    "filesChanged": {"added": [], "modified": ["intro.mdx"], "removed": []},
                },
            }
        )

    @route("GET", "/v1/agent/{projectId}/jobs", writes=False)
    async def list_agent_jobs(self, request, projectId="", **kw):
        return MockResponse(
            body={
                "allSessions": [
                    {
                        "sessionId": "sess_mock_001",
                        "subdomain": "docs",
                        "branch": "agent-edit-001",
                        "haulted": True,
                        "haultReason": "completed",
                        "pullRequestLink": "https://github.com/org/repo/pull/1",
                        "messageToUser": "PR created",
                        "todos": [],
                        "userId": "user_001",
                        "title": "Add API section",
                        "createdAt": "2026-03-14T12:00:00.000Z",
                    },
                ],
            }
        )

    @route("GET", "/v1/agent/{projectId}/job/{id}", writes=False)
    async def get_agent_job(self, request, projectId="", id="", **kw):
        return MockResponse(
            body={
                "sessionId": id or "sess_mock_001",
                "subdomain": "docs",
                "branch": "agent-edit-001",
                "haulted": True,
                "haultReason": "completed",
                "pullRequestLink": "https://github.com/org/repo/pull/1",
                "messageToUser": "PR created",
                "todos": [
                    {
                        "id": "todo_1",
                        "content": "Edit intro",
                        "status": "completed",
                        "priority": "high",
                    }
                ],
                "userId": "user_001",
                "title": "Add API section",
                "createdAt": "2026-03-14T12:00:00.000Z",
            }
        )

    @route("POST", "/v1/agent/{projectId}/job")
    async def create_agent_job(self, request, projectId="", **kw):
        return MockResponse(body={"sessionId": "sess_mock_new"})

    @route("GET", "/v1/analytics/{projectId}/feedback", writes=False)
    async def get_feedback(self, request, projectId="", **kw):
        return MockResponse(
            body={
                "feedback": [
                    {
                        "id": "fb_mock_001",
                        "path": "/intro",
                        "comment": "Helpful",
                        "createdAt": "2026-03-14T12:00:00.000Z",
                        "source": "contextual",
                        "status": "resolved",
                        "helpful": True,
                        "contact": None,
                    },
                ],
                "nextCursor": None,
                "hasMore": False,
            }
        )

    @route("GET", "/v1/analytics/{projectId}/assistant", writes=False)
    async def get_assistant_conversations(self, request, projectId="", **kw):
        return MockResponse(
            body={
                "conversations": [
                    {
                        "id": "conv_mock_001",
                        "timestamp": "2026-03-14T12:00:00.000Z",
                        "query": "How do I get started?",
                        "response": "See the quickstart.",
                        "sources": [
                            {"title": "Quickstart", "url": "https://docs.mintlify.app/quickstart"}
                        ],
                        "queryCategory": "getting-started",
                    },
                ],
                "nextCursor": None,
                "hasMore": False,
            }
        )

    @route("POST", "/discovery/v1/search/{domain}", writes=False)
    async def search_docs(self, request, domain="", **kw):
        return MockResponse(
            body=[
                {"content": "Get started with the API.", "path": "/intro", "metadata": {}},
                {"content": "Authentication uses Bearer tokens.", "path": "/auth", "metadata": {}},
            ]
        )

    @route("POST", "/discovery/v1/assistant/{domain}/message")
    async def create_assistant_message(self, request, domain="", **kw):
        return MockResponse(
            body={"message": "See the quickstart guide for setup.", "threadId": "thread_mock_001"}
        )
