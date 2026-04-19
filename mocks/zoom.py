# CHANGELOG: https://developers.zoom.us/changelog/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/zoom/api (openapi.v2.json)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class ZoomMock(BaseMock):
    prefix = "/zoom"
    spec_url = "https://github.com/zoom/api"
    sandbox_base = "https://api.zoom.us"

    @route("GET", "/v2/users/me")
    async def me(self, request, **kw):
        return MockResponse(
            body={"id": "mock_user", "email": "mock@verifiabl.dev", "type": 1, "first_name": "Mock"}
        )

    @route("GET", "/v2/users/me/meetings")
    async def list_meetings(self, request, **kw):
        return MockResponse(
            body={"meetings": [{"id": 1234567890, "topic": "Mock Meeting", "type": 2}]}
        )

    @route("POST", "/v2/users/me/meetings")
    async def create_meeting(self, request, **kw):
        return MockResponse(
            status=201,
            body={"id": 9876543210, "topic": "New Meeting", "join_url": "https://zoom.us/j/mock"},
        )
