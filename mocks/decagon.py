# CHANGELOG: https://docs.decagon.ai (no RSS/atom feed found as of 2026-03)
# SPEC:      https://docs.decagon.ai/api-reference (access gated; mock inferred from conversational AI platform)
# SANDBOX:   https://decagon.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class DecagonMock(BaseMock):
    prefix = "/decagon"
    spec_url = "https://docs.decagon.ai/api-reference"
    sandbox_base = "https://api.decagon.ai"

    @route("GET", "/v1/agents", writes=False)
    async def list_agents(self, request, **kw):
        return MockResponse(
            body={
                "agents": [
                    {
                        "id": "agt_mock_001",
                        "name": "Support Agent",
                        "status": "active",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "agt_mock_002",
                        "name": "Sales Concierge",
                        "status": "active",
                        "created_at": 1710400100,
                    },
                ],
            }
        )

    @route("GET", "/v1/agents/{id}", writes=False)
    async def get_agent(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "agt_mock_001",
                "name": "Support Agent",
                "status": "active",
                "created_at": 1710400000,
                "channel_types": ["chat", "email"],
            }
        )

    @route("GET", "/v1/conversations", writes=False)
    async def list_conversations(self, request, **kw):
        return MockResponse(
            body={
                "conversations": [
                    {
                        "id": "conv_mock_001",
                        "agent_id": "agt_mock_001",
                        "channel": "chat",
                        "status": "open",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "conv_mock_002",
                        "agent_id": "agt_mock_001",
                        "channel": "email",
                        "status": "closed",
                        "created_at": 1710401000,
                    },
                ],
            }
        )

    @route("GET", "/v1/conversations/{id}", writes=False)
    async def get_conversation(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "conv_mock_001",
                "agent_id": "agt_mock_001",
                "channel": "chat",
                "status": "open",
                "created_at": 1710400000,
                "user_id": "usr_mock_001",
            }
        )

    @route("GET", "/v1/conversations/{id}/messages", writes=False)
    async def list_messages(self, request, id="", **kw):
        return MockResponse(
            body={
                "messages": [
                    {
                        "id": "msg_mock_001",
                        "role": "user",
                        "content": "I need help with my order",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "msg_mock_002",
                        "role": "assistant",
                        "content": "I'd be happy to help.",
                        "created_at": 1710400001,
                    },
                ],
            }
        )

    @route("POST", "/v1/conversations")
    async def create_conversation(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "conv_mock_new",
                "agent_id": "agt_mock_001",
                "channel": "chat",
                "status": "open",
                "created_at": 1710400000,
            },
        )

    @route("POST", "/v1/conversations/{id}/messages")
    async def send_message(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": "msg_mock_verifiabl",
                "role": "assistant",
                "content": "Thanks for your message. How can I assist you?",
                "created_at": 1710400000,
            }
        )

    @route("GET", "/v1/users/{id}/memory", writes=False)
    async def get_user_memory(self, request, id="", **kw):
        return MockResponse(
            body={
                "user_id": id or "usr_mock_001",
                "preferences": {},
                "conversation_summary": None,
                "updated_at": 1710400000,
            }
        )

    @route("GET", "/v1/integrations", writes=False)
    async def list_integrations(self, request, **kw):
        return MockResponse(
            body={
                "integrations": [
                    {
                        "id": "int_mock_001",
                        "type": "slack",
                        "status": "connected",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "int_mock_002",
                        "type": "zendesk",
                        "status": "connected",
                        "created_at": 1710400100,
                    },
                ],
            }
        )
