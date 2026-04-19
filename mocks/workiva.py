# CHANGELOG: https://support.workiva.com/hc/en-us/sections/4404206165268-Release-Notes (no RSS/atom feed as of 2026-03)
# SPEC:      https://developers.workiva.com/2022-01-01/
# SANDBOX:   https://developer.workiva.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _file(id_: str, name: str, kind: str = "Document", container: str = ""):
    return {
        "id": id_,
        "name": name,
        "kind": kind,
        "type": "10-K" if kind == "Document" else kind,
        "container": container,
        "created": {"dateTime": "2019-10-28T15:03:27Z"},
        "modified": {"dateTime": "2019-10-29T13:15:27Z"},
        "template": False,
    }


def _document(id_: str, name: str):
    return {
        "id": id_,
        "name": name,
        "created": {"dateTime": "2019-10-28T15:03:27Z"},
        "modified": {"dateTime": "2019-10-29T13:15:27Z"},
        "template": False,
    }


class WorkivaMock(BaseMock):
    prefix = "/workiva"
    spec_url = "https://developers.workiva.com/2022-01-01/"
    sandbox_base = "https://api.app.wdesk.com"

    @route("GET", "/platform/v1/files", writes=False)
    async def list_files(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    _file("file_mock_001", "2019 Supporting Documents", "Folder"),
                    _file("file_mock_002", "2019 Year-End Summary", "Document"),
                ],
            }
        )

    @route("GET", "/platform/v1/files/{fileId}", writes=False)
    async def get_file(self, request, fileId="", **kw):
        return MockResponse(body=_file(fileId or "file_mock_002", "Year-end review", "Document"))

    @route("PUT", "/platform/v1/files/{fileId}")
    async def update_file(self, request, fileId="", **kw):
        return MockResponse(
            body=_file(fileId or "file_mock_002", "Year-end review (updated)", "Document")
        )

    @route("GET", "/platform/v1/documents", writes=False)
    async def list_documents(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    _document("doc_mock_001", "Example Company 10-K"),
                    _document("doc_mock_002", "2019 Year-End Summary"),
                ],
            }
        )

    @route("GET", "/platform/v1/documents/{documentId}", writes=False)
    async def get_document(self, request, documentId="", **kw):
        return MockResponse(body=_document(documentId or "doc_mock_001", "Example Company 10-K"))

    @route("POST", "/platform/v1/tasks")
    async def create_task(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "task_mock_001",
                "title": "Review Document",
                "description": "Review document for spelling and grammar",
                "status": "Created",
                "assignee": {
                    "id": "V1ZVd2VyFzU3NiQ1NDA4NjIzNzk2MjD",
                    "displayName": "Jane Doe",
                    "email": "jane.doe@verifiabl.dev",
                },
                "dueDate": "2019-10-30T00:00:00Z",
                "location": {
                    "file": "file_mock_002",
                    "fileSegment": "465ttdh2a142y75ehsft5ab34edf5675",
                },
                "created": {
                    "dateTime": "2019-10-28T15:03:27Z",
                    "user": {"id": "V3ZVc2VyFzV3NiQ5NDA2NjIzNxk2njH"},
                },
                "modified": {"dateTime": "2019-10-28T15:03:27Z"},
                "sourceUrl": "https://app.wdesk.com/tasks/d/mock_token",
            },
        )
