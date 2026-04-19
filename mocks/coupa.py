# CHANGELOG: https://compass.coupa.com/en-us/products/product-documentation/integration-technical-documentation/the-coupa-core-api (no RSS/atom feed as of 2026-03)
# SPEC:      https://compass.coupa.com/en-us/products/product-documentation/integration-technical-documentation/the-coupa-core-api
# SANDBOX:   https://www.coupa.com (instance-specific: https://{instance}/api/)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class CoupaMock(BaseMock):
    prefix = "/coupa"
    spec_url = "https://compass.coupa.com/en-us/products/product-documentation/integration-technical-documentation/the-coupa-core-api"
    sandbox_base = "https://instance.coupa.com"

    @route("GET", "/api/suppliers", writes=False)
    async def list_suppliers(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 1001,
                    "name": "Acme Supplies",
                    "number": "SUP001",
                    "status": "active",
                    "created-at": "2024-01-15T10:00:00+00:00",
                },
                {
                    "id": 1002,
                    "name": "Globex Corp",
                    "number": "SUP002",
                    "status": "active",
                    "created-at": "2024-02-20T14:30:00+00:00",
                },
            ]
        )

    @route("GET", "/api/suppliers/{id}", writes=False)
    async def get_supplier(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1001,
                "name": "Acme Supplies",
                "number": "SUP001",
                "display-name": "Acme Supplies",
                "account-number": "ACC001",
                "status": "active",
                "supplier-status": "active",
                "created-at": "2024-01-15T10:00:00+00:00",
                "updated-at": "2024-03-01T09:00:00+00:00",
            }
        )

    @route("POST", "/api/suppliers")
    async def create_supplier(self, request, **kw):
        return MockResponse(status=201, body={"id": 1003, "number": "SUP003"})

    @route("PUT", "/api/suppliers/{id}")
    async def update_supplier(self, request, id="", **kw):
        return MockResponse(body={"id": int(id) if id.isdigit() else 1001})

    @route("GET", "/api/invoices", writes=False)
    async def list_invoices(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 2001,
                    "invoice-number": "INV001",
                    "status": "approved",
                    "total": "1500.00",
                    "created-at": "2024-03-01T08:00:00+00:00",
                },
                {
                    "id": 2002,
                    "invoice-number": "INV002",
                    "status": "pending_approval",
                    "total": "2200.50",
                    "created-at": "2024-03-05T11:00:00+00:00",
                },
            ]
        )

    @route("GET", "/api/invoices/{id}", writes=False)
    async def get_invoice(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 2001,
                "invoice-number": "INV001",
                "status": "approved",
                "total": "1500.00",
                "currency": {"code": "USD"},
                "created-at": "2024-03-01T08:00:00+00:00",
                "updated-at": "2024-03-02T12:00:00+00:00",
            }
        )

    @route("POST", "/api/invoices")
    async def create_invoice(self, request, **kw):
        return MockResponse(
            status=201, body={"id": 2003, "invoice-number": "INV003", "status": "draft"}
        )

    @route("GET", "/api/purchase_orders", writes=False)
    async def list_purchase_orders(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 3001,
                    "po-number": "PO001",
                    "status": "issued",
                    "total": "5000.00",
                    "created-at": "2024-02-10T09:00:00+00:00",
                },
                {
                    "id": 3002,
                    "po-number": "PO002",
                    "status": "draft",
                    "total": "1200.00",
                    "created-at": "2024-03-10T14:00:00+00:00",
                },
            ]
        )

    @route("GET", "/api/purchase_orders/{id}", writes=False)
    async def get_purchase_order(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 3001,
                "po-number": "PO001",
                "status": "issued",
                "total": "5000.00",
                "currency": {"code": "USD"},
                "supplier": {"id": 1001, "name": "Acme Supplies"},
                "created-at": "2024-02-10T09:00:00+00:00",
                "updated-at": "2024-02-11T10:00:00+00:00",
            }
        )

    @route("POST", "/api/purchase_orders")
    async def create_purchase_order(self, request, **kw):
        return MockResponse(status=201, body={"id": 3003, "po-number": "PO003", "status": "draft"})
