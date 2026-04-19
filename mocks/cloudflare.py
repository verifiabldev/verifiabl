# CHANGELOG: https://developers.cloudflare.com/changelog/rss/index.xml
# SPEC:      https://github.com/cloudflare/api-schemas
# SANDBOX:   https://dash.cloudflare.com
# SKILL:     —
# MCP:       https://docs.mcp.cloudflare.com/mcp
# LLMS:      https://developers.cloudflare.com/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


def _envelope(result, result_info=None):
    out = {"success": True, "result": result, "errors": [], "messages": []}
    if result_info is not None:
        out["result_info"] = result_info
    return out


class CloudflareMock(BaseMock):
    prefix = "/cloudflare"
    spec_url = "https://github.com/cloudflare/api-schemas"
    sandbox_base = "https://api.cloudflare.com/client/v4"

    @route("GET", "/client/v4/zones", writes=False)
    async def list_zones(self, request, **kw):
        return MockResponse(
            body=_envelope(
                [
                    {
                        "id": "zone_mock_001",
                        "name": "verifiabl.dev",
                        "status": "active",
                        "paused": False,
                        "type": "full",
                        "development_mode": 0,
                        "name_servers": ["ns1.cloudflare.com", "ns2.cloudflare.com"],
                        "created_on": "2014-01-01T05:20:00.12345Z",
                        "modified_on": "2014-01-01T05:20:00.12345Z",
                        "account": {"id": "acct_mock_001", "name": "Mock Account"},
                    },
                    {
                        "id": "zone_mock_002",
                        "name": "test.verifiabl.dev",
                        "status": "active",
                        "paused": False,
                        "type": "full",
                        "development_mode": 0,
                        "name_servers": ["ns1.cloudflare.com", "ns2.cloudflare.com"],
                        "created_on": "2014-01-01T05:20:00.12345Z",
                        "modified_on": "2014-01-01T05:20:00.12345Z",
                        "account": {"id": "acct_mock_001", "name": "Mock Account"},
                    },
                ],
                {"count": 2, "page": 1, "per_page": 20, "total_count": 2},
            )
        )

    @route("GET", "/client/v4/zones/{zone_id}", writes=False)
    async def get_zone(self, request, zone_id="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "id": zone_id or "zone_mock_001",
                    "name": "verifiabl.dev",
                    "status": "active",
                    "paused": False,
                    "type": "full",
                    "development_mode": 0,
                    "name_servers": ["ns1.cloudflare.com", "ns2.cloudflare.com"],
                    "created_on": "2014-01-01T05:20:00.12345Z",
                    "modified_on": "2014-01-01T05:20:00.12345Z",
                    "account": {"id": "acct_mock_001", "name": "Mock Account"},
                }
            )
        )

    @route("GET", "/client/v4/zones/{zone_id}/dns_records", writes=False)
    async def list_dns_records(self, request, zone_id="", **kw):
        return MockResponse(
            body=_envelope(
                [
                    {
                        "id": "rec_mock_001",
                        "zone_id": zone_id or "zone_mock_001",
                        "zone_name": "verifiabl.dev",
                        "name": "verifiabl.dev",
                        "type": "A",
                        "content": "198.51.100.4",
                        "ttl": 3600,
                        "proxied": True,
                        "created_on": "2014-01-01T05:20:00.12345Z",
                        "modified_on": "2014-01-01T05:20:00.12345Z",
                    },
                    {
                        "id": "rec_mock_002",
                        "zone_id": zone_id or "zone_mock_001",
                        "zone_name": "verifiabl.dev",
                        "name": "www.verifiabl.dev",
                        "type": "CNAME",
                        "content": "verifiabl.dev",
                        "ttl": 3600,
                        "proxied": True,
                        "created_on": "2014-01-01T05:20:00.12345Z",
                        "modified_on": "2014-01-01T05:20:00.12345Z",
                    },
                ],
                {"count": 2, "page": 1, "per_page": 20, "total_count": 2},
            )
        )

    @route("POST", "/client/v4/zones/{zone_id}/dns_records")
    async def create_dns_record(self, request, zone_id="", **kw):
        return MockResponse(
            status=201,
            body=_envelope(
                {
                    "id": "rec_mock_new",
                    "zone_id": zone_id or "zone_mock_001",
                    "zone_name": "verifiabl.dev",
                    "name": "api.verifiabl.dev",
                    "type": "A",
                    "content": "198.51.100.5",
                    "ttl": 3600,
                    "proxied": False,
                    "created_on": "2014-01-01T05:20:00.12345Z",
                    "modified_on": "2014-01-01T05:20:00.12345Z",
                }
            ),
        )

    @route("GET", "/client/v4/zones/{zone_id}/dns_records/{record_id}", writes=False)
    async def get_dns_record(self, request, zone_id="", record_id="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "id": record_id or "rec_mock_001",
                    "zone_id": zone_id or "zone_mock_001",
                    "zone_name": "verifiabl.dev",
                    "name": "verifiabl.dev",
                    "type": "A",
                    "content": "198.51.100.4",
                    "ttl": 3600,
                    "proxied": True,
                    "created_on": "2014-01-01T05:20:00.12345Z",
                    "modified_on": "2014-01-01T05:20:00.12345Z",
                }
            )
        )

    @route("PUT", "/client/v4/zones/{zone_id}/dns_records/{record_id}")
    async def update_dns_record(self, request, zone_id="", record_id="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "id": record_id or "rec_mock_001",
                    "zone_id": zone_id or "zone_mock_001",
                    "zone_name": "verifiabl.dev",
                    "name": "verifiabl.dev",
                    "type": "A",
                    "content": "198.51.100.6",
                    "ttl": 300,
                    "proxied": True,
                    "created_on": "2014-01-01T05:20:00.12345Z",
                    "modified_on": "2014-01-01T05:20:00.12345Z",
                }
            )
        )

    @route("DELETE", "/client/v4/zones/{zone_id}/dns_records/{record_id}")
    async def delete_dns_record(self, request, zone_id="", record_id="", **kw):
        return MockResponse(body=_envelope({"id": record_id or "rec_mock_001"}))
