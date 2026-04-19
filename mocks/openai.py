# CHANGELOG: https://developers.openai.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/openai/openai-openapi
# SANDBOX:   https://platform.openai.com
# SKILL:     —
# MCP:       —
# LLMS:      https://cdn.openai.com/API/docs/txt/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class OpenAIMock(BaseMock):
    prefix = "/openai"
    spec_url = "https://github.com/openai/openai-openapi"
    sandbox_base = "https://api.openai.com"

    @route("GET", "/v1/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "gpt-4o",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "system",
                    },
                    {
                        "id": "gpt-4o-mini",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "system",
                    },
                    {
                        "id": "text-embedding-3-small",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "system",
                    },
                ],
            }
        )

    @route("GET", "/v1/models/{model}", writes=False)
    async def get_model(self, request, model="", **kw):
        return MockResponse(
            body={
                "id": model or "gpt-4o",
                "object": "model",
                "created": 1710400000,
                "owned_by": "system",
            }
        )

    @route("POST", "/v1/chat/completions", writes=False)
    async def create_chat_completion(self, request, **kw):
        return MockResponse(
            body={
                "id": "chatcmpl_mock_verifiabl",
                "object": "chat.completion",
                "created": 1710400000,
                "model": "gpt-4o",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Mock completion."},
                        "finish_reason": "stop",
                    },
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
            }
        )

    @route("POST", "/v1/embeddings", writes=False)
    async def create_embedding(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [{"object": "embedding", "embedding": [0.0023, -0.0156], "index": 0}],
                "model": "text-embedding-3-small",
                "usage": {"prompt_tokens": 5, "total_tokens": 5},
            }
        )

    @route("POST", "/v1/completions", writes=False)
    async def create_completion(self, request, **kw):
        return MockResponse(
            body={
                "id": "cmpl_mock_verifiabl",
                "object": "text_completion",
                "created": 1710400000,
                "model": "gpt-4o-mini",
                "choices": [
                    {"text": " Mock.", "index": 0, "finish_reason": "stop", "logprobs": None}
                ],
                "usage": {"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7},
            }
        )

    @route("POST", "/v1/moderations", writes=False)
    async def create_moderation(self, request, **kw):
        return MockResponse(
            body={
                "id": "modr_mock_verifiabl",
                "model": "text-moderation-007",
                "results": [
                    {
                        "flagged": False,
                        "categories": {"harassment": False, "hate": False},
                        "category_scores": {"harassment": 0.001, "hate": 0.001},
                    }
                ],
            }
        )

    @route("GET", "/v1/files", writes=False)
    async def list_files(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "file_mock_001",
                        "object": "file",
                        "bytes": 1024,
                        "created_at": 1710400000,
                        "filename": "train.jsonl",
                        "purpose": "fine-tune",
                    },
                    {
                        "id": "file_mock_002",
                        "object": "file",
                        "bytes": 2048,
                        "created_at": 1710400001,
                        "filename": "prompts.jsonl",
                        "purpose": "assistants",
                    },
                ],
            }
        )

    @route("POST", "/v1/files")
    async def create_file(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "file_mock_new",
                "object": "file",
                "bytes": 512,
                "created_at": 1710400000,
                "filename": "upload.jsonl",
                "purpose": "fine-tune",
            },
        )

    @route("GET", "/v1/files/{file_id}", writes=False)
    async def get_file(self, request, file_id="", **kw):
        return MockResponse(
            body={
                "id": file_id or "file_mock_001",
                "object": "file",
                "bytes": 1024,
                "created_at": 1710400000,
                "filename": "train.jsonl",
                "purpose": "fine-tune",
            }
        )

    @route("DELETE", "/v1/files/{file_id}")
    async def delete_file(self, request, file_id="", **kw):
        return MockResponse(
            body={"id": file_id or "file_mock_001", "object": "file", "deleted": True}
        )
