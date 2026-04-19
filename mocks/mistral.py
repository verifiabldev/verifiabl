# CHANGELOG: https://docs.mistral.ai/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/mistralai/platform-docs-public/blob/main/openapi.yaml
# SANDBOX:   https://console.mistral.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class MistralMock(BaseMock):
    prefix = "/mistral"
    spec_url = "https://github.com/mistralai/platform-docs-public/blob/main/openapi.yaml"
    sandbox_base = "https://api.mistral.ai"

    @route("GET", "/v1/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "mistral-small-latest",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "mistralai",
                        "capabilities": {
                            "completion_chat": True,
                            "completion_fim": False,
                            "function_calling": True,
                            "fine_tuning": False,
                            "vision": False,
                            "classification": False,
                        },
                        "name": None,
                        "description": None,
                        "max_context_length": 32768,
                    },
                    {
                        "id": "mistral-embed",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "mistralai",
                        "capabilities": {
                            "completion_chat": False,
                            "completion_fim": False,
                            "function_calling": False,
                            "fine_tuning": False,
                            "vision": False,
                            "classification": False,
                        },
                        "name": None,
                        "description": None,
                        "max_context_length": 8192,
                    },
                ],
            }
        )

    @route("GET", "/v1/models/{model_id}", writes=False)
    async def get_model(self, request, model_id="", **kw):
        return MockResponse(
            body={
                "id": model_id or "mistral-small-latest",
                "object": "model",
                "created": 1710400000,
                "owned_by": "mistralai",
                "capabilities": {
                    "completion_chat": True,
                    "completion_fim": False,
                    "function_calling": True,
                    "fine_tuning": False,
                    "vision": False,
                    "classification": False,
                },
                "name": None,
                "description": None,
                "max_context_length": 32768,
            }
        )

    @route("POST", "/v1/chat/completions", writes=False)
    async def create_chat_completion(self, request, **kw):
        return MockResponse(
            body={
                "id": "chatcmpl_mock_verifiabl",
                "object": "chat.completion",
                "model": "mistral-small-latest",
                "created": 1710400000,
                "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Mock completion.",
                            "tool_calls": None,
                            "prefix": False,
                        },
                        "finish_reason": "stop",
                    },
                ],
            }
        )

    @route("POST", "/v1/embeddings", writes=False)
    async def create_embedding(self, request, **kw):
        return MockResponse(
            body={
                "id": "emb_mock_verifiabl",
                "object": "list",
                "data": [{"object": "embedding", "embedding": [0.0023, -0.0156], "index": 0}],
                "model": "mistral-embed",
                "usage": {"prompt_tokens": 5, "completion_tokens": 0, "total_tokens": 5},
            }
        )

    @route("POST", "/v1/moderations", writes=False)
    async def create_moderation(self, request, **kw):
        return MockResponse(
            body={
                "id": "modr_mock_verifiabl",
                "model": "mistral-moderation-latest",
                "results": [
                    {
                        "categories": {
                            "sexual": False,
                            "hate_and_discrimination": False,
                            "violence_and_threats": False,
                            "dangerous_and_criminal_content": False,
                            "selfharm": False,
                            "health": False,
                            "financial": False,
                            "law": False,
                            "pii": False,
                        },
                        "category_scores": {
                            "sexual": 0.001,
                            "hate_and_discrimination": 0.001,
                            "violence_and_threats": 0.001,
                            "dangerous_and_criminal_content": 0.001,
                            "selfharm": 0.001,
                            "health": 0.001,
                            "financial": 0.001,
                            "law": 0.001,
                            "pii": 0.001,
                        },
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
                        "sample_type": "instruct",
                        "source": "upload",
                        "num_lines": 2,
                        "mimetype": "application/jsonl",
                        "signature": None,
                    },
                    {
                        "id": "file_mock_002",
                        "object": "file",
                        "bytes": 2048,
                        "created_at": 1710400001,
                        "filename": "prompts.jsonl",
                        "purpose": "fine-tune",
                        "sample_type": "instruct",
                        "source": "upload",
                        "num_lines": 3,
                        "mimetype": "application/jsonl",
                        "signature": None,
                    },
                ],
                "total": 2,
            }
        )

    @route("POST", "/v1/files")
    async def create_file(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "file_mock_new",
                "object": "file",
                "bytes": None,
                "created_at": 1710400000,
                "filename": "upload.jsonl",
                "purpose": "fine-tune",
                "sample_type": "instruct",
                "source": "upload",
                "num_lines": 1,
                "mimetype": "application/jsonl",
                "signature": "d4821d2de1917341",
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
                "sample_type": "instruct",
                "source": "upload",
                "num_lines": 2,
                "mimetype": "application/jsonl",
                "signature": None,
            }
        )
