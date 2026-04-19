# CHANGELOG: https://help.gong.io/docs/release-notes  (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.gong.io/docs (API reference); OpenAPI via instance /ajax/settings/api/documentation/specs
# SANDBOX:   https://app.gong.io (Settings → API for credentials)
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Basic (ACCESS_KEY:ACCESS_SECRET) or Bearer token in Authorization header
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: Gong v2 covers calls, users, stats, CRM, library, and Engage flows; 13 endpoints kept in one file.
class GongMock(BaseMock):
    prefix = "/gong"
    spec_url = "https://help.gong.io/docs"
    sandbox_base = "https://api.gong.io"

    @route("GET", "/v2/calls", writes=False)
    async def list_calls(self, request, **kw):
        return MockResponse(
            body={
                "calls": [
                    {
                        "id": 1001,
                        "duration": 3600,
                        "parties": [
                            {"emailAddress": "alice@verifiabl.dev", "name": "Alice"},
                            {"emailAddress": "bob@verifiabl.dev", "name": "Bob"},
                        ],
                    },
                    {
                        "id": 1002,
                        "duration": 1800,
                        "parties": [
                            {"emailAddress": "alice@verifiabl.dev", "name": "Alice"},
                            {"emailAddress": "carol@verifiabl.dev", "name": "Carol"},
                        ],
                    },
                ],
            }
        )

    @route("GET", "/v2/calls/{id}", writes=False)
    async def get_call(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1001,
                "duration": 3600,
                "parties": [
                    {"emailAddress": "alice@verifiabl.dev", "name": "Alice"},
                    {"emailAddress": "bob@verifiabl.dev", "name": "Bob"},
                ],
            }
        )

    @route("GET", "/v2/calls/{id}/transcript", writes=False)
    async def get_transcript(self, request, id="", **kw):
        return MockResponse(
            body={
                "transcript": [
                    {
                        "speakerId": 1,
                        "sentences": [
                            {"text": "Hello, thanks for joining.", "start": 0, "end": 2000}
                        ],
                    },
                    {
                        "speakerId": 2,
                        "sentences": [
                            {"text": "Thanks for having me.", "start": 2100, "end": 3500}
                        ],
                    },
                ],
            }
        )

    @route("GET", "/v2/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "users": [
                    {
                        "id": 2001,
                        "emailAddress": "alice@verifiabl.dev",
                        "firstName": "Alice",
                        "lastName": "Smith",
                    },
                    {
                        "id": 2002,
                        "emailAddress": "bob@verifiabl.dev",
                        "firstName": "Bob",
                        "lastName": "Jones",
                    },
                ],
                "records": {
                    "totalRecords": 2,
                    "currentPageSize": 2,
                    "currentPageNumber": 0,
                    "cursor": None,
                },
            }
        )

    @route("GET", "/v2/users/{id}", writes=False)
    async def get_user(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 2001,
                "emailAddress": "alice@verifiabl.dev",
                "firstName": "Alice",
                "lastName": "Smith",
            }
        )

    @route("GET", "/v2/users/{id}/stats", writes=False)
    async def get_user_stats(self, request, id="", **kw):
        return MockResponse(
            body={
                "userId": int(id) if id.isdigit() else 2001,
                "callsCount": 42,
                "talkTimeSeconds": 7200,
            }
        )

    @route("GET", "/v2/stats/activity", writes=False)
    async def get_activity_stats(self, request, **kw):
        return MockResponse(
            body={
                "activities": [
                    {
                        "userId": 2001,
                        "callsCount": 42,
                        "fromDateTime": "2026-03-01T00:00:00Z",
                        "toDateTime": "2026-03-14T23:59:59Z",
                    },
                ],
            }
        )

    @route("POST", "/v2/crm/object")
    async def update_crm_object(self, request, **kw):
        return MockResponse(status=200, body={"requestId": "crm_mock_verifiabl"})

    @route("GET", "/v2/crm/integrations", writes=False)
    async def list_crm_integrations(self, request, **kw):
        return MockResponse(
            body={
                "integrations": [
                    {"id": "crm_int_mock_001", "type": "salesforce", "status": "active"},
                ],
            }
        )

    @route("GET", "/v2/library/folder/content", writes=False)
    async def list_library_folder_content(self, request, **kw):
        return MockResponse(
            body={
                "calls": [
                    {"id": 1001, "duration": 3600, "title": "Q1 review"},
                    {"id": 1002, "duration": 1800, "title": "Discovery"},
                ],
            }
        )

    @route("POST", "/v2/calls")
    async def add_call(self, request, **kw):
        return MockResponse(status=201, body={"requestId": "call_mock_verifiabl", "callId": 1003})

    @route("GET", "/v2/flows", writes=False)
    async def list_flows(self, request, **kw):
        return MockResponse(
            body={
                "flows": [
                    {"id": 3001, "name": "Outbound sequence", "visibility": "company"},
                    {"id": 3002, "name": "Follow-up", "visibility": "company"},
                ],
            }
        )

    @route("GET", "/v2/flows/folders", writes=False)
    async def list_flow_folders(self, request, **kw):
        return MockResponse(
            body={
                "folders": [
                    {"id": 4001, "name": "Enterprise", "flowCount": 5},
                    {"id": 4002, "name": "SMB", "flowCount": 3},
                ],
            }
        )
