# CHANGELOG: https://ai.google.dev/gemini-api/docs/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://ai.google.dev/api/rest
# SANDBOX:   https://aistudio.google.com/app/apikey
# FAVICON:   https://google.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      API key in x-goog-api-key header (per ai.google.dev)
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: 10 endpoints (models, generateContent, embedContent, countTokens, files) with schema-faithful camelCase and envelope; single file keeps integration discoverable.
class GeminiMock(BaseMock):
    prefix = "/gemini"
    spec_url = "https://ai.google.dev/api/rest"
    sandbox_base = "https://generativelanguage.googleapis.com"

    @route("GET", "/v1beta/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "models": [
                    {
                        "name": "models/gemini-2.0-flash",
                        "baseModelId": "gemini-2.0-flash",
                        "version": "2.0",
                        "displayName": "Gemini 2.0 Flash",
                        "inputTokenLimit": 1048576,
                        "outputTokenLimit": 8192,
                        "supportedGenerationMethods": ["generateContent", "generateMessage"],
                    },
                    {
                        "name": "models/gemini-1.5-flash",
                        "baseModelId": "gemini-1.5-flash",
                        "version": "1.5",
                        "displayName": "Gemini 1.5 Flash",
                        "inputTokenLimit": 1048576,
                        "outputTokenLimit": 8192,
                        "supportedGenerationMethods": ["generateContent", "embedContent"],
                    },
                    {
                        "name": "models/text-embedding-004",
                        "baseModelId": "text-embedding-004",
                        "version": "1.0",
                        "displayName": "Text Embedding 004",
                        "inputTokenLimit": 2048,
                        "outputTokenLimit": 1,
                        "supportedGenerationMethods": ["embedContent"],
                    },
                ],
                "nextPageToken": None,
            }
        )

    @route("GET", "/v1beta/models/{name}", writes=False)
    async def get_model(self, request, name="", **kw):
        return MockResponse(
            body={
                "name": f"models/{name}" if name else "models/gemini-2.0-flash",
                "baseModelId": name.split("/")[-1] if name else "gemini-2.0-flash",
                "version": "2.0",
                "displayName": "Gemini 2.0 Flash",
                "inputTokenLimit": 1048576,
                "outputTokenLimit": 8192,
                "supportedGenerationMethods": ["generateContent", "generateMessage"],
            }
        )

    @route("POST", "/v1beta/models/{model}:generateContent", writes=False)
    async def generate_content(self, request, model="", **kw):
        return MockResponse(
            body={
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": "Mock completion from verifiabl.dev."}],
                            "role": "model",
                        },
                        "finishReason": "STOP",
                        "index": 0,
                    },
                ],
                "usageMetadata": {
                    "promptTokenCount": 10,
                    "candidatesTokenCount": 6,
                    "totalTokenCount": 16,
                },
                "modelVersion": "gemini-2.0-flash",
            }
        )

    @route("POST", "/v1beta/models/{model}:streamGenerateContent", writes=False)
    async def stream_generate_content(self, request, model="", **kw):
        return MockResponse(
            body={
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": "Mock streamed completion."}],
                            "role": "model",
                        },
                        "finishReason": "STOP",
                        "index": 0,
                    },
                ],
                "usageMetadata": {
                    "promptTokenCount": 10,
                    "candidatesTokenCount": 4,
                    "totalTokenCount": 14,
                },
            }
        )

    @route("POST", "/v1beta/models/{model}:embedContent", writes=False)
    async def embed_content(self, request, model="", **kw):
        return MockResponse(
            body={
                "embedding": {"values": [0.0023, -0.0156, 0.0081]},
            }
        )

    @route("POST", "/v1beta/models/{model}:countTokens", writes=False)
    async def count_tokens(self, request, model="", **kw):
        return MockResponse(body={"totalTokenCount": 42})

    @route("GET", "/v1beta/files", writes=False)
    async def list_files(self, request, **kw):
        return MockResponse(
            body={
                "files": [
                    {
                        "name": "files/file_mock_001",
                        "displayName": "train.jsonl",
                        "mimeType": "application/jsonl",
                        "sizeBytes": "1024",
                        "createTime": "2024-03-14T12:00:00Z",
                    },
                    {
                        "name": "files/file_mock_002",
                        "displayName": "prompts.jsonl",
                        "mimeType": "application/jsonl",
                        "sizeBytes": "2048",
                        "createTime": "2024-03-14T12:01:00Z",
                    },
                ],
                "nextPageToken": None,
            }
        )

    @route("GET", "/v1beta/files/{name}", writes=False)
    async def get_file(self, request, name="", **kw):
        return MockResponse(
            body={
                "name": f"files/{name}" if name else "files/file_mock_001",
                "displayName": "train.jsonl",
                "mimeType": "application/jsonl",
                "sizeBytes": "1024",
                "createTime": "2024-03-14T12:00:00Z",
            }
        )

    @route("POST", "/v1beta/files")
    async def create_file(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "name": "files/file_mock_new",
                "displayName": "upload.jsonl",
                "mimeType": "application/jsonl",
                "sizeBytes": "512",
                "createTime": "2024-03-14T12:00:00Z",
            },
        )
