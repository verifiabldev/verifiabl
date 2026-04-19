# CHANGELOG: https://weaviate.io/weaviate/release-notes (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/weaviate/weaviate/blob/master/openapi-specs/schema.json
# SANDBOX:   https://weaviate.io/go/console
# FAVICON:   https://weaviate.io/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
# LOC EXCEPTION: Schema, objects CRUD, batch, and GraphQL require 10 routes with spec-faithful envelope shapes.
from mocks.base import BaseMock, route
from models import MockResponse


class WeaviateMock(BaseMock):
    prefix = "/weaviate"
    spec_url = "https://github.com/weaviate/weaviate/blob/master/openapi-specs/schema.json"
    sandbox_base = "https://your-instance.weaviate.network"

    @route("GET", "/v1/schema", writes=False)
    async def get_schema(self, request, **kw):
        return MockResponse(
            body={
                "classes": [
                    {
                        "class": "Article",
                        "description": "Article collection",
                        "vectorizer": "text2vec-transformers",
                        "properties": [
                            {"name": "title", "dataType": ["string"]},
                            {"name": "content", "dataType": ["text"]},
                        ],
                    },
                    {
                        "class": "JeopardyQuestion",
                        "description": "Jeopardy questions",
                        "properties": [
                            {"name": "question", "dataType": ["string"]},
                            {"name": "answer", "dataType": ["string"]},
                        ],
                    },
                ],
                "name": "schema_mock",
                "maintainer": "mock@verifiabl.dev",
            }
        )

    @route("POST", "/v1/schema")
    async def create_class(self, request, **kw):
        return MockResponse(
            body={
                "class": "NewClass",
                "description": "Created by mock",
                "properties": [{"name": "name", "dataType": ["string"]}],
            }
        )

    @route("GET", "/v1/schema/{className}", writes=False)
    async def get_class(self, request, className="", **kw):
        return MockResponse(
            body={
                "class": className or "Article",
                "description": "Article collection",
                "vectorizer": "text2vec-transformers",
                "properties": [
                    {"name": "title", "dataType": ["string"]},
                    {"name": "content", "dataType": ["text"]},
                ],
            }
        )

    @route("GET", "/v1/objects", writes=False)
    async def list_objects(self, request, **kw):
        return MockResponse(
            body={
                "objects": [
                    {
                        "class": "Article",
                        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                        "properties": {"title": "Mock Article", "content": "Sample content"},
                        "creationTimeUnix": 1710400000000,
                        "lastUpdateTimeUnix": 1710400000000,
                    },
                    {
                        "class": "Article",
                        "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
                        "properties": {"title": "Second Article", "content": "More content"},
                        "creationTimeUnix": 1710400001000,
                        "lastUpdateTimeUnix": 1710400001000,
                    },
                ],
                "totalResults": 2,
            }
        )

    @route("POST", "/v1/objects")
    async def create_object(self, request, **kw):
        return MockResponse(
            body={
                "class": "Article",
                "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
                "properties": {"title": "New Article", "content": "Created by mock"},
                "creationTimeUnix": 1710400002000,
                "lastUpdateTimeUnix": 1710400002000,
            }
        )

    @route("GET", "/v1/objects/{id}", writes=False)
    async def get_object(self, request, id="", **kw):
        return MockResponse(
            body={
                "class": "Article",
                "id": id or "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "properties": {"title": "Mock Article", "content": "Sample content"},
                "creationTimeUnix": 1710400000000,
                "lastUpdateTimeUnix": 1710400000000,
            }
        )

    @route("PUT", "/v1/objects/{id}")
    async def update_object(self, request, id="", **kw):
        return MockResponse(
            body={
                "class": "Article",
                "id": id or "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "properties": {"title": "Updated Article", "content": "Updated content"},
                "creationTimeUnix": 1710400000000,
                "lastUpdateTimeUnix": 1710400003000,
            }
        )

    @route("DELETE", "/v1/objects/{id}")
    async def delete_object(self, request, id="", **kw):
        return MockResponse(status=204)

    @route("POST", "/v1/batch/objects")
    async def batch_objects(self, request, **kw):
        return MockResponse(
            body={
                "results": [
                    {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "SUCCESS"},
                    {"id": "b2c3d4e5-f6a7-8901-bcde-f12345678901", "status": "SUCCESS"},
                ],
            }
        )

    @route("POST", "/v1/graphql", writes=False)
    async def graphql(self, request, **kw):
        return MockResponse(
            body={
                "data": {
                    "Get": {
                        "Article": [
                            {
                                "title": "Mock Article",
                                "content": "Sample content",
                                "_additional": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
                            },
                        ],
                    },
                },
            }
        )
