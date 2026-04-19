# CHANGELOG: https://jam.dev/docs  (no RSS/atom feed as of 2026-03)
# SPEC:      https://jam.dev/docs/debug-a-jam/mcp  (REST-style mock inferred from MCP + webhooks)
# SANDBOX:   https://app.jam.dev
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (PAT: jam_pat_...)
from mocks.base import BaseMock, route
from models import MockResponse


class JamdevMock(BaseMock):
    prefix = "/jamdev"
    spec_url = "https://jam.dev/docs/debug-a-jam/mcp"
    sandbox_base = "https://api.jam.dev"

    @route("GET", "/v1/jams", writes=False)
    async def list_jams(self, request, **kw):
        return MockResponse(
            body={
                "jams": [
                    {
                        "id": "jam_mock_001",
                        "type": "video",
                        "recording_url": "https://jam.dev/r/rec_mock_001",
                        "created_at": 1710400000,
                        "author": {"id": "usr_mock_001", "name": "Mock User"},
                    },
                    {
                        "id": "jam_mock_002",
                        "type": "screenshot",
                        "recording_url": "https://jam.dev/r/rec_mock_002",
                        "created_at": 1710400100,
                        "author": {"id": "usr_mock_001", "name": "Mock User"},
                    },
                ],
            }
        )

    @route("GET", "/v1/jams/{id}", writes=False)
    async def get_jam(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "jam_mock_001",
                "type": "video",
                "recording_url": "https://jam.dev/r/rec_mock_001",
                "created_at": 1710400000,
                "author": {
                    "id": "usr_mock_001",
                    "name": "Mock User",
                    "email": "mock@verifiabl.dev",
                },
                "folder_id": "fld_mock_001",
            }
        )

    @route("GET", "/v1/members", writes=False)
    async def list_members(self, request, **kw):
        return MockResponse(
            body={
                "members": [
                    {"id": "usr_mock_001", "name": "Mock User", "email": "mock@verifiabl.dev"},
                    {"id": "usr_mock_002", "name": "Alice", "email": "alice@verifiabl.dev"},
                ],
            }
        )

    @route("GET", "/v1/folders", writes=False)
    async def list_folders(self, request, **kw):
        return MockResponse(
            body={
                "folders": [
                    {"id": "fld_mock_001", "name": "Bugs"},
                    {"id": "fld_mock_002", "name": "Feedback"},
                ],
            }
        )

    @route("GET", "/v1/jams/{id}/comments", writes=False)
    async def list_comments(self, request, id="", **kw):
        return MockResponse(
            body={
                "comments": [
                    {
                        "id": "cmt_mock_001",
                        "body": "Looks like a race condition.",
                        "author_id": "usr_mock_002",
                        "created_at": 1710400200,
                    },
                ],
            }
        )

    @route("POST", "/v1/jams/{id}/comments")
    async def create_comment(self, request, id="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "cmt_mock_002",
                "body": "Reproduced.",
                "author_id": "usr_mock_001",
                "created_at": 1710400300,
            },
        )

    @route("PATCH", "/v1/jams/{id}")
    async def update_jam(self, request, id="", **kw):
        return MockResponse(body={"id": id or "jam_mock_001", "folder_id": "fld_mock_002"})
