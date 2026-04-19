# CHANGELOG: https://github.com/ollama/ollama/releases  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.ollama.com/api
# SANDBOX:   https://ollama.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class OllamaMock(BaseMock):
    prefix = "/ollama"
    spec_url = "https://docs.ollama.com/api"
    sandbox_base = "https://ollama.com"

    @route("GET", "/api/tags", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "models": [
                    {
                        "name": "gemma3",
                        "model": "gemma3",
                        "modified_at": "2025-10-03T23:34:03.409490317-07:00",
                        "size": 3338801804,
                        "digest": "a2af6cc3eb7fa8be8504abaf9b04e88f17a119ec3f04a3addf55f92841195f5a",
                        "details": {
                            "format": "gguf",
                            "family": "gemma",
                            "families": ["gemma"],
                            "parameter_size": "4.3B",
                            "quantization_level": "Q4_K_M",
                        },
                    },
                    {
                        "name": "llama3.2",
                        "model": "llama3.2",
                        "modified_at": "2025-09-01T12:00:00Z",
                        "size": 2100000000,
                        "digest": "mock_digest_llama",
                        "details": {
                            "format": "gguf",
                            "family": "llama",
                            "families": ["llama"],
                            "parameter_size": "3B",
                            "quantization_level": "Q4_0",
                        },
                    },
                ],
            }
        )

    @route("POST", "/api/show", writes=False)
    async def show_model(self, request, **kw):
        return MockResponse(
            body={
                "parameters": "temperature 0.7\nnum_ctx 2048",
                "license": "Gemma Terms of Use",
                "capabilities": ["completion", "vision"],
                "modified_at": "2025-08-14T15:49:43.634137516-07:00",
                "details": {
                    "parent_model": "",
                    "format": "gguf",
                    "family": "gemma3",
                    "families": ["gemma3"],
                    "parameter_size": "4.3B",
                    "quantization_level": "Q4_K_M",
                },
                "template": "{{ .System }}\n\n{{ .Prompt }}",
            }
        )

    @route("POST", "/api/generate", writes=False)
    async def generate(self, request, **kw):
        return MockResponse(
            body={
                "model": "gemma3",
                "created_at": "2025-10-17T23:14:07.414671Z",
                "response": "Mock completion.",
                "done": True,
                "done_reason": "stop",
                "total_duration": 174560334,
                "load_duration": 101397084,
                "prompt_eval_count": 11,
                "prompt_eval_duration": 13074791,
                "eval_count": 18,
                "eval_duration": 52479709,
            }
        )

    @route("POST", "/api/chat", writes=False)
    async def chat(self, request, **kw):
        return MockResponse(
            body={
                "model": "gemma3",
                "created_at": "2025-10-17T23:14:07.414671Z",
                "message": {"role": "assistant", "content": "Mock chat response."},
                "done": True,
                "done_reason": "stop",
                "total_duration": 174560334,
                "load_duration": 101397084,
                "prompt_eval_count": 11,
                "prompt_eval_duration": 13074791,
                "eval_count": 18,
                "eval_duration": 52479709,
            }
        )

    @route("POST", "/api/embed", writes=False)
    async def embed(self, request, **kw):
        return MockResponse(
            body={
                "model": "embeddinggemma",
                "embeddings": [[0.010071029, -0.0017594862, 0.05007221, 0.04692972]],
                "total_duration": 14143917,
                "load_duration": 1019500,
                "prompt_eval_count": 8,
            }
        )

    @route("GET", "/api/ps", writes=False)
    async def list_running(self, request, **kw):
        return MockResponse(
            body={"models": [{"name": "gemma3", "size": 3338801804, "size_vram": 2100000000}]}
        )

    @route("GET", "/api/version", writes=False)
    async def version(self, request, **kw):
        return MockResponse(body={"version": "0.18.0"})

    @route("POST", "/api/pull")
    async def pull(self, request, **kw):
        return MockResponse(body={"status": "success"})

    @route("DELETE", "/api/delete")
    async def delete_model(self, request, **kw):
        return MockResponse(body={"status": "success"})
