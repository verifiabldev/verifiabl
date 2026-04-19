# CHANGELOG: https://openrouter.ai/announcements  (no RSS/atom feed as of 2026-03)
# SPEC:      https://openrouter.ai/openapi.json
# SANDBOX:   https://openrouter.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class OpenRouterMock(BaseMock):
    prefix = "/openrouter"
    spec_url = "https://openrouter.ai/openapi.json"
    sandbox_base = "https://openrouter.ai"

    @route("GET", "/api/v1/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": "openai/gpt-4o-mini", "name": "GPT-4o mini", "context_length": 128000},
                    {
                        "id": "anthropic/claude-3.5-sonnet",
                        "name": "Claude 3.5 Sonnet",
                        "context_length": 200000,
                    },
                ],
            }
        )

    @route("GET", "/api/v1/models/count", writes=False)
    async def models_count(self, request, **kw):
        return MockResponse(body={"data": 250})

    @route("GET", "/api/v1/generation", writes=False)
    async def get_generation(self, request, **kw):
        return MockResponse(
            body={
                "id": "gen_mock_verifiabl",
                "model": "openai/gpt-4o-mini",
                "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14},
                "cost": 0.00014,
            }
        )

    @route("POST", "/api/v1/chat/completions")
    async def chat_completions(self, request, **kw):
        return MockResponse(
            body={
                "id": "gen_mock_verifiabl",
                "object": "chat.completion",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "Hello there!"},
                    }
                ],
                "created": 1710400000,
                "model": "openai/gpt-4o-mini",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 4,
                    "total_tokens": 14,
                    "cost": 0.00014,
                },
            }
        )

    @route("POST", "/api/v1/completions")
    async def completions(self, request, **kw):
        return MockResponse(
            body={
                "id": "gen_mock_verifiabl",
                "choices": [{"finish_reason": "stop", "text": "Hello there!"}],
                "created": 1710400000,
                "model": "openai/gpt-4o-mini",
                "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14},
            }
        )

    @route("POST", "/api/v1/embeddings")
    async def embeddings(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [{"object": "embedding", "embedding": [0.01] * 1536, "index": 0}],
                "model": "openai/text-embedding-3-small",
                "usage": {"prompt_tokens": 5, "total_tokens": 5},
            }
        )
