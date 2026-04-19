# CHANGELOG: https://developers.miro.com/changelog  (no RSS/atom feed found as of 2026-03)
# SPEC:      https://github.com/miroapp/api-clients/blob/main/packages/generator/spec.json
# SANDBOX:   https://miro.com/app/dashboard/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class MiroMock(BaseMock):
    prefix = "/miro"
    spec_url = "https://github.com/miroapp/api-clients/blob/main/packages/generator/spec.json"
    sandbox_base = "https://api.miro.com"

    @route("GET", "/v2/boards", writes=False)
    async def list_boards(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "uXjV_mock_001",
                        "name": "Mock Board",
                        "description": "Sample",
                        "type": "board",
                    },
                    {
                        "id": "uXjV_mock_002",
                        "name": "Second Board",
                        "description": "",
                        "type": "board",
                    },
                ],
                "total": 2,
                "size": 2,
                "offset": 0,
                "limit": 20,
            }
        )

    @route("POST", "/v2/boards")
    async def create_board(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "uXjV_mock_new",
                "name": "New Board",
                "description": "",
                "type": "board",
                "viewLink": "https://miro.com/app/board/uXjV_mock_new",
                "createdAt": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/v2/boards/{board_id}", writes=False)
    async def get_board(self, request, board_id="", **kw):
        return MockResponse(
            body={
                "id": board_id,
                "name": "Mock Board",
                "description": "Sample board description",
                "type": "board",
                "viewLink": "https://miro.com/app/board/" + board_id,
                "createdAt": "2024-03-14T12:00:00.000Z",
                "modifiedAt": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("PATCH", "/v2/boards/{board_id}")
    async def update_board(self, request, board_id="", **kw):
        return MockResponse(
            body={
                "id": board_id,
                "name": "Updated Board",
                "description": "",
                "type": "board",
                "viewLink": "https://miro.com/app/board/" + board_id,
            }
        )

    @route("GET", "/v2/boards/{board_id}/items", writes=False)
    async def list_items(self, request, board_id="", **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "3458764517517819001", "type": "sticky_note"},
                    {"id": "3458764517517819002", "type": "shape"},
                ],
                "total": 2,
                "size": 2,
                "cursor": "MzQ1ODc2NDUyMjQ5MDA4Mjg5NX4=",
                "limit": 10,
            }
        )

    @route("GET", "/v2/boards/{board_id}/items/{item_id}", writes=False)
    async def get_item(self, request, board_id="", item_id="", **kw):
        return MockResponse(
            body={
                "id": item_id,
                "type": "sticky_note",
                "data": {"content": "Mock note content"},
                "position": {"x": 0, "y": 0},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "modifiedAt": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("POST", "/v2/boards/{board_id}/sticky_notes")
    async def create_sticky_note(self, request, board_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "3458764517517819010",
                "type": "sticky_note",
                "data": {"content": "New sticky note"},
                "style": {"fillColor": "light_yellow"},
                "position": {"x": 0, "y": 0},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "modifiedAt": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/v2/boards/{board_id}/sticky_notes/{item_id}", writes=False)
    async def get_sticky_note(self, request, board_id="", item_id="", **kw):
        return MockResponse(
            body={
                "id": item_id,
                "type": "sticky_note",
                "data": {"content": "Mock sticky content"},
                "style": {"fillColor": "light_yellow", "textAlign": "left"},
                "position": {"x": 0, "y": 0},
                "geometry": {"width": 200, "height": 200},
                "createdAt": "2024-03-14T12:00:00.000Z",
                "modifiedAt": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("GET", "/v2/boards/{board_id}/members", writes=False)
    async def list_board_members(self, request, board_id="", **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "3074457353169356300", "role": "editor", "name": "Mock User"},
                ],
                "total": 1,
                "size": 1,
                "offset": 0,
                "limit": 20,
            }
        )
