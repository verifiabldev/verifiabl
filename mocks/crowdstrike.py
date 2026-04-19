# CHANGELOG: https://developer.crowdstrike.com/blog/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.crowdstrike.com/docs/openapi
# SANDBOX:   https://falcon.crowdstrike.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_DEVICE = {
    "device_id": "dev_mock_verifiabl",
    "hostname": "mock-host-01",
    "platform_name": "Windows",
    "status": "normal",
    "last_seen": "2024-03-14T12:00:00Z",
    "first_seen": "2024-01-01T00:00:00Z",
    "local_ip": "10.0.0.1",
    "external_ip": "203.0.113.1",
    "machine_domain": "verifiabl.dev",
    "os_version": "Windows 11",
}
_DETECT = {
    "detection_id": "det_mock_001",
    "severity": 2,
    "status": "new",
    "created_timestamp": "2024-03-14T11:00:00Z",
    "max_confidence": 90,
    "tactic": "Execution",
    "technique": "Command and Scripting Interpreter",
}


def _body(resources, errors=None):
    return {"resources": resources, "errors": errors or []}


class CrowdstrikeMock(BaseMock):
    prefix = "/crowdstrike"
    spec_url = "https://developer.crowdstrike.com/docs/openapi"
    sandbox_base = "https://api.crowdstrike.com"

    @route("GET", "/devices/combined/devices/v1", writes=False)
    async def combined_devices(self, request, **kw):
        return MockResponse(
            body=_body(
                [
                    _DEVICE,
                    {**_DEVICE, "device_id": "dev_mock_002", "hostname": "mock-host-02"},
                ]
            )
        )

    @route("GET", "/devices/queries/devices/v1", writes=False)
    async def query_devices(self, request, **kw):
        return MockResponse(body=_body(["dev_mock_verifiabl", "dev_mock_002"]))

    @route("POST", "/devices/entities/devices/v2", writes=False)
    async def get_device_details(self, request, **kw):
        return MockResponse(
            body=_body(
                [
                    _DEVICE,
                    {**_DEVICE, "device_id": "dev_mock_002", "hostname": "mock-host-02"},
                ]
            )
        )

    @route("POST", "/devices/entities/devices-actions/v2")
    async def device_action(self, request, **kw):
        return MockResponse(body=_body([{"id": "dev_mock_verifiabl"}]))

    @route("POST", "/detects/queries/detects/v1", writes=False)
    async def query_detects(self, request, **kw):
        return MockResponse(body=_body(["det_mock_001", "det_mock_002"]))

    @route("POST", "/detects/entities/summaries/GET/v1", writes=False)
    async def get_detect_summaries(self, request, **kw):
        return MockResponse(
            body=_body(
                [
                    _DETECT,
                    {**_DETECT, "detection_id": "det_mock_002", "severity": 1},
                ]
            )
        )
