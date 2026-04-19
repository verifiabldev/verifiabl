# CHANGELOG: https://developers.notion.com/page/changelog  (no RSS/atom feed)
# SPEC:      https://developers.notion.com/reference
# SANDBOX:   https://www.notion.so/my-integrations
# SKILL:     —
# MCP:       https://developers.notion.com/docs/get-started-with-mcp
# LLMS:      —
# AUTH:      Bearer token in Authorization header; Notion-Version header (per docs)
from mocks.base import BaseMock, route
from models import MockResponse


class NotionMock(BaseMock):
    # LOC EXCEPTION: Notion list/single responses require object/type/results envelope per spec; 10 endpoints for core workflow.
    prefix = "/notion"
    spec_url = "https://developers.notion.com/reference"
    sandbox_base = "https://api.notion.com"

    @route("GET", "/v1/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "type": "user",
                "user": {},
                "results": [
                    {
                        "id": "user_mock_001",
                        "object": "user",
                        "name": "Mock User",
                        "avatar_url": None,
                        "type": "person",
                        "person": {"email": "mock@verifiabl.dev"},
                    },
                    {
                        "id": "user_mock_002",
                        "object": "user",
                        "name": "Bot",
                        "avatar_url": None,
                        "type": "bot",
                        "bot": {},
                    },
                ],
                "next_cursor": None,
                "has_more": False,
            }
        )

    @route("GET", "/v1/users/{user_id}", writes=False)
    async def get_user(self, request, user_id="", **kw):
        return MockResponse(
            body={
                "id": user_id or "user_mock_001",
                "object": "user",
                "name": "Mock User",
                "avatar_url": None,
                "type": "person",
                "person": {"email": "mock@verifiabl.dev"},
            }
        )

    @route("GET", "/v1/databases/{database_id}", writes=False)
    async def get_database(self, request, database_id="", **kw):
        return MockResponse(
            body={
                "id": database_id or "db_mock_001",
                "object": "database",
                "title": [{"type": "text", "text": {"content": "Mock DB"}}],
                "properties": {"Name": {"title": {}}},
            }
        )

    @route("POST", "/v1/databases/{database_id}/query", writes=False)
    async def query_database(self, request, database_id="", **kw):
        return MockResponse(
            body={
                "object": "list",
                "type": "page",
                "results": [
                    {
                        "id": "page_mock_001",
                        "object": "page",
                        "properties": {"Name": {"title": [{"plain_text": "Entry 1"}]}},
                    },
                    {
                        "id": "page_mock_002",
                        "object": "page",
                        "properties": {"Name": {"title": [{"plain_text": "Entry 2"}]}},
                    },
                ],
                "next_cursor": None,
                "has_more": False,
            }
        )

    @route("GET", "/v1/pages/{page_id}", writes=False)
    async def get_page(self, request, page_id="", **kw):
        return MockResponse(
            body={
                "id": page_id or "page_mock_001",
                "object": "page",
                "created_time": "2024-03-14T12:00:00.000Z",
                "last_edited_time": "2024-03-14T12:00:00.000Z",
                "properties": {"title": {"title": [{"plain_text": "Mock Page"}]}},
            }
        )

    @route("POST", "/v1/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "type": "page_or_data_source",
                "page_or_data_source": {},
                "results": [
                    {
                        "id": "page_mock_001",
                        "object": "page",
                        "properties": {"title": {"title": [{"plain_text": "Mock Page"}]}},
                    },
                ],
                "next_cursor": None,
                "has_more": False,
            }
        )

    @route("POST", "/v1/pages")
    async def create_page(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "page_mock_new",
                "object": "page",
                "created_time": "2024-03-14T12:00:00.000Z",
                "last_edited_time": "2024-03-14T12:00:00.000Z",
                "properties": {"title": {"title": [{"plain_text": "New Page"}]}},
            },
        )

    @route("PATCH", "/v1/pages/{page_id}")
    async def update_page(self, request, page_id="", **kw):
        return MockResponse(
            body={
                "id": page_id or "page_mock_001",
                "object": "page",
                "created_time": "2024-03-14T12:00:00.000Z",
                "last_edited_time": "2024-03-14T12:00:00.000Z",
                "properties": {"title": {"title": [{"plain_text": "Updated Page"}]}},
            }
        )

    @route("GET", "/v1/blocks/{block_id}/children", writes=False)
    async def get_block_children(self, request, block_id="", **kw):
        return MockResponse(
            body={
                "object": "list",
                "type": "block",
                "results": [
                    {
                        "id": "block_mock_001",
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"plain_text": "Mock content"}]},
                    },
                ],
                "next_cursor": None,
                "has_more": False,
            }
        )

    @route("POST", "/v1/blocks/{block_id}/children")
    async def append_block_children(self, request, block_id="", **kw):
        return MockResponse(
            body={
                "object": "list",
                "type": "block",
                "results": [
                    {
                        "id": "block_mock_new",
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"plain_text": "Appended"}]},
                    },
                ],
                "next_cursor": None,
                "has_more": False,
            }
        )
