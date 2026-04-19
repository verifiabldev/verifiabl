# CHANGELOG: https://meraki.io/whats-new/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/meraki/openapi
# SANDBOX:   https://dashboard.meraki.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class MerakiMock(BaseMock):
    prefix = "/meraki"
    spec_url = "https://github.com/meraki/openapi"
    sandbox_base = "https://api.meraki.com"

    @route("GET", "/api/v1/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "org_mock_001",
                    "name": "Mock Organization",
                    "url": "https://dashboard.meraki.com/o/abc/manage/overview",
                    "api": {"enabled": True},
                    "licensing": {"model": "co-term"},
                    "cloud": {
                        "region": {"name": "North America", "host": {"name": "United States"}}
                    },
                    "management": {"details": []},
                },
                {
                    "id": "org_mock_002",
                    "name": "Second Org",
                    "url": "https://dashboard.meraki.com/o/def/manage/overview",
                    "api": {"enabled": True},
                    "licensing": {"model": "per-device"},
                    "cloud": {
                        "region": {"name": "North America", "host": {"name": "United States"}}
                    },
                    "management": {"details": []},
                },
            ]
        )

    @route("GET", "/api/v1/organizations/{organizationId}", writes=False)
    async def get_organization(self, request, organizationId="", **kw):
        return MockResponse(
            body={
                "id": organizationId or "org_mock_001",
                "name": "Mock Organization",
                "url": "https://dashboard.meraki.com/o/abc/manage/overview",
                "api": {"enabled": True},
                "licensing": {"model": "co-term"},
                "cloud": {"region": {"name": "North America", "host": {"name": "United States"}}},
                "management": {"details": []},
            }
        )

    @route("GET", "/api/v1/organizations/{organizationId}/networks", writes=False)
    async def list_organization_networks(self, request, organizationId="", **kw):
        return MockResponse(
            body=[
                {
                    "id": "N_mock_001",
                    "organizationId": organizationId or "org_mock_001",
                    "name": "Main Office",
                    "productTypes": ["appliance", "switch", "wireless"],
                    "timeZone": "America/Los_Angeles",
                    "tags": [],
                    "url": "https://n1.meraki.com/n/N_mock_001/manage/nodes/list",
                    "notes": "",
                    "isBoundToConfigTemplate": False,
                },
                {
                    "id": "N_mock_002",
                    "organizationId": organizationId or "org_mock_001",
                    "name": "Branch",
                    "productTypes": ["wireless"],
                    "timeZone": "America/New_York",
                    "tags": [],
                    "url": "https://n1.meraki.com/n/N_mock_002/manage/nodes/list",
                    "notes": "",
                    "isBoundToConfigTemplate": False,
                },
            ]
        )

    @route("POST", "/api/v1/organizations/{organizationId}/networks")
    async def create_network(self, request, organizationId="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "N_mock_new",
                "organizationId": organizationId or "org_mock_001",
                "name": "New Network",
                "productTypes": ["appliance", "switch", "wireless"],
                "timeZone": "America/Los_Angeles",
                "tags": [],
                "url": "https://n1.meraki.com/n/N_mock_new/manage/nodes/list",
                "notes": "",
                "isBoundToConfigTemplate": False,
            },
        )

    @route("GET", "/api/v1/organizations/{organizationId}/devices", writes=False)
    async def list_organization_devices(self, request, organizationId="", **kw):
        return MockResponse(
            body=[
                {
                    "serial": "QBSB-VQ3J-XZ54",
                    "mac": "00:11:22:33:44:55",
                    "name": "MX64-Mock",
                    "model": "MX64",
                    "networkId": "N_mock_001",
                    "firmware": "wireless",
                    "lanIp": "192.168.1.1",
                },
                {
                    "serial": "ABCD-EF12-GH34",
                    "mac": "00:11:22:33:44:66",
                    "name": "MR33-Mock",
                    "model": "MR33",
                    "networkId": "N_mock_001",
                    "firmware": "wireless",
                    "lanIp": "192.168.1.2",
                },
            ]
        )

    @route("GET", "/api/v1/networks/{networkId}", writes=False)
    async def get_network(self, request, networkId="", **kw):
        return MockResponse(
            body={
                "id": networkId or "N_mock_001",
                "organizationId": "org_mock_001",
                "name": "Main Office",
                "productTypes": ["appliance", "switch", "wireless"],
                "timeZone": "America/Los_Angeles",
                "tags": [],
                "url": "https://n1.meraki.com/n/N_mock_001/manage/nodes/list",
                "notes": "",
                "isBoundToConfigTemplate": False,
            }
        )

    @route("PUT", "/api/v1/networks/{networkId}")
    async def update_network(self, request, networkId="", **kw):
        return MockResponse(
            body={
                "id": networkId or "N_mock_001",
                "organizationId": "org_mock_001",
                "name": "Main Office",
                "productTypes": ["appliance", "switch", "wireless"],
                "timeZone": "America/Los_Angeles",
                "tags": [],
                "url": "https://n1.meraki.com/n/N_mock_001/manage/nodes/list",
                "notes": "",
                "isBoundToConfigTemplate": False,
            }
        )

    @route("GET", "/api/v1/networks/{networkId}/devices", writes=False)
    async def list_network_devices(self, request, networkId="", **kw):
        return MockResponse(
            body=[
                {
                    "serial": "QBSB-VQ3J-XZ54",
                    "mac": "00:11:22:33:44:55",
                    "name": "MX64-Mock",
                    "model": "MX64",
                    "networkId": networkId or "N_mock_001",
                    "firmware": "wireless",
                    "lanIp": "192.168.1.1",
                },
                {
                    "serial": "ABCD-EF12-GH34",
                    "mac": "00:11:22:33:44:66",
                    "name": "MR33-Mock",
                    "model": "MR33",
                    "networkId": networkId or "N_mock_001",
                    "firmware": "wireless",
                    "lanIp": "192.168.1.2",
                },
            ]
        )
