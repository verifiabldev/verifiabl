# CHANGELOG: https://huggingface.co/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://huggingface.co/.well-known/openapi.json
# SANDBOX:   https://huggingface.co
# SKILL:     —
# MCP:       —
# LLMS:      https://huggingface.co/docs/hub/llms-full.txt
from mocks.base import BaseMock, route
from models import MockResponse


class HuggingfaceMock(BaseMock):
    prefix = "/huggingface"
    spec_url = "https://huggingface.co/.well-known/openapi.json"
    sandbox_base = "https://huggingface.co"

    @route("GET", "/api/whoami-v2", writes=False)
    async def whoami(self, request, **kw):
        return MockResponse(
            body={
                "type": "user",
                "id": "user_mock_verifiabl",
                "name": "mockuser",
                "fullname": "Mock User",
                "email": "mock@verifiabl.dev",
                "emailVerified": True,
                "isPro": False,
                "canPay": False,
                "orgs": [],
                "auth": {"accessToken": {"displayName": "mock", "role": "write"}},
            }
        )

    @route("GET", "/api/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "verifiabl/mock-model-a",
                    "modelId": "verifiabl/mock-model-a",
                    "author": "verifiabl",
                    "downloads": 1000,
                    "likes": 42,
                    "private": False,
                    "tags": ["text-generation"],
                    "pipeline_tag": "text-generation",
                    "createdAt": "2024-03-14T12:00:00.000Z",
                },
                {
                    "id": "verifiabl/mock-model-b",
                    "modelId": "verifiabl/mock-model-b",
                    "author": "verifiabl",
                    "downloads": 500,
                    "likes": 10,
                    "private": False,
                    "tags": ["sentence-similarity"],
                    "pipeline_tag": "sentence-similarity",
                    "createdAt": "2024-03-14T12:00:00.000Z",
                },
            ]
        )

    @route("GET", "/api/datasets", writes=False)
    async def list_datasets(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "verifiabl/mock-dataset-a",
                    "author": "verifiabl",
                    "downloads": 200,
                    "likes": 5,
                    "private": False,
                    "lastModified": "2024-03-14T12:00:00.000Z",
                },
                {
                    "id": "verifiabl/mock-dataset-b",
                    "author": "verifiabl",
                    "downloads": 100,
                    "likes": 2,
                    "private": False,
                    "lastModified": "2024-03-14T12:00:00.000Z",
                },
            ]
        )

    @route("GET", "/api/{repoType}/{namespace}/{repo}", writes=False)
    async def get_repo(self, request, repoType="", namespace="", repo="", **kw):
        return MockResponse(
            body={
                "id": f"{namespace}/{repo}",
                "author": namespace,
                "downloads": 1000,
                "likes": 42,
                "lastModified": "2024-03-14T12:00:00.000Z",
                "private": False,
                "repoType": repoType or "model",
                "gated": False,
            }
        )

    @route("GET", "/api/models/{namespace}/{repo}/lfs-files", writes=False)
    async def list_model_lfs(self, request, namespace="", repo="", **kw):
        return MockResponse(
            body=[
                {"path": "config.json", "size": 600, "blobId": "blob_mock_001"},
                {"path": "model.safetensors", "size": 500000000, "blobId": "blob_mock_002"},
            ]
        )

    @route("GET", "/api/{repoType}/{namespace}/{repo}/refs", writes=False)
    async def list_refs(self, request, repoType="", namespace="", repo="", **kw):
        return MockResponse(
            body={"branches": [{"name": "main", "ref": "refs/heads/main"}], "convertedRefs": []}
        )

    @route("GET", "/api/{repoType}/{namespace}/{repo}/tree/{rev}/{path}", writes=False)
    async def get_tree(
        self, request, repoType="", namespace="", repo="", rev="main", path="", **kw
    ):
        return MockResponse(
            body=[
                {"path": "README.md", "type": "file", "size": 1024},
                {"path": "config.json", "type": "file", "size": 600},
            ]
        )

    @route("POST", "/api/repos/create")
    async def create_repo(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "url": "https://huggingface.co/verifiabl/new-repo",
                "repoId": "verifiabl/new-repo",
                "repoType": "model",
            },
        )

    @route("POST", "/api/{repoType}/{namespace}/{repo}/branch/{rev}")
    async def create_branch(self, request, repoType="", namespace="", repo="", rev="", **kw):
        return MockResponse(
            body={"ref": f"refs/heads/{rev or 'feature'}", "revision": "rev_mock_001"}
        )

    @route("PUT", "/api/{repoType}/{namespace}/{repo}/settings")
    async def update_repo_settings(self, request, repoType="", namespace="", repo="", **kw):
        return MockResponse(body={"id": f"{namespace}/{repo}", "private": False})
