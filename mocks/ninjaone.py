# CHANGELOG: https://app.ninjarmm.com/apidocs-beta/upcoming-changes  (no RSS/atom feed as of 2026-03)
# SPEC:      https://app.ninjarmm.com/apidocs/NinjaRMM-API-v2.json
# SANDBOX:   https://app.ninjarmm.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (OAuth 2.0 client credentials)
from mocks.base import BaseMock, route
from models import MockResponse


def _org_brief(id_: int, name: str):
    return {
        "id": id_,
        "name": name,
        "description": None,
        "userData": {},
        "nodeApprovalMode": "AUTOMATIC",
    }


def _device(id_: int, org_id: int, system_name: str, node_class: str = "WINDOWS_WORKSTATION"):
    return {
        "id": id_,
        "uid": "550e8400-e29b-41d4-a716-446655440000",
        "organizationId": org_id,
        "locationId": 1,
        "nodeClass": node_class,
        "displayName": system_name,
        "systemName": system_name,
        "approvalStatus": "APPROVED",
        "offline": False,
        "created": 1710400000.0,
        "lastContact": 1710400000.0,
        "tags": [],
    }


# LOC EXCEPTION: 13 schema-faithful RMM endpoints (devices, policies, orgs, alerts) with shared device/org helpers.
class NinjaOneMock(BaseMock):
    prefix = "/ninjaone"
    spec_url = "https://app.ninjarmm.com/apidocs/NinjaRMM-API-v2.json"
    sandbox_base = "https://app.ninjarmm.com"

    @route("GET", "/v2/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body=[
                _org_brief(1, "Mock Organization"),
                _org_brief(2, "Second Org"),
            ]
        )

    @route("GET", "/v2/organization/{id}", writes=False)
    async def get_organization(self, request, id="", **kw):
        oid = int(id) if id and id.isdigit() else 1
        return MockResponse(
            body={
                **_org_brief(oid, "Mock Organization"),
                "locations": [
                    {
                        "id": 1,
                        "name": "Main Office",
                        "address": "123 Main St",
                        "description": None,
                        "userData": {},
                    }
                ],
                "policies": [{"nodeRoleId": 1, "policyId": 1}],
            }
        )

    @route("GET", "/v2/organization/{id}/devices", writes=False)
    async def list_organization_devices(self, request, id="", **kw):
        oid = int(id) if id and id.isdigit() else 1
        return MockResponse(
            body=[
                _device(101, oid, "WORKSTATION-MOCK-01"),
                _device(102, oid, "WORKSTATION-MOCK-02"),
            ]
        )

    @route("GET", "/v2/devices", writes=False)
    async def list_devices(self, request, **kw):
        return MockResponse(
            body=[
                _device(101, 1, "WORKSTATION-MOCK-01"),
                _device(102, 1, "WORKSTATION-MOCK-02"),
            ]
        )

    @route("GET", "/v2/device/{id}", writes=False)
    async def get_device(self, request, id="", **kw):
        did = int(id) if id and id.isdigit() else 101
        return MockResponse(body=_device(did, 1, "WORKSTATION-MOCK-01"))

    @route("GET", "/v2/policies", writes=False)
    async def list_policies(self, request, **kw):
        return MockResponse(
            body=[
                {"id": 1, "name": "Default Policy", "description": "Default endpoint policy"},
                {"id": 2, "name": "Workstation Policy", "description": "Workstation policy"},
            ]
        )

    @route("GET", "/v2/alerts", writes=False)
    async def list_alerts(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "uid": "alert_mock_001",
                    "deviceId": 101,
                    "conditionName": "High CPU",
                    "severity": "warning",
                    "triggeredAt": 1710400000.0,
                },
            ]
        )

    @route("GET", "/v2/activities", writes=False)
    async def list_activities(self, request, **kw):
        return MockResponse(
            body=[
                {"id": 1, "deviceId": 101, "activityType": "CHECK_IN", "timestamp": 1710400000.0},
                {"id": 2, "deviceId": 102, "activityType": "CHECK_IN", "timestamp": 1710400001.0},
            ]
        )

    @route("GET", "/v2/groups", writes=False)
    async def list_groups(self, request, **kw):
        return MockResponse(
            body=[
                {"id": 1, "name": "All Workstations", "description": "Saved search"},
                {"id": 2, "name": "Servers", "description": "Server devices"},
            ]
        )

    @route("GET", "/v2/locations", writes=False)
    async def list_locations(self, request, **kw):
        return MockResponse(
            body=[
                {"id": 1, "name": "Main Office", "address": "123 Main St", "organizationId": 1},
                {"id": 2, "name": "Branch", "address": "456 Branch Ave", "organizationId": 1},
            ]
        )

    @route("PATCH", "/v2/device/{id}")
    async def update_device(self, request, id="", **kw):
        did = int(id) if id and id.isdigit() else 101
        return MockResponse(body=_device(did, 1, "WORKSTATION-MOCK-01"))

    @route("POST", "/v2/organizations")
    async def create_organization(self, request, **kw):
        return MockResponse(status=201, body=_org_brief(3, "New Organization"))

    @route("PUT", "/v2/organization/{id}/policies")
    async def update_organization_policies(self, request, id="", **kw):
        return MockResponse(body={"id": int(id) if id and id.isdigit() else 1})
