# CHANGELOG: https://developers.ops.ringcentral.com/guide/basics/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/grokify/ringcentral-postman (ringcentral-api_spec_openapi2.yaml)
# SANDBOX:   https://developers.ringcentral.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class RingCentralMock(BaseMock):
    prefix = "/ringcentral"
    spec_url = "https://github.com/grokify/ringcentral-postman"
    sandbox_base = "https://platform.ringcentral.com"

    @route("GET", "/restapi/v1.0/account/{accountId}", writes=False)
    async def get_account(self, request, accountId="", **kw):
        return MockResponse(
            body={
                "id": accountId or "1",
                "status": "Confirmed",
                "serviceInfo": {"brand": {"name": "RingCentral"}},
            }
        )

    @route("GET", "/restapi/v1.0/account/{accountId}/extension", writes=False)
    async def list_extensions(self, request, accountId="", **kw):
        return MockResponse(
            body={
                "records": [
                    {"id": "1", "extensionNumber": "101", "status": "Enabled", "type": "User"},
                    {"id": "2", "extensionNumber": "102", "status": "Enabled", "type": "User"},
                ],
                "paging": {"page": 1, "totalPages": 1, "perPage": 100},
                "navigation": {"firstPage": {"uri": "..."}, "nextPage": None},
            }
        )

    @route("GET", "/restapi/v1.0/account/{accountId}/extension/{extensionId}", writes=False)
    async def get_extension(self, request, accountId="", extensionId="", **kw):
        return MockResponse(
            body={
                "id": extensionId or "1",
                "extensionNumber": "101",
                "status": "Enabled",
                "type": "User",
            }
        )

    @route(
        "GET", "/restapi/v1.0/account/{accountId}/extension/{extensionId}/call-log", writes=False
    )
    async def list_call_log(self, request, accountId="", extensionId="", **kw):
        return MockResponse(
            body={
                "records": [
                    {
                        "id": "call_mock_001",
                        "sessionId": "session_mock_001",
                        "from": {"phoneNumber": "+15551234567"},
                        "to": {"phoneNumber": "+15559876543"},
                        "type": "Voice",
                        "direction": "Outbound",
                        "startTime": "2024-03-10T18:07:52.534Z",
                        "duration": 120,
                        "action": "Phone Call",
                        "legs": [],
                    },
                ],
                "paging": {"page": 1, "totalPages": 1, "perPage": 100},
                "navigation": {"firstPage": {"uri": "..."}, "nextPage": None},
            }
        )

    @route(
        "GET",
        "/restapi/v1.0/account/{accountId}/extension/{extensionId}/message-store",
        writes=False,
    )
    async def list_messages(self, request, accountId="", extensionId="", **kw):
        return MockResponse(
            body={
                "records": [
                    {
                        "id": "msg_mock_001",
                        "type": "SMS",
                        "availability": "Alive",
                        "direction": "Outbound",
                    },
                    {
                        "id": "msg_mock_002",
                        "type": "SMS",
                        "availability": "Alive",
                        "direction": "Inbound",
                    },
                ],
                "paging": {"page": 1, "totalPages": 1, "perPage": 100},
                "navigation": {"firstPage": {"uri": "..."}, "nextPage": None},
            }
        )

    @route("POST", "/restapi/v1.0/account/{accountId}/extension/{extensionId}/sms")
    async def send_sms(self, request, accountId="", extensionId="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "msg_mock_new",
                "uri": "/restapi/v1.0/account/~/extension/~/message-store/msg_mock_new",
                "type": "SMS",
                "availability": "Alive",
                "to": [{"phoneNumber": "+15551234567"}],
            },
        )
