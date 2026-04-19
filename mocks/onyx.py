# CHANGELOG: https://docs.onyx.app/changelog.md (no RSS/atom feed as of 2026-03)
# SPEC:      https://cloud.onyx.app/api/openapi.json
# SANDBOX:   https://cloud.onyx.app/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class OnyxMock(BaseMock):
    prefix = "/onyx"
    spec_url = "https://cloud.onyx.app/api/openapi.json"
    sandbox_base = "https://cloud.onyx.app/api"

    @route("GET", "/agents", writes=False)
    async def get_agents(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": 1,
                        "name": "Default Assistant",
                        "description": "General purpose agent",
                        "tools": [],
                        "starter_messages": None,
                        "llm_relevance_filter": False,
                        "llm_filter_extraction": False,
                        "document_sets": [],
                        "llm_model_version_override": None,
                        "llm_model_provider_override": None,
                        "uploaded_image_id": None,
                        "icon_name": "default",
                        "is_public": True,
                        "is_visible": True,
                        "display_priority": 0,
                        "is_default_persona": True,
                        "builtin_persona": True,
                        "labels": [],
                        "owner": None,
                    },
                    {
                        "id": 2,
                        "name": "Sales Agent",
                        "description": "CRM and pipeline agent",
                        "tools": [
                            {
                                "id": 1,
                                "name": "search",
                                "description": "Search",
                                "definition": None,
                                "display_name": "Search",
                                "in_code_tool_id": None,
                                "custom_headers": None,
                                "passthrough_auth": False,
                            }
                        ],
                        "starter_messages": [{"name": "Intro", "message": "How can I help?"}],
                        "llm_relevance_filter": True,
                        "llm_filter_extraction": False,
                        "document_sets": [
                            {
                                "id": 1,
                                "name": "Sales",
                                "description": None,
                                "cc_pair_summaries": [],
                                "is_up_to_date": True,
                                "is_public": True,
                                "users": [],
                                "groups": [],
                                "federated_connector_summaries": [],
                            }
                        ],
                        "llm_model_version_override": None,
                        "llm_model_provider_override": None,
                        "uploaded_image_id": None,
                        "icon_name": "briefcase",
                        "is_public": True,
                        "is_visible": True,
                        "display_priority": 1,
                        "is_default_persona": False,
                        "builtin_persona": False,
                        "labels": [{"id": 1, "name": "sales"}],
                        "owner": {"id": "user_mock_001", "email": "admin@verifiabl.dev"},
                    },
                ],
                "total_items": 2,
            }
        )

    @route("GET", "/persona/{persona_id}", writes=False)
    async def get_persona(self, request, persona_id="", **kw):
        return MockResponse(
            body={
                "id": int(persona_id or "1"),
                "name": "Default Assistant",
                "description": "General purpose agent",
                "is_public": True,
                "is_visible": True,
                "uploaded_image_id": None,
                "icon_name": "default",
                "user_file_ids": [],
                "display_priority": 0,
                "is_default_persona": True,
                "builtin_persona": True,
                "starter_messages": None,
                "llm_relevance_filter": False,
                "llm_filter_extraction": False,
                "tools": [],
                "labels": [],
                "owner": None,
                "users": [],
                "groups": [],
                "document_sets": [],
                "llm_model_provider_override": None,
                "llm_model_version_override": None,
                "num_chunks": None,
                "system_prompt": None,
                "replace_base_system_prompt": False,
                "task_prompt": None,
                "datetime_aware": True,
                "search_start_date": None,
            }
        )

    @route("GET", "/chat/get-user-chat-sessions", writes=False)
    async def get_user_chat_sessions(self, request, **kw):
        return MockResponse(
            body={
                "sessions": [
                    {
                        "id": "session_mock_001",
                        "name": "Product questions",
                        "persona_id": 1,
                        "time_created": "2026-03-14T12:00:00Z",
                        "time_updated": "2026-03-14T12:05:00Z",
                        "shared_status": "private",
                        "current_alternate_model": None,
                        "current_temperature_override": None,
                    },
                    {
                        "id": "session_mock_002",
                        "name": "Support thread",
                        "persona_id": 2,
                        "time_created": "2026-03-13T10:00:00Z",
                        "time_updated": "2026-03-13T10:30:00Z",
                        "shared_status": "private",
                        "current_alternate_model": None,
                        "current_temperature_override": None,
                    },
                ],
            }
        )

    @route("GET", "/chat/get-chat-session/{session_id}", writes=False)
    async def get_chat_session(self, request, session_id="", **kw):
        return MockResponse(
            body={
                "chat_session_id": session_id or "session_mock_001",
                "description": None,
                "persona_id": 1,
                "persona_name": "Default Assistant",
                "personal_icon_name": "default",
                "messages": [
                    {
                        "chat_session_id": session_id or "session_mock_001",
                        "message_id": 1,
                        "parent_message": None,
                        "latest_child_message": None,
                        "message": "Hello",
                        "reasoning_tokens": None,
                        "message_type": "user",
                        "context_docs": None,
                        "citations": None,
                        "time_sent": "2026-03-14T12:00:00Z",
                        "files": [],
                        "error": None,
                    },
                    {
                        "chat_session_id": session_id or "session_mock_001",
                        "message_id": 2,
                        "parent_message": 1,
                        "latest_child_message": None,
                        "message": "Hi, how can I help?",
                        "reasoning_tokens": None,
                        "message_type": "assistant",
                        "context_docs": None,
                        "citations": None,
                        "time_sent": "2026-03-14T12:00:05Z",
                        "files": [],
                        "error": None,
                    },
                ],
                "time_created": "2026-03-14T12:00:00Z",
                "shared_status": "private",
                "current_alternate_model": None,
                "current_temperature_override": None,
                "deleted": False,
                "packets": [],
            }
        )

    @route("POST", "/chat/create-chat-session")
    async def create_chat_session(self, request, **kw):
        return MockResponse(body={"chat_session_id": "session_mock_new"})

    @route("POST", "/chat/send-chat-message")
    async def send_chat_message(self, request, **kw):
        return MockResponse(
            body={
                "chat_session_id": "session_mock_001",
                "message_id": 3,
                "answer": "Mock response from Onyx.",
                "citations": {},
                "message": "Mock response from Onyx.",
            }
        )

    @route("DELETE", "/chat/delete-chat-session/{session_id}")
    async def delete_chat_session(self, request, session_id="", **kw):
        return MockResponse(status=200, body={})

    @route("GET", "/tool", writes=False)
    async def list_tools(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 1,
                    "name": "search",
                    "description": "Search knowledge base",
                    "display_name": "Search",
                    "enabled": True,
                },
                {
                    "id": 2,
                    "name": "web_search",
                    "description": "Web search",
                    "display_name": "Web Search",
                    "enabled": True,
                },
            ]
        )

    @route("GET", "/tool/{tool_id}", writes=False)
    async def get_tool(self, request, tool_id="", **kw):
        return MockResponse(
            body={
                "id": int(tool_id or "1"),
                "name": "search",
                "description": "Search knowledge base",
                "display_name": "Search",
                "definition": {},
                "enabled": True,
                "in_code_tool_id": "search",
            }
        )
