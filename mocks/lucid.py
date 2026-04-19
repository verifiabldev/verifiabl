# CHANGELOG: https://community.lucid.co/product-updates  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.lucid.co/reference/overview
# SANDBOX:   https://developer.lucid.co
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _doc(doc_id="110808fd-4553-4316-bccf-4f25ff59a532", title="Mock Diagram"):
    return {
        "documentId": doc_id,
        "title": title,
        "editUrl": f"https://lucid.app/lucidchart/{doc_id}/edit",
        "viewUrl": f"https://lucid.app/lucidchart/{doc_id}/view",
        "version": 1,
        "pageCount": 1,
        "canEdit": True,
        "created": "2024-03-14T12:26:40Z",
        "creatorId": 12345,
        "lastModified": "2024-03-14T12:26:40Z",
        "lastModifiedUserId": 12345,
        "product": "lucidchart",
    }


class LucidMock(BaseMock):
    prefix = "/lucid"
    spec_url = "https://developer.lucid.co/reference/overview"
    sandbox_base = "https://api.lucid.co"

    @route("POST", "/documents", writes=True)
    async def create_document(self, request, **kw):
        return MockResponse(status=201, body=_doc("doc_mock_new_001", "Created Document"))

    @route("POST", "/documents/search", writes=False)
    async def search_documents(self, request, **kw):
        return MockResponse(
            body=[
                _doc("doc_mock_001", "Flowchart"),
                _doc("doc_mock_002", "Org Chart"),
            ]
        )

    @route("GET", "/documents/{id}", writes=False)
    async def get_document(self, request, id="", **kw):
        return MockResponse(body=_doc(id or "doc_mock_001", "Mock Diagram"))

    @route("POST", "/documents/{id}/trash", writes=True)
    async def trash_document(self, request, id="", **kw):
        return MockResponse(status=204, body=None)

    @route("POST", "/folders/search", writes=False)
    async def search_folders(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 1001,
                    "type": "folder",
                    "name": "My Documents",
                    "parent": None,
                    "created": "2024-03-14T12:26:40Z",
                },
                {
                    "id": 1002,
                    "type": "folder",
                    "name": "Projects",
                    "parent": 1001,
                    "created": "2024-03-14T12:26:40Z",
                },
            ]
        )

    @route("GET", "/documents/{id}/shares/users/{userId}", writes=False)
    async def get_document_user_collaborator(self, request, id="", userId="", **kw):
        return MockResponse(
            body={
                "documentId": id or "doc_mock_001",
                "userId": int(userId) if userId else 12345,
                "role": "edit",
                "created": "2024-03-14T12:26:40Z",
            }
        )
