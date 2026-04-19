# CHANGELOG: https://developer.monday.com/api-reference/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.monday.com/api-reference
# SANDBOX:   https://developer.monday.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class MondayMock(BaseMock):
    prefix = "/monday"
    spec_url = "https://developer.monday.com/api-reference"
    sandbox_base = "https://api.monday.com"

    @route("POST", "/v2", writes=True)
    async def graphql(self, request, **kw):
        body = {
            "data": {
                "boards": [
                    {"id": "12345678", "name": "My Amazing CRM Board", "board_kind": "public"},
                    {"id": "12345679", "name": "Sprint Board", "board_kind": "public"},
                ],
                "items": [
                    {"id": "item_mock_001", "name": "Lead: Acme Corp", "state": "active"},
                    {"id": "item_mock_002", "name": "Lead: Globex", "state": "active"},
                ],
            },
            "account_id": 98765,
        }
        return MockResponse(body=body)
