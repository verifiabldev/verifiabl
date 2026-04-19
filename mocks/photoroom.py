# CHANGELOG: https://docs.photoroom.com/getting-started/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://image-api.photoroom.com/openapi
# SANDBOX:   https://app.photoroom.com/api-dashboard
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      x-api-key header (per OpenAPI securitySchemes)
import base64
from mocks.base import BaseMock, route
from models import MockResponse

_MOCK_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class PhotoroomMock(BaseMock):
    prefix = "/photoroom"
    spec_url = "https://image-api.photoroom.com/openapi"
    sandbox_base = "https://image-api.photoroom.com"

    @route("GET", "/v2/account", writes=False)
    async def account_v2(self, request, **kw):
        return MockResponse(
            body={"images": {"available": 100, "subscription": 100}, "plan": "basic"}
        )

    @route("GET", "/v1/account", writes=False)
    async def account_v1(self, request, **kw):
        return MockResponse(body={"credits": {"available": 100, "subscription": 100}})

    @route("GET", "/v2/edit", writes=False)
    async def edit_get(self, request, **kw):
        return MockResponse(body=_MOCK_PNG, content_type="image/png")

    @route("POST", "/v2/edit")
    async def edit_post(self, request, **kw):
        return MockResponse(body=_MOCK_PNG, content_type="image/png")

    @route("POST", "/v1/segment")
    async def segment(self, request, **kw):
        return MockResponse(body={"base64img": base64.b64encode(_MOCK_PNG).decode()})

    @route("GET", "/v1/render", writes=False)
    async def render_get(self, request, **kw):
        return MockResponse(body=_MOCK_PNG, content_type="image/png")
