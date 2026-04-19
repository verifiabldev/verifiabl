# CHANGELOG: https://api.slack.com/changelog/feed
# SKILL:     —
# MCP:       https://mcp.slack.com/mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class SlackMock(BaseMock):
    prefix = "/slack"
    spec_url = "https://api.slack.com/specs"
    sandbox_base = "https://slack.com"

    # -- read-like (POST but no state mutation) --

    @route("POST", "/api/api.test", writes=False)
    async def api_test(self, request, **kw):
        return MockResponse(body={"ok": True})

    @route("POST", "/api/auth.test", writes=False)
    async def auth_test(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "url": "https://verifiabl.slack.com/",
                "team": "verifiabl",
                "user": "mockbot",
                "team_id": "T_MOCK",
                "user_id": "U_MOCK",
            }
        )

    @route("POST", "/api/conversations.list", writes=False)
    async def conversations_list(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channels": [
                    {"id": "C_GENERAL", "name": "general", "is_channel": True, "num_members": 12},
                    {"id": "C_RANDOM", "name": "random", "is_channel": True, "num_members": 8},
                ],
            }
        )

    @route("POST", "/api/conversations.info", writes=False)
    async def conversations_info(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channel": {
                    "id": "C_GENERAL",
                    "name": "general",
                    "is_channel": True,
                    "topic": {"value": "Mock topic"},
                },
            }
        )

    @route("POST", "/api/conversations.history", writes=False)
    async def conversations_history(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "messages": [
                    {
                        "type": "message",
                        "user": "U_MOCK",
                        "text": "hello world",
                        "ts": "1710400000.000001",
                    },
                    {
                        "type": "message",
                        "user": "U_MOCK2",
                        "text": "hey there",
                        "ts": "1710400001.000002",
                    },
                ],
                "has_more": False,
            }
        )

    @route("POST", "/api/users.list", writes=False)
    async def users_list(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "members": [
                    {"id": "U_MOCK", "name": "mockbot", "real_name": "Mock Bot", "is_bot": True},
                    {
                        "id": "U_MOCK2",
                        "name": "alice",
                        "real_name": "Alice Verifiabl",
                        "is_bot": False,
                    },
                ],
            }
        )

    @route("POST", "/api/users.info", writes=False)
    async def users_info(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "user": {
                    "id": "U_MOCK",
                    "name": "mockbot",
                    "real_name": "Mock Bot",
                    "is_bot": True,
                },
            }
        )

    # -- true writes --

    @route("POST", "/api/chat.postMessage")
    async def post_message(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channel": "C_MOCK",
                "ts": "1710400000.000001",
                "message": {"text": "mock message", "type": "message"},
            }
        )

    @route("POST", "/api/chat.update")
    async def chat_update(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channel": "C_MOCK",
                "ts": "1710400000.000001",
                "text": "updated message",
            }
        )

    @route("POST", "/api/chat.delete")
    async def chat_delete(self, request, **kw):
        return MockResponse(body={"ok": True, "channel": "C_MOCK", "ts": "1710400000.000001"})

    @route("POST", "/api/conversations.create")
    async def conversations_create(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channel": {"id": "C_NEW", "name": "new-channel", "is_channel": True},
            }
        )

    @route("POST", "/api/conversations.join")
    async def conversations_join(self, request, **kw):
        return MockResponse(
            body={
                "ok": True,
                "channel": {"id": "C_GENERAL", "name": "general", "is_channel": True},
            }
        )

    @route("POST", "/api/reactions.add")
    async def reactions_add(self, request, **kw):
        return MockResponse(body={"ok": True})
