# CHANGELOG: https://developer.box.com/changelog  (no RSS/atom feed as of 2026-03)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class BoxMock(BaseMock):
    prefix = "/box"
    spec_url = "https://github.com/box/box-openapi"
    sandbox_base = "https://api.box.com"

    @route("GET", "/2.0/users/me")
    async def me(self, request, **kw):
        return MockResponse(
            body={"id": "1", "type": "user", "name": "Mock User", "login": "mock@verifiabl.dev"}
        )

    @route("GET", "/2.0/folders/{id}")
    async def get_folder(self, request, id="0", **kw):
        return MockResponse(
            body={
                "id": id,
                "type": "folder",
                "name": "Mock Folder",
                "item_collection": {"total_count": 0, "entries": []},
            }
        )

    @route("POST", "/2.0/folders")
    async def create_folder(self, request, **kw):
        return MockResponse(status=201, body={"id": "42", "type": "folder", "name": "New Folder"})
