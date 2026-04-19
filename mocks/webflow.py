# CHANGELOG: https://developers.webflow.com/data/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/webflow/openapi-spec
# SANDBOX:   https://webflow.com/dashboard
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per OpenAPI securitySchemes)
from mocks.base import BaseMock, route
from models import MockResponse


class WebflowMock(BaseMock):
    prefix = "/webflow"
    spec_url = "https://github.com/webflow/openapi-spec"
    sandbox_base = "https://api.webflow.com"

    @route("GET", "/v2/sites", writes=False)
    async def list_sites(self, request, **kw):
        return MockResponse(
            body={
                "sites": [
                    {
                        "id": "site_mock_001",
                        "workspaceId": "ws_mock_001",
                        "displayName": "Mock Site",
                        "shortName": "mock-site",
                        "createdOn": "2024-03-14T12:00:00.000Z",
                        "lastPublished": "2024-03-14T12:00:00.000Z",
                        "lastUpdated": "2024-03-14T12:00:00.000Z",
                        "previewUrl": "https://verifiabl.dev/preview.png",
                        "timeZone": "America/Los_Angeles",
                    },
                    {
                        "id": "site_mock_002",
                        "workspaceId": "ws_mock_001",
                        "displayName": "Blog",
                        "shortName": "blog",
                        "createdOn": "2024-03-13T10:00:00.000Z",
                        "lastPublished": "2024-03-13T10:00:00.000Z",
                        "lastUpdated": "2024-03-13T10:00:00.000Z",
                        "previewUrl": "https://verifiabl.dev/blog.png",
                        "timeZone": "UTC",
                    },
                ],
            }
        )

    @route("GET", "/v2/sites/{site_id}", writes=False)
    async def get_site(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "id": site_id or "site_mock_001",
                "workspaceId": "ws_mock_001",
                "displayName": "Mock Site",
                "shortName": "mock-site",
                "createdOn": "2024-03-14T12:00:00.000Z",
                "lastPublished": "2024-03-14T12:00:00.000Z",
                "lastUpdated": "2024-03-14T12:00:00.000Z",
                "previewUrl": "https://verifiabl.dev/preview.png",
                "timeZone": "America/Los_Angeles",
            }
        )

    @route("GET", "/v2/sites/{site_id}/collections", writes=False)
    async def list_collections(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "collections": [
                    {
                        "id": "col_mock_001",
                        "displayName": "Blog Posts",
                        "singularName": "Blog Post",
                        "slug": "blog-posts",
                        "createdOn": "2024-03-14T12:00:00.000Z",
                        "lastUpdated": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "col_mock_002",
                        "displayName": "Authors",
                        "singularName": "Author",
                        "slug": "authors",
                        "createdOn": "2024-03-13T10:00:00.000Z",
                        "lastUpdated": "2024-03-13T10:00:00.000Z",
                    },
                ],
            }
        )

    @route("GET", "/v2/collections/{collection_id}", writes=False)
    async def get_collection(self, request, collection_id="", **kw):
        return MockResponse(
            body={
                "id": collection_id or "col_mock_001",
                "displayName": "Blog Posts",
                "singularName": "Blog Post",
                "slug": "blog-posts",
                "createdOn": "2024-03-14T12:00:00.000Z",
                "lastUpdated": "2024-03-14T12:00:00.000Z",
                "fields": [
                    {
                        "id": "field_mock_001",
                        "displayName": "Name",
                        "slug": "name",
                        "type": "PlainText",
                        "isRequired": True,
                        "isEditable": True,
                    },
                    {
                        "id": "field_mock_002",
                        "displayName": "Body",
                        "slug": "body",
                        "type": "RichText",
                        "isRequired": False,
                        "isEditable": True,
                    },
                ],
            }
        )

    @route("GET", "/v2/collections/{collection_id}/items", writes=False)
    async def list_items(self, request, collection_id="", **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "item_mock_001",
                        "cmsLocaleId": "locale_mock",
                        "lastPublished": "2024-03-14T12:00:00.000Z",
                        "lastUpdated": "2024-03-14T12:00:00.000Z",
                        "createdOn": "2024-03-14T12:00:00.000Z",
                        "isArchived": False,
                        "isDraft": False,
                        "fieldData": {"name": "First Post", "slug": "first-post"},
                    },
                    {
                        "id": "item_mock_002",
                        "cmsLocaleId": "locale_mock",
                        "lastPublished": "2024-03-13T10:00:00.000Z",
                        "lastUpdated": "2024-03-13T10:00:00.000Z",
                        "createdOn": "2024-03-13T10:00:00.000Z",
                        "isArchived": False,
                        "isDraft": False,
                        "fieldData": {"name": "Second Post", "slug": "second-post"},
                    },
                ],
                "pagination": {"limit": 100, "offset": 0, "total": 2},
            }
        )

    @route("GET", "/v2/collections/{collection_id}/items/{item_id}", writes=False)
    async def get_item(self, request, collection_id="", item_id="", **kw):
        return MockResponse(
            body={
                "id": item_id or "item_mock_001",
                "cmsLocaleId": "locale_mock",
                "lastPublished": "2024-03-14T12:00:00.000Z",
                "lastUpdated": "2024-03-14T12:00:00.000Z",
                "createdOn": "2024-03-14T12:00:00.000Z",
                "isArchived": False,
                "isDraft": False,
                "fieldData": {"name": "First Post", "slug": "first-post"},
            }
        )

    @route("POST", "/v2/collections/{collection_id}/items")
    async def create_items(self, request, collection_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "items": [
                    {
                        "id": "item_mock_new",
                        "cmsLocaleId": "locale_mock",
                        "lastPublished": None,
                        "lastUpdated": "2024-03-14T12:00:00.000Z",
                        "createdOn": "2024-03-14T12:00:00.000Z",
                        "isArchived": False,
                        "isDraft": True,
                        "fieldData": {"name": "New Item", "slug": "new-item"},
                    }
                ]
            },
        )

    @route("PATCH", "/v2/collections/{collection_id}/items")
    async def update_items(self, request, collection_id="", **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "item_mock_001",
                        "cmsLocaleId": "locale_mock",
                        "lastPublished": "2024-03-14T12:00:00.000Z",
                        "lastUpdated": "2024-03-14T12:00:00.000Z",
                        "createdOn": "2024-03-14T12:00:00.000Z",
                        "isArchived": False,
                        "isDraft": False,
                        "fieldData": {"name": "Updated Post", "slug": "updated-post"},
                    }
                ]
            }
        )

    @route("POST", "/v2/collections/{collection_id}/items/publish")
    async def publish_items(self, request, collection_id="", **kw):
        return MockResponse(
            body={"publishTime": "2024-03-14T12:00:00.000Z", "publishStatus": "success"}
        )
