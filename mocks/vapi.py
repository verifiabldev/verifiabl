# CHANGELOG: https://docs.vapi.ai/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.vapi.ai/api-reference
# SANDBOX:   https://dashboard.vapi.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _call(id_: str = "call_mock_verifiabl", assistant_id: str = "asst_mock_001"):
    return {
        "id": id_,
        "type": "webCall",
        "status": "ended",
        "assistantId": assistant_id,
        "createdAt": "2026-03-14T12:00:00.000Z",
        "updatedAt": "2026-03-14T12:05:00.000Z",
    }


def _assistant(id_: str = "asst_mock_001", name: str = "Support Agent"):
    return {
        "id": id_,
        "name": name,
        "createdAt": "2026-03-14T12:00:00.000Z",
        "updatedAt": "2026-03-14T12:00:00.000Z",
    }


class VapiMock(BaseMock):
    prefix = "/vapi"
    spec_url = "https://docs.vapi.ai/api-reference"
    sandbox_base = "https://api.vapi.ai"

    @route("GET", "/call", writes=False)
    async def list_calls(self, request, **kw):
        return MockResponse(body=[_call("call_mock_001"), _call("call_mock_002")])

    @route("POST", "/call")
    async def create_call(self, request, **kw):
        return MockResponse(status=201, body=_call("call_mock_new"))

    @route("GET", "/call/{id}", writes=False)
    async def get_call(self, request, id="", **kw):
        return MockResponse(body=_call(id or "call_mock_verifiabl"))

    @route("PATCH", "/call/{id}")
    async def update_call(self, request, id="", **kw):
        return MockResponse(body=_call(id or "call_mock_verifiabl"))

    @route("GET", "/assistant", writes=False)
    async def list_assistants(self, request, **kw):
        return MockResponse(
            body=[
                _assistant("asst_mock_001", "Support Agent"),
                _assistant("asst_mock_002", "Sales Bot"),
            ]
        )

    @route("POST", "/assistant")
    async def create_assistant(self, request, **kw):
        return MockResponse(status=201, body=_assistant("asst_mock_new", "New Assistant"))

    @route("GET", "/assistant/{id}", writes=False)
    async def get_assistant(self, request, id="", **kw):
        return MockResponse(body=_assistant(id or "asst_mock_001"))

    @route("PATCH", "/assistant/{id}")
    async def update_assistant(self, request, id="", **kw):
        return MockResponse(body=_assistant(id or "asst_mock_001"))

    @route("POST", "/chat")
    async def create_chat(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "chat_mock_verifiabl",
                "assistantId": "asst_mock_001",
                "createdAt": "2026-03-14T12:00:00.000Z",
            },
        )
