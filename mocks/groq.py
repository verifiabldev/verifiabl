# CHANGELOG: https://console.groq.com/docs/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://console.groq.com/docs/api-reference
# SANDBOX:   https://console.groq.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header
from mocks.base import BaseMock, route
from models import MockResponse


class GroqMock(BaseMock):
    prefix = "/groq"
    spec_url = "https://console.groq.com/docs/api-reference"
    sandbox_base = "https://api.groq.com"

    @route("GET", "/openai/v1/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "llama-3.3-70b-versatile",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "groq",
                    },
                    {
                        "id": "llama-3.1-8b-instant",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "groq",
                    },
                    {
                        "id": "openai/gpt-oss-20b",
                        "object": "model",
                        "created": 1710400000,
                        "owned_by": "groq",
                    },
                ],
            }
        )

    @route("GET", "/openai/v1/models/{model}", writes=False)
    async def get_model(self, request, model="", **kw):
        return MockResponse(
            body={
                "id": model or "llama-3.3-70b-versatile",
                "object": "model",
                "created": 1710400000,
                "owned_by": "groq",
            }
        )

    @route("POST", "/openai/v1/chat/completions", writes=False)
    async def create_chat_completion(self, request, **kw):
        return MockResponse(
            body={
                "id": "chatcmpl_mock_verifiabl",
                "object": "chat.completion",
                "created": 1710400000,
                "model": "llama-3.3-70b-versatile",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Mock completion."},
                        "logprobs": None,
                        "finish_reason": "stop",
                    },
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 2,
                    "total_tokens": 12,
                    "queue_time": 0.01,
                    "prompt_time": 0.001,
                    "completion_time": 0.05,
                    "total_time": 0.061,
                },
                "system_fingerprint": "fp_mock_verifiabl",
                "x_groq": {"id": "req_mock_verifiabl"},
            }
        )

    @route("POST", "/openai/v1/responses", writes=False)
    async def create_response(self, request, **kw):
        return MockResponse(
            body={
                "id": "resp_mock_verifiabl",
                "object": "response",
                "status": "completed",
                "created_at": 1710400000,
                "model": "llama-3.3-70b-versatile",
                "output": [
                    {
                        "type": "message",
                        "id": "msg_mock_001",
                        "status": "completed",
                        "role": "assistant",
                        "content": [
                            {"type": "output_text", "text": "Mock response.", "annotations": []}
                        ],
                    }
                ],
                "usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12},
                "error": None,
                "incomplete_details": None,
            }
        )

    @route("POST", "/openai/v1/audio/transcriptions", writes=False)
    async def create_transcription(self, request, **kw):
        return MockResponse(
            body={"text": "Mock transcribed text.", "x_groq": {"id": "req_mock_verifiabl"}}
        )

    @route("POST", "/openai/v1/audio/translations", writes=False)
    async def create_translation(self, request, **kw):
        return MockResponse(body={"text": "Mock translated text."})
