# CHANGELOG: https://developers.figma.com/docs/rest-api/changelog/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/figma/rest-api-spec
# SANDBOX:   https://www.figma.com/developers
# SKILL:     —
# MCP:       https://mcp.figma.com/mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class FigmaMock(BaseMock):
    prefix = "/figma"
    spec_url = "https://github.com/figma/rest-api-spec"
    sandbox_base = "https://api.figma.com"

    @route("GET", "/v1/me", writes=False)
    async def get_me(self, request, **kw):
        return MockResponse(
            body={
                "id": "user_mock_verifiabl",
                "handle": "mockuser",
                "img_url": "https://verifiabl.dev/avatar.png",
                "email": "mock@verifiabl.dev",
            }
        )

    @route("GET", "/v1/files/{file_key}", writes=False)
    async def get_file(self, request, file_key="", **kw):
        return MockResponse(
            body={
                "name": "Mock Design",
                "role": "editor",
                "lastModified": "2024-03-14T12:00:00.000Z",
                "editorType": "figma",
                "version": "1710400000",
                "document": {
                    "id": "0:0",
                    "name": "Document",
                    "type": "DOCUMENT",
                    "children": [{"id": "1:2", "name": "Page 1", "type": "CANVAS", "children": []}],
                },
                "components": {},
                "componentSets": {},
                "schemaVersion": 0,
                "styles": {},
            }
        )

    @route("GET", "/v1/files/{file_key}/meta", writes=False)
    async def get_file_meta(self, request, file_key="", **kw):
        return MockResponse(
            body={
                "name": "Mock Design",
                "folder_name": "Mock Project",
                "last_touched_at": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("GET", "/v1/teams/{team_id}/projects", writes=False)
    async def get_team_projects(self, request, team_id="", **kw):
        return MockResponse(
            body={
                "name": "Mock Team",
                "projects": [
                    {"id": "proj_mock_001", "name": "Design System"},
                    {"id": "proj_mock_002", "name": "Marketing"},
                ],
            }
        )

    @route("GET", "/v1/projects/{project_id}/files", writes=False)
    async def get_project_files(self, request, project_id="", **kw):
        return MockResponse(
            body={
                "name": "Design System",
                "files": [
                    {
                        "key": "file_mock_001",
                        "name": "Components",
                        "thumbnail_url": "https://verifiabl.dev/thumb.png",
                        "last_modified": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "key": "file_mock_002",
                        "name": "Tokens",
                        "last_modified": "2024-03-13T10:00:00.000Z",
                    },
                ],
            }
        )

    @route("GET", "/v1/files/{file_key}/components", writes=False)
    async def get_file_components(self, request, file_key="", **kw):
        return MockResponse(
            body={
                "status": 200,
                "error": False,
                "meta": {
                    "components": [
                        {
                            "key": "comp_mock_001",
                            "file_key": file_key or "file_mock_001",
                            "node_id": "1:10",
                            "name": "Button",
                            "thumbnail_url": "https://verifiabl.dev/comp.png",
                            "created_at": "2024-03-14T12:00:00.000Z",
                            "updated_at": "2024-03-14T12:00:00.000Z",
                        }
                    ]
                },
            }
        )

    @route("GET", "/v1/teams/{team_id}/components", writes=False)
    async def get_team_components(self, request, team_id="", **kw):
        return MockResponse(
            body={
                "status": 200,
                "error": False,
                "meta": {
                    "components": [
                        {
                            "key": "comp_mock_001",
                            "file_key": "file_mock_001",
                            "node_id": "1:10",
                            "name": "Button",
                            "thumbnail_url": "https://verifiabl.dev/comp.png",
                            "created_at": "2024-03-14T12:00:00.000Z",
                            "updated_at": "2024-03-14T12:00:00.000Z",
                        }
                    ],
                    "cursor": {},
                },
            }
        )

    @route("GET", "/v1/components/{key}", writes=False)
    async def get_component(self, request, key="", **kw):
        return MockResponse(
            body={
                "status": 200,
                "error": False,
                "meta": {
                    "key": key or "comp_mock_001",
                    "file_key": "file_mock_001",
                    "node_id": "1:10",
                    "name": "Button",
                    "thumbnail_url": "https://verifiabl.dev/comp.png",
                    "created_at": "2024-03-14T12:00:00.000Z",
                    "updated_at": "2024-03-14T12:00:00.000Z",
                },
            }
        )

    @route("GET", "/v1/images/{file_key}", writes=False)
    async def get_images(self, request, file_key="", **kw):
        return MockResponse(
            body={"err": None, "images": {"1:2": "https://verifiabl.dev/rendered.png"}}
        )

    @route("POST", "/v1/files/{file_key}/comments")
    async def post_comment(self, request, file_key="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "comment_mock_001",
                "file_key": file_key or "file_mock_001",
                "parent_id": None,
                "user": {
                    "id": "user_mock_verifiabl",
                    "handle": "mockuser",
                    "img_url": "https://verifiabl.dev/avatar.png",
                },
                "created_at": "2024-03-14T12:00:00.000Z",
                "resolved_at": None,
                "message": "Mock comment",
                "client_meta": {},
                "order_id": "1710400000",
            },
        )
