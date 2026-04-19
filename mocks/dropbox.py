# CHANGELOG: https://www.dropbox.com/developers/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/dropbox/dropbox-api-spec
# SANDBOX:   https://www.dropbox.com/developers/apps
# SKILL:     —
# MCP:       https://mcp.dropbox.com/mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class DropboxMock(BaseMock):
    prefix = "/dropbox"
    spec_url = "https://github.com/dropbox/dropbox-api-spec"
    sandbox_base = "https://api.dropboxapi.com"

    @route("POST", "/2/users/get_current_account", writes=False)
    async def current_account(self, request, **kw):
        return MockResponse(
            body={
                "account_id": "dbid:mock_verifiabl",
                "name": {"display_name": "Mock User"},
                "email": "mock@verifiabl.dev",
            }
        )

    @route("POST", "/2/files/list_folder", writes=False)
    async def list_folder(self, request, **kw):
        return MockResponse(
            body={
                "entries": [
                    {
                        "name": "mock.txt",
                        ".tag": "file",
                        "id": "id:mock_file_001",
                        "path_lower": "/mock.txt",
                        "size": 1024,
                    },
                    {
                        "name": "docs",
                        ".tag": "folder",
                        "id": "id:mock_folder_001",
                        "path_lower": "/docs",
                    },
                ],
                "cursor": "mock_cursor_verifiabl",
                "has_more": False,
            }
        )

    @route("POST", "/2/files/list_folder/continue", writes=False)
    async def list_folder_continue(self, request, **kw):
        return MockResponse(body={"entries": [], "cursor": "mock_cursor_end", "has_more": False})

    @route("POST", "/2/files/get_metadata", writes=False)
    async def get_metadata(self, request, **kw):
        return MockResponse(
            body={
                "name": "mock.txt",
                ".tag": "file",
                "id": "id:mock_file_001",
                "path_lower": "/mock.txt",
                "size": 1024,
            }
        )

    @route("POST", "/2/files/create_folder")
    async def create_folder(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "name": "new_folder",
                ".tag": "folder",
                "id": "id:mock_folder_new",
                "path_lower": "/new_folder",
            },
        )

    @route("POST", "/2/files/delete")
    async def delete(self, request, **kw):
        return MockResponse(body={".tag": "file", "id": "id:mock_file_001", "name": "mock.txt"})

    @route("POST", "/2/files/upload")
    async def upload(self, request, **kw):
        return MockResponse(
            body={
                "name": "uploaded.txt",
                ".tag": "file",
                "id": "id:mock_upload_001",
                "path_lower": "/uploaded.txt",
                "size": 0,
            }
        )

    @route("POST", "/2/files/get_temporary_link", writes=False)
    async def get_temporary_link(self, request, **kw):
        return MockResponse(
            body={
                "link": "https://dl.dropboxusercontent.com/mock/verifiabl_temp",
                "metadata": {
                    "name": "mock.txt",
                    ".tag": "file",
                    "id": "id:mock_file_001",
                    "size": 1024,
                },
            }
        )
