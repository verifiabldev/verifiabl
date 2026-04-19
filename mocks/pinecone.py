# CHANGELOG: https://docs.pinecone.io/release-notes/2024 (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/pinecone-io/pinecone-api
# SANDBOX:   https://app.pinecone.io/
# SKILL:     —
# MCP:       —
# LLMS:      https://docs.pinecone.io/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class PineconeMock(BaseMock):
    prefix = "/pinecone"
    spec_url = "https://github.com/pinecone-io/pinecone-api"
    sandbox_base = "https://api.pinecone.io"

    @route("GET", "/indexes", writes=False)
    async def list_indexes(self, request, **kw):
        return MockResponse(
            body={
                "indexes": [
                    {
                        "name": "mock-index-001",
                        "metric": "cosine",
                        "dimension": 1536,
                        "status": {"ready": True, "state": "Ready"},
                        "host": "mock-index-001.svc.us-east-1.pinecone.io",
                        "spec": {"serverless": {"region": "us-east-1", "cloud": "aws"}},
                        "deletion_protection": "disabled",
                        "vector_type": "dense",
                    },
                    {
                        "name": "mock-index-002",
                        "metric": "cosine",
                        "dimension": 384,
                        "status": {"ready": True, "state": "Ready"},
                        "host": "mock-index-002.svc.us-west1-gcp.pinecone.io",
                        "spec": {"serverless": {"region": "us-west1", "cloud": "gcp"}},
                        "deletion_protection": "disabled",
                        "vector_type": "dense",
                    },
                ]
            }
        )

    @route("POST", "/indexes")
    async def create_index(self, request, **kw):
        return MockResponse(status=201, body={})

    @route("GET", "/indexes/{name}", writes=False)
    async def describe_index(self, request, name="", **kw):
        return MockResponse(
            body={
                "name": name or "mock-index-001",
                "dimension": 1536,
                "metric": "cosine",
                "host": "mock-index-001.svc.us-east-1.pinecone.io",
                "status": {"ready": True, "state": "Ready"},
                "spec": {"serverless": {"cloud": "aws", "region": "us-east-1"}},
                "deletion_protection": "disabled",
                "vector_type": "dense",
            }
        )

    @route("DELETE", "/indexes/{name}")
    async def delete_index(self, request, name="", **kw):
        return MockResponse(body={})

    @route("POST", "/query", writes=False)
    async def query(self, request, **kw):
        return MockResponse(
            body={
                "matches": [
                    {"id": "vec_mock_001", "score": 0.95, "values": [0.1] * 8},
                    {"id": "vec_mock_002", "score": 0.88, "values": [0.2] * 8},
                ],
                "namespace": "example-namespace",
                "usage": {"read_units": 6},
            }
        )

    @route("POST", "/vectors/upsert")
    async def upsert(self, request, **kw):
        return MockResponse(body={"upsertedCount": 2})

    @route("GET", "/vectors/fetch", writes=False)
    async def fetch(self, request, **kw):
        return MockResponse(
            body={
                "vectors": {
                    "vec_mock_001": {
                        "id": "vec_mock_001",
                        "values": [0.1] * 8,
                        "metadata": {"genre": "comedy", "year": 2020},
                    },
                    "vec_mock_002": {
                        "id": "vec_mock_002",
                        "values": [0.2] * 8,
                        "metadata": {"genre": "documentary", "year": 2019},
                    },
                },
                "namespace": "example-namespace",
                "usage": {"read_units": 1},
            }
        )
