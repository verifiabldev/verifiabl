# CHANGELOG: https://docs.synthflow.ai/api-reference/resources/api-changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.synthflow.ai/api-reference
# SANDBOX:   https://app.synthflow.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per OpenAPI securitySchemes)
from mocks.base import BaseMock, route
from models import MockResponse


def _agent(
    model_id: str = "model_mock_verifiabl",
    name: str = "Support Agent",
    agent_type: str = "outbound",
):
    return {
        "model_id": model_id,
        "name": name,
        "type": agent_type,
        "timezone": "America/New_York",
    }


def _list_assistants_body():
    return {
        "status": "success",
        "response": {
            "pagination": {"total_records": 2, "limit": 20, "offset": 0},
            "assistants": [
                _agent("model_mock_001", "Support Agent", "inbound"),
                _agent("model_mock_002", "Sales Bot", "outbound"),
            ],
        },
    }


def _call(call_id: str = "call_mock_verifiabl", model_id: str = "model_mock_001"):
    return {
        "call_id": call_id,
        "model_id": model_id,
        "duration": 120,
        "call_status": "completed",
        "type_of_call": "outbound",
        "transcript": "Agent: Hello. Human: Hi.",
        "start_time": "1710400000000",
        "phone_number_to": "+15551234567",
        "lead_name": "Jane",
    }


def _list_calls_body():
    return {
        "status": "success",
        "response": {
            "pagination": {"total_records": 2, "limit": 20, "offset": 0},
            "calls": [_call("call_mock_001"), _call("call_mock_002")],
        },
    }


# LOC EXCEPTION: status/response/pagination envelope plus assistants and calls resources require helper bodies.
class SynthflowMock(BaseMock):
    prefix = "/synthflow"
    spec_url = "https://docs.synthflow.ai/api-reference"
    sandbox_base = "https://api.synthflow.ai"

    @route("GET", "/assistants", writes=False)
    async def list_assistants(self, request, **kw):
        return MockResponse(body=_list_assistants_body())

    @route("GET", "/assistants/", writes=False)
    async def list_assistants_slash(self, request, **kw):
        return MockResponse(body=_list_assistants_body())

    @route("POST", "/assistants")
    async def create_assistant(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "status": "success",
                "response": {"model_id": "model_mock_new"},
                "details": {"phone": None, "voice": "eleven_turbo_v2"},
            },
        )

    @route("GET", "/assistants/{model_id}", writes=False)
    async def get_assistant(self, request, model_id="", **kw):
        return MockResponse(
            body={
                "status": "success",
                "response": _agent(model_id or "model_mock_001"),
            }
        )

    @route("PUT", "/assistants/{model_id}")
    async def update_assistant(self, request, model_id="", **kw):
        return MockResponse(
            body={
                "status": "success",
                "response": _agent(model_id or "model_mock_001"),
            }
        )

    @route("GET", "/calls", writes=False)
    async def list_calls(self, request, **kw):
        return MockResponse(body=_list_calls_body())

    @route("POST", "/calls")
    async def create_call(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "status": "success",
                "response": {"call_id": "call_mock_new", "answer": "ringing"},
                "eta": 5,
            },
        )

    @route("GET", "/calls/{call_id}", writes=False)
    async def get_call(self, request, call_id="", **kw):
        return MockResponse(
            body={
                "status": "success",
                "response": {
                    "pagination": {"total_records": 1, "limit": 20, "offset": 0},
                    "calls": [_call(call_id or "call_mock_verifiabl")],
                },
            }
        )
