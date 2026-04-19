# CHANGELOG: https://loops.so/docs/api-reference/changelog
# SPEC:      https://app.loops.so/openapi.json
# SANDBOX:   https://app.loops.so/settings?page=api
# SKILL:     —
# MCP:       —
# LLMS:      https://loops.so/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class LoopsMock(BaseMock):
    prefix = "/loops"
    spec_url = "https://app.loops.so/openapi.json"
    sandbox_base = "https://app.loops.so/api/v1"

    @route("GET", "/api/v1/api-key", writes=False)
    async def test_api_key(self, request, **kw):
        return MockResponse(body={"success": True, "teamName": "verifiabl"})

    @route("POST", "/api/v1/contacts/create")
    async def create_contact(self, request, **kw):
        return MockResponse(body={"success": True, "id": "contact_mock_verifiabl"})

    @route("PUT", "/api/v1/contacts/update")
    async def update_contact(self, request, **kw):
        return MockResponse(body={"success": True, "id": "contact_mock_verifiabl"})

    @route("GET", "/api/v1/contacts/find", writes=False)
    async def find_contact(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "contact_mock_001",
                    "email": "alice@verifiabl.dev",
                    "firstName": "Alice",
                    "lastName": "Verifiabl",
                    "source": "api",
                    "subscribed": True,
                    "userGroup": "",
                    "userId": None,
                    "mailingLists": {},
                    "optInStatus": "accepted",
                }
            ]
        )

    @route("POST", "/api/v1/contacts/delete")
    async def delete_contact(self, request, **kw):
        return MockResponse(body={"success": True, "message": "Contact deleted."})

    @route("GET", "/api/v1/contacts/properties", writes=False)
    async def list_contact_properties(self, request, **kw):
        return MockResponse(
            body=[
                {"key": "firstName", "label": "First name", "type": "string"},
                {"key": "planName", "label": "Plan name", "type": "string"},
            ]
        )

    @route("POST", "/api/v1/contacts/properties")
    async def create_contact_property(self, request, **kw):
        return MockResponse(body={"success": True})

    @route("GET", "/api/v1/lists", writes=False)
    async def list_mailing_lists(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "list_mock_001",
                    "name": "Main list",
                    "description": "Primary audience",
                    "isPublic": True,
                },
                {
                    "id": "list_mock_002",
                    "name": "Newsletter",
                    "description": "Weekly digest",
                    "isPublic": False,
                },
            ]
        )

    @route("POST", "/api/v1/events/send")
    async def send_event(self, request, **kw):
        return MockResponse(body={"success": True})

    @route("POST", "/api/v1/transactional")
    async def send_transactional(self, request, **kw):
        return MockResponse(body={"success": True})

    @route("GET", "/api/v1/transactional", writes=False)
    async def list_transactional(self, request, **kw):
        return MockResponse(
            body={
                "pagination": {
                    "totalResults": 2,
                    "returnedResults": 2,
                    "perPage": 20,
                    "totalPages": 1,
                    "nextCursor": None,
                    "nextPage": None,
                },
                "data": [
                    {
                        "id": "txn_mock_001",
                        "name": "Welcome email",
                        "lastUpdated": "2025-02-02T02:56:28.845Z",
                        "dataVariables": ["name"],
                    },
                    {
                        "id": "txn_mock_002",
                        "name": "Password reset",
                        "lastUpdated": "2025-02-01T12:00:00.000Z",
                        "dataVariables": ["resetLink"],
                    },
                ],
            }
        )
