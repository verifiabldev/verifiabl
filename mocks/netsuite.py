# CHANGELOG: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_3798389663.html  (no RSS/atom feed as of 2026-03)
# SPEC:      https://system.netsuite.com/help/helpcenter/en_US/APIs/REST_API_Browser/record/v1/2025.2/index.html
# SANDBOX:   https://1234567.suitetalk.api.netsuite.com (account-specific)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _collection(items, base_href):
    return {
        "links": [{"rel": "self", "href": f"{base_href}?limit=1000&offset=0"}],
        "items": [
            {"links": [{"rel": "self", "href": f"{base_href}/{it['id']}"}], **it} for it in items
        ],
        "totalResults": len(items),
    }


class NetSuiteMock(BaseMock):
    prefix = "/netsuite"
    spec_url = "https://system.netsuite.com/help/helpcenter/en_US/APIs/REST_API_Browser/record/v1/2025.2/index.html"
    sandbox_base = "https://1234567.suitetalk.api.netsuite.com"

    @route("GET", "/services/rest/record/v1/metadata-catalog", writes=False)
    async def metadata_catalog(self, request, **kw):
        return MockResponse(
            body={"links": [], "items": [{"name": "customer"}, {"name": "salesOrder"}]}
        )

    @route("GET", "/services/rest/record/v1/customer", writes=False)
    async def list_customers(self, request, **kw):
        items = [
            {"id": "107", "companyName": "Acme Corp", "email": "acme@verifiabl.dev"},
            {"id": "108", "companyName": "Beta LLC", "email": "beta@verifiabl.dev"},
        ]
        return MockResponse(
            body=_collection(
                items, "https://1234567.suitetalk.api.netsuite.com/services/rest/record/v1/customer"
            )
        )

    @route("POST", "/services/rest/record/v1/customer")
    async def create_customer(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "109",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://1234567.suitetalk.api.netsuite.com/services/rest/record/v1/customer/109",
                    }
                ],
                "companyName": "New Customer",
            },
        )

    @route("GET", "/services/rest/record/v1/customer/{id}", writes=False)
    async def get_customer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id,
                "companyName": "Acme Corp",
                "email": "acme@verifiabl.dev",
                "entityId": "CUST-001",
            }
        )

    @route("GET", "/services/rest/record/v1/salesOrder", writes=False)
    async def list_sales_orders(self, request, **kw):
        items = [
            {"id": "1001", "tranId": "SO-001", "entity": {"id": "107"}},
            {"id": "1002", "tranId": "SO-002", "entity": {"id": "108"}},
        ]
        return MockResponse(
            body=_collection(
                items,
                "https://1234567.suitetalk.api.netsuite.com/services/rest/record/v1/salesOrder",
            )
        )

    @route("POST", "/services/rest/record/v1/salesOrder")
    async def create_sales_order(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "1003",
                "tranId": "SO-003",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://1234567.suitetalk.api.netsuite.com/services/rest/record/v1/salesOrder/1003",
                    }
                ],
            },
        )

    @route("GET", "/services/rest/record/v1/salesOrder/{id}", writes=False)
    async def get_sales_order(self, request, id="", **kw):
        return MockResponse(
            body={"id": id, "tranId": "SO-001", "entity": {"id": "107"}, "total": 2000}
        )

    @route("POST", "/services/rest/query/v1/suiteql", writes=False)
    async def suiteql(self, request, **kw):
        return MockResponse(
            body={
                "links": [
                    {
                        "rel": "self",
                        "href": "https://1234567.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql",
                    }
                ],
                "count": 2,
                "offset": 0,
                "totalResults": 2,
                "items": [
                    {"links": [], "id": "107", "companyname": "Acme Corp"},
                    {"links": [], "id": "108", "companyname": "Beta LLC"},
                ],
            }
        )
