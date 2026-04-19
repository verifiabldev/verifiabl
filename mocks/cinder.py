# CHANGELOG: https://www.cinder.co/blog-posts (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.cinder.co (access gated; mock inferred from Trust & Safety domain)
# SANDBOX:   https://app.cinder.co
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class CinderMock(BaseMock):
    prefix = "/cinder"
    spec_url = "https://docs.cinder.co"
    sandbox_base = "https://api.cinder.co"

    @route("GET", "/v1/queues", writes=False)
    async def list_queues(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "que_mock_001",
                        "name": "Content Review",
                        "status": "active",
                        "item_count": 12,
                    },
                    {
                        "id": "que_mock_002",
                        "name": "Escalations",
                        "status": "active",
                        "item_count": 3,
                    },
                ],
                "next_cursor": None,
            }
        )

    @route("GET", "/v1/queues/{id}", writes=False)
    async def get_queue(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "que_mock_001",
                "name": "Content Review",
                "status": "active",
                "policy_id": "pol_mock_001",
                "created_at": 1710400000,
            }
        )

    @route("GET", "/v1/queues/{id}/items", writes=False)
    async def list_queue_items(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "item_mock_001",
                        "content_id": "cnt_001",
                        "status": "pending",
                        "submitted_at": 1710400000,
                    },
                    {
                        "id": "item_mock_002",
                        "content_id": "cnt_002",
                        "status": "pending",
                        "submitted_at": 1710400001,
                    },
                ],
                "next_cursor": None,
            }
        )

    @route("GET", "/v1/items/{id}", writes=False)
    async def get_item(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "item_mock_001",
                "content_id": "cnt_001",
                "queue_id": "que_mock_001",
                "status": "pending",
                "submitted_at": 1710400000,
                "labels": [],
            }
        )

    @route("POST", "/v1/items")
    async def submit_item(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "item_mock_verifiabl",
                "content_id": "cnt_verifiabl",
                "queue_id": "que_mock_001",
                "status": "pending",
                "submitted_at": 1710400000,
            },
        )

    @route("GET", "/v1/policies", writes=False)
    async def list_policies(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "pol_mock_001", "name": "Community Standards", "updated_at": 1710400000},
                    {"id": "pol_mock_002", "name": "Safety Escalation", "updated_at": 1710400000},
                ],
            }
        )

    @route("GET", "/v1/policies/{id}", writes=False)
    async def get_policy(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "pol_mock_001",
                "name": "Community Standards",
                "rules": [],
                "updated_at": 1710400000,
            }
        )

    @route("GET", "/v1/labels", writes=False)
    async def list_labels(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "lbl_mock_001", "name": "safe", "category": "verdict"},
                    {"id": "lbl_mock_002", "name": "escalate", "category": "action"},
                ],
            }
        )

    @route("POST", "/v1/queues/{id}/items/{item_id}/resolve")
    async def resolve_item(self, request, id="", item_id="", **kw):
        return MockResponse(
            body={
                "id": item_id or "item_mock_001",
                "status": "resolved",
                "resolved_at": 1710400000,
            }
        )

    @route("GET", "/v1/workflows", writes=False)
    async def list_workflows(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "wf_mock_001", "name": "Default Triage", "enabled": True},
                    {"id": "wf_mock_002", "name": "Escalation Path", "enabled": True},
                ],
            }
        )
