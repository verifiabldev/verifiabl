# CHANGELOG: https://www.chatprd.ai/docs (no RSS/atom feed as of 2026-03)
# SPEC:      https://www.chatprd.ai/docs (no public OpenAPI — mock inferred from MCP document management)
# SANDBOX:   https://app.chatprd.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (Clerk-backed session per docs)
from mocks.base import BaseMock, route
from models import MockResponse


class ChatprdMock(BaseMock):
    prefix = "/chatprd"
    spec_url = "https://www.chatprd.ai/docs"
    sandbox_base = "https://api.chatprd.ai"

    @route("GET", "/v1/workspaces", writes=False)
    async def list_workspaces(self, request, **kw):
        return MockResponse(
            body={
                "workspaces": [
                    {"id": "ws_mock_001", "name": "Acme Product", "created_at": 1710400000},
                    {"id": "ws_mock_002", "name": "Beta Team", "created_at": 1710400100},
                ],
            }
        )

    @route("GET", "/v1/workspaces/{id}", writes=False)
    async def get_workspace(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "ws_mock_001",
                "name": "Acme Product",
                "created_at": 1710400000,
                "document_count": 3,
            }
        )

    @route("GET", "/v1/documents", writes=False)
    async def list_documents(self, request, **kw):
        return MockResponse(
            body={
                "documents": [
                    {
                        "id": "doc_mock_001",
                        "title": "API v2 PRD",
                        "workspace_id": "ws_mock_001",
                        "updated_at": 1710400000,
                    },
                    {
                        "id": "doc_mock_002",
                        "title": "Onboarding Spec",
                        "workspace_id": "ws_mock_001",
                        "updated_at": 1710401000,
                    },
                ],
            }
        )

    @route("GET", "/v1/documents/{id}", writes=False)
    async def get_document(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "doc_mock_001",
                "title": "API v2 PRD",
                "workspace_id": "ws_mock_001",
                "content": "## Overview\nThis PRD describes the API v2 rollout.",
                "updated_at": 1710400000,
            }
        )

    @route("POST", "/v1/documents")
    async def create_document(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "doc_mock_new",
                "title": "New Document",
                "workspace_id": "ws_mock_001",
                "updated_at": 1710400000,
            },
        )

    @route("PATCH", "/v1/documents/{id}")
    async def update_document(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "doc_mock_001",
                "title": "Updated Title",
                "updated_at": 1710400000,
            }
        )

    @route("GET", "/v1/templates", writes=False)
    async def list_templates(self, request, **kw):
        return MockResponse(
            body={
                "templates": [
                    {
                        "id": "tpl_mock_001",
                        "name": "PRD",
                        "description": "Product requirements document",
                    },
                    {
                        "id": "tpl_mock_002",
                        "name": "Technical Spec",
                        "description": "Technical specification",
                    },
                ],
            }
        )

    @route("GET", "/v1/templates/{id}", writes=False)
    async def get_template(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "tpl_mock_001",
                "name": "PRD",
                "description": "Product requirements document",
                "sections": ["Overview", "Goals", "Requirements", "Success Metrics"],
            }
        )
