# CHANGELOG: https://manual.bubble.io/core-resources/application-settings/versions  (no RSS/atom feed as of 2026-03)
# SPEC:      https://manual.bubble.io/core-resources/api/the-bubble-api/the-data-api/data-api-requests
# SANDBOX:   https://bubble.io (app-specific: https://yourapp.bubbleapps.io)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class BubbleMock(BaseMock):
    prefix = "/bubble"
    spec_url = (
        "https://manual.bubble.io/core-resources/api/the-bubble-api/the-data-api/data-api-requests"
    )
    sandbox_base = "https://yourapp.bubbleapps.io"

    @route("GET", "/api/1.1/obj/{type}", writes=False)
    async def list_things(self, request, type="", **kw):
        return MockResponse(
            body={
                "response": {
                    "cursor": 0,
                    "results": [
                        {
                            "_id": "1672236233855x229135430406542270",
                            "Created Date": "2022-12-28T11:03:11.097Z",
                            "Modified Date": "2022-12-30T11:03:11.097Z",
                            "Created By": "admin_user_mock",
                            "Unit name": "Unit A",
                            "Unit number": 1,
                        },
                        {
                            "_id": "1672236233856x330332849009372400",
                            "Created Date": "2022-12-28T11:03:11.098Z",
                            "Modified Date": "2022-12-30T11:03:11.098Z",
                            "Created By": "admin_user_mock",
                            "Unit name": "Unit B",
                            "Unit number": 2,
                        },
                    ],
                    "count": 2,
                    "remaining": 0,
                },
            }
        )

    @route("GET", "/api/1.1/obj/{type}/{id}", writes=False)
    async def get_thing(self, request, type="", id="", **kw):
        return MockResponse(
            body={
                "response": {
                    "_id": id or "1672236233855x229135430406542270",
                    "Created By": "admin_user_mock",
                    "Created Date": "2022-12-28T11:03:11.097Z",
                    "Modified Date": "2022-12-30T11:03:11.097Z",
                    "Unit name": "Unit A",
                    "Unit number": 1,
                },
            }
        )

    @route("POST", "/api/1.1/obj/{type}")
    async def create_thing(self, request, type="", **kw):
        return MockResponse(
            status=201, body={"status": "success", "id": "1672236233855x_mock_verifiabl"}
        )

    @route("PATCH", "/api/1.1/obj/{type}/{id}")
    async def update_thing(self, request, type="", id="", **kw):
        return MockResponse(status=204, body=None)

    @route("PUT", "/api/1.1/obj/{type}/{id}")
    async def replace_thing(self, request, type="", id="", **kw):
        return MockResponse(status=204, body=None)

    @route("DELETE", "/api/1.1/obj/{type}/{id}")
    async def delete_thing(self, request, type="", id="", **kw):
        return MockResponse(status=204, body=None)

    @route("POST", "/api/1.1/obj/{type}/bulk")
    async def bulk_create(self, request, type="", **kw):
        return MockResponse(
            body=[
                {"status": "success", "id": "1672396136196x_mock_001"},
                {"status": "success", "id": "1672396136197x_mock_002"},
            ]
        )
