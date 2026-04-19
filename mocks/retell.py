# CHANGELOG: https://www.retellai.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.retellai.com/api-references
# SANDBOX:   https://dashboard.retellai.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per docs.retellai.com/accounts/api-keys-overview)
from mocks.base import BaseMock, route
from models import MockResponse


def _agent(
    agent_id: str = "agent_mock_verifiabl", version: int = 0, agent_name: str = "Support Agent"
):
    return {
        "agent_id": agent_id,
        "version": version,
        "is_published": False,
        "response_engine": {"type": "retell-llm", "llm_id": "llm_mock_001", "version": 0},
        "voice_id": "retell-Cimo",
        "agent_name": agent_name,
        "last_modification_timestamp": 1710400000000,
    }


def _call(
    call_id: str = "call_mock_verifiabl",
    agent_id: str = "agent_mock_001",
    call_type: str = "web_call",
):
    base = {
        "call_id": call_id,
        "agent_id": agent_id,
        "agent_version": 0,
        "call_status": "ended",
        "agent_name": "Support Agent",
        "metadata": {},
        "start_timestamp": 1710400000000,
        "end_timestamp": 1710400060000,
        "duration_ms": 60000,
    }
    if call_type == "web_call":
        base["call_type"] = "web_call"
        base["access_token"] = "mock_access_token_verifiabl"
    else:
        base["call_type"] = "phone_call"
        base["from_number"] = "+12137771234"
        base["to_number"] = "+12137771235"
        base["direction"] = "outbound"
    return base


# LOC EXCEPTION: 9 routes with schema-faithful agent/call (web vs phone) and get-agent-versions/list bodies.
class RetellMock(BaseMock):
    prefix = "/retell"
    spec_url = "https://docs.retellai.com/api-references"
    sandbox_base = "https://api.retellai.com"

    @route("GET", "/list-agents", writes=False)
    async def list_agents(self, request, **kw):
        return MockResponse(
            body=[
                _agent("agent_mock_001", 0, "Support Agent"),
                _agent("agent_mock_002", 0, "Sales Bot"),
            ]
        )

    @route("POST", "/create-agent")
    async def create_agent(self, request, **kw):
        return MockResponse(status=201, body=_agent("agent_mock_new", 0, "New Agent"))

    @route("GET", "/get-agent-versions/{agent_id}", writes=False)
    async def get_agent_versions(self, request, agent_id="", **kw):
        return MockResponse(
            body=[
                {"agent_id": agent_id or "agent_mock_001", "version": 1, "is_published": True},
                {"agent_id": agent_id or "agent_mock_001", "version": 0, "is_published": False},
            ]
        )

    @route("GET", "/v2/get-call/{call_id}", writes=False)
    async def get_call(self, request, call_id="", **kw):
        return MockResponse(
            body=_call(call_id or "call_mock_verifiabl", "agent_mock_001", "web_call")
        )

    @route("POST", "/v2/list-calls", writes=False)
    async def list_calls(self, request, **kw):
        return MockResponse(
            body=[
                _call("call_mock_001", "agent_mock_001", "web_call"),
                _call("call_mock_002", "agent_mock_001", "phone_call"),
            ]
        )

    @route("POST", "/v2/create-phone-call")
    async def create_phone_call(self, request, **kw):
        return MockResponse(status=201, body=_call("call_mock_new", "agent_mock_001", "phone_call"))

    @route("POST", "/v2/create-web-call")
    async def create_web_call(self, request, **kw):
        return MockResponse(status=201, body=_call("call_mock_new", "agent_mock_001", "web_call"))

    @route("PATCH", "/v2/update-call/{call_id}")
    async def update_call(self, request, call_id="", **kw):
        return MockResponse(
            body=_call(call_id or "call_mock_verifiabl", "agent_mock_001", "web_call")
        )

    @route("GET", "/get-retell-llm/{llm_id}", writes=False)
    async def get_retell_llm(self, request, llm_id="", **kw):
        return MockResponse(
            body={
                "llm_id": llm_id or "llm_mock_001",
                "version": 0,
                "is_published": False,
                "model": "gpt-4o-mini",
                "general_prompt": "You are a helpful voice agent.",
            }
        )
