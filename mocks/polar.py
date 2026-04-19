# CHANGELOG: https://polar.sh/docs/changelog/api.md (no RSS/atom feed as of 2026-03)
# SPEC:      https://polar.sh/docs/openapi.yaml
# SANDBOX:   https://sandbox.polar.sh
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _paginated(items: list, total: int = 2, max_page: int = 1):
    return {"items": items, "pagination": {"total_count": total, "max_page": max_page}}


class PolarMock(BaseMock):
    prefix = "/polar"
    spec_url = "https://polar.sh/docs/openapi.yaml"
    sandbox_base = "https://sandbox-api.polar.sh"

    @route("GET", "/v1/organizations/", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "org_mock_001",
                        "name": "Acme Corp",
                        "slug": "acme",
                        "created_at": "2025-01-15T12:00:00Z",
                        "modified_at": None,
                    },
                    {
                        "id": "org_mock_002",
                        "name": "Globex",
                        "slug": "globex",
                        "created_at": "2025-01-16T12:00:00Z",
                        "modified_at": None,
                    },
                ]
            )
        )

    @route("GET", "/v1/organizations/{id}", writes=False)
    async def get_organization(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "org_mock_001",
                "name": "Acme Corp",
                "slug": "acme",
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
                "avatar_url": None,
            }
        )

    @route("GET", "/v1/products/", writes=False)
    async def list_products(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "prod_mock_001",
                        "name": "Pro Plan",
                        "description": "Monthly subscription",
                        "is_recurring": True,
                        "created_at": "2025-01-15T12:00:00Z",
                        "modified_at": None,
                    },
                    {
                        "id": "prod_mock_002",
                        "name": "Lifetime License",
                        "description": "One-time purchase",
                        "is_recurring": False,
                        "created_at": "2025-01-16T12:00:00Z",
                        "modified_at": None,
                    },
                ]
            )
        )

    @route("GET", "/v1/products/{id}", writes=False)
    async def get_product(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "prod_mock_001",
                "name": "Pro Plan",
                "description": "Monthly subscription",
                "is_recurring": True,
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
            }
        )

    @route("POST", "/v1/products/")
    async def create_product(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "prod_mock_new",
                "name": "New Product",
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
            },
        )

    @route("GET", "/v1/orders/", writes=False)
    async def list_orders(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "ord_mock_001",
                        "status": "paid",
                        "paid": True,
                        "subtotal_amount": 10000,
                        "created_at": "2025-01-15T12:00:00Z",
                        "modified_at": None,
                    },
                    {
                        "id": "ord_mock_002",
                        "status": "paid",
                        "paid": True,
                        "subtotal_amount": 20000,
                        "created_at": "2025-01-16T12:00:00Z",
                        "modified_at": None,
                    },
                ]
            )
        )

    @route("GET", "/v1/orders/{id}", writes=False)
    async def get_order(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "ord_mock_001",
                "status": "paid",
                "paid": True,
                "subtotal_amount": 10000,
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
            }
        )

    @route("GET", "/v1/subscriptions/", writes=False)
    async def list_subscriptions(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "sub_mock_001",
                        "amount": 10000,
                        "currency": "usd",
                        "recurring_interval": "month",
                        "status": "active",
                        "created_at": "2025-01-15T12:00:00Z",
                        "modified_at": None,
                    },
                    {
                        "id": "sub_mock_002",
                        "amount": 20000,
                        "currency": "usd",
                        "recurring_interval": "year",
                        "status": "active",
                        "created_at": "2025-01-16T12:00:00Z",
                        "modified_at": None,
                    },
                ]
            )
        )

    @route("GET", "/v1/subscriptions/{id}", writes=False)
    async def get_subscription(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "sub_mock_001",
                "amount": 10000,
                "currency": "usd",
                "recurring_interval": "month",
                "status": "active",
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
            }
        )

    @route("GET", "/v1/customers/", writes=False)
    async def list_customers(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "cus_mock_001",
                        "email": "alice@verifiabl.dev",
                        "external_id": None,
                        "created_at": "2025-01-15T12:00:00Z",
                        "modified_at": None,
                    },
                    {
                        "id": "cus_mock_002",
                        "email": "bob@verifiabl.dev",
                        "external_id": None,
                        "created_at": "2025-01-16T12:00:00Z",
                        "modified_at": None,
                    },
                ]
            )
        )

    @route("GET", "/v1/customers/{id}", writes=False)
    async def get_customer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "cus_mock_001",
                "email": "alice@verifiabl.dev",
                "external_id": None,
                "created_at": "2025-01-15T12:00:00Z",
                "modified_at": None,
            }
        )

    @route("POST", "/v1/checkouts/")
    async def create_checkout(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "checkout_mock_new",
                "url": "https://checkout.polar.sh/session/checkout_mock_new",
                "client_secret": "cs_mock_verifiabl",
                "created_at": "2025-01-15T12:00:00Z",
            },
        )
