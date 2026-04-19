# CHANGELOG: https://docs.anthropic.com/en/release-notes/api  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.anthropic.com/en/api/overview
# SANDBOX:   https://console.anthropic.com/
# SKILL:     —
# MCP:       —
# LLMS:      https://claude.com/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class ClaudeMock(BaseMock):
    prefix = "/claude"
    spec_url = "https://docs.anthropic.com/en/api/overview"
    sandbox_base = "https://api.anthropic.com"

    @route("GET", "/v1/models", writes=False)
    async def list_models(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "claude-3-5-sonnet-20241022",
                        "type": "model",
                        "display_name": "Claude 3.5 Sonnet",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "claude-3-opus-20240229",
                        "type": "model",
                        "display_name": "Claude 3 Opus",
                        "created_at": 1709200000,
                    },
                ],
                "last_id": "claude-3-opus-20240229",
                "first_id": "claude-3-5-sonnet-20241022",
                "has_more": False,
            }
        )

    @route("GET", "/v1/models/{id}", writes=False)
    async def get_model(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "claude-3-5-sonnet-20241022",
                "type": "model",
                "display_name": "Claude 3.5 Sonnet",
                "created_at": 1710400000,
            }
        )

    @route("POST", "/v1/messages")
    async def create_message(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "msg_mock_verifiabl",
                "type": "message",
                "role": "assistant",
                "content": [{"type": "text", "text": "Mock response from verifiabl.dev."}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "model": "claude-3-5-sonnet-20241022",
                "usage": {"input_tokens": 10, "output_tokens": 12},
            },
        )

    @route("POST", "/v1/messages/count_tokens", writes=False)
    async def count_tokens(self, request, **kw):
        return MockResponse(body={"input_tokens": 42})

    @route("GET", "/v1/messages/batches", writes=False)
    async def list_batches(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "batch_mock_001",
                        "type": "message_batch",
                        "processing_status": "ended",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "batch_mock_002",
                        "type": "message_batch",
                        "processing_status": "in_progress",
                        "created_at": 1710400100,
                    },
                ],
                "last_id": "batch_mock_002",
                "first_id": "batch_mock_001",
                "has_more": False,
            }
        )

    @route("GET", "/v1/messages/batches/{id}", writes=False)
    async def get_batch(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "batch_mock_001",
                "type": "message_batch",
                "processing_status": "ended",
                "created_at": 1710400000,
                "ended_at": 1710403600,
                "request_counts": {
                    "succeeded": 2,
                    "errored": 0,
                    "canceled": 0,
                    "expired": 0,
                    "processing": 0,
                },
            }
        )

    @route("POST", "/v1/messages/batches")
    async def create_batch(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "batch_mock_verifiabl",
                "type": "message_batch",
                "processing_status": "in_progress",
                "created_at": 1710400000,
            },
        )
