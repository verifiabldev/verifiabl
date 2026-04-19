# CHANGELOG: https://docs.lemonsqueezy.com/api/getting-started/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.lemonsqueezy.com/api
# SANDBOX:   https://app.lemonsqueezy.com (Test mode)
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per API docs)
from mocks.base import BaseMock, route
from models import MockResponse


def _list(typename: str, items: list) -> dict:
    data = [{"type": typename, "id": str(x["id"]), "attributes": x["attributes"]} for x in items]
    return {
        "meta": {
            "page": {
                "currentPage": 1,
                "from": 1,
                "lastPage": 1,
                "perPage": 10,
                "to": len(data),
                "total": len(data),
            }
        },
        "jsonapi": {"version": "1.0"},
        "data": data,
    }


def _one(typename: str, id: str, attributes: dict) -> dict:
    return {
        "jsonapi": {"version": "1.0"},
        "data": {"type": typename, "id": str(id), "attributes": attributes},
    }


TS = "2024-05-24T14:15:06.000000Z"


# LOC EXCEPTION: JSON:API envelope plus 13 schema-faithful endpoints; fewer would break agent checkout/subscription flows.
class LemonSqueezyMock(BaseMock):
    prefix = "/lemonsqueezy"
    spec_url = "https://docs.lemonsqueezy.com/api"
    sandbox_base = "https://api.lemonsqueezy.com"

    @route("GET", "/v1/users/me", writes=False)
    async def get_user(self, request, **kw):
        return MockResponse(
            body=_one(
                "users",
                "1",
                {
                    "name": "Mock User",
                    "email": "test@verifiabl.dev",
                    "createdAt": TS,
                    "updatedAt": TS,
                },
            )
        )

    @route("GET", "/v1/stores", writes=False)
    async def list_stores(self, request, **kw):
        return MockResponse(
            body=_list(
                "stores",
                [
                    {
                        "id": "1",
                        "attributes": {
                            "name": "Mock Store",
                            "slug": "mock-store",
                            "domain": "mock-store.lemonsqueezy.com",
                            "url": "https://mock-store.lemonsqueezy.com",
                            "plan": "fresh",
                            "country": "US",
                            "currency": "USD",
                            "total_sales": 0,
                            "total_revenue": 0,
                            "created_at": TS,
                            "updated_at": TS,
                        },
                    },
                    {
                        "id": "2",
                        "attributes": {
                            "name": "Second Store",
                            "slug": "second-store",
                            "domain": "second-store.lemonsqueezy.com",
                            "url": "https://second-store.lemonsqueezy.com",
                            "plan": "sweet",
                            "country": "US",
                            "currency": "USD",
                            "total_sales": 1,
                            "total_revenue": 999,
                            "created_at": TS,
                            "updated_at": TS,
                        },
                    },
                ],
            )
        )

    @route("GET", "/v1/stores/{id}", writes=False)
    async def get_store(self, request, id="", **kw):
        return MockResponse(
            body=_one(
                "stores",
                id or "1",
                {
                    "name": "Mock Store",
                    "slug": "mock-store",
                    "domain": "mock-store.lemonsqueezy.com",
                    "url": "https://mock-store.lemonsqueezy.com",
                    "plan": "fresh",
                    "country": "US",
                    "currency": "USD",
                    "total_sales": 0,
                    "total_revenue": 0,
                    "created_at": TS,
                    "updated_at": TS,
                },
            )
        )

    @route("GET", "/v1/products", writes=False)
    async def list_products(self, request, **kw):
        return MockResponse(
            body=_list(
                "products",
                [
                    {
                        "id": "1",
                        "attributes": {
                            "store_id": 1,
                            "name": "Pro Plan",
                            "slug": "pro-plan",
                            "status": "published",
                            "price": 1999,
                            "price_formatted": "$19.99",
                            "buy_now_url": "https://mock-store.lemonsqueezy.com/checkout/buy/abc",
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                    {
                        "id": "2",
                        "attributes": {
                            "store_id": 1,
                            "name": "Enterprise",
                            "slug": "enterprise",
                            "status": "published",
                            "price": 9999,
                            "price_formatted": "$99.99",
                            "buy_now_url": "https://mock-store.lemonsqueezy.com/checkout/buy/def",
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                ],
            )
        )

    @route("GET", "/v1/products/{id}", writes=False)
    async def get_product(self, request, id="", **kw):
        return MockResponse(
            body=_one(
                "products",
                id or "1",
                {
                    "store_id": 1,
                    "name": "Pro Plan",
                    "slug": "pro-plan",
                    "status": "published",
                    "price": 1999,
                    "price_formatted": "$19.99",
                    "buy_now_url": "https://mock-store.lemonsqueezy.com/checkout/buy/abc",
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": False,
                },
            )
        )

    @route("GET", "/v1/orders", writes=False)
    async def list_orders(self, request, **kw):
        return MockResponse(
            body=_list(
                "orders",
                [
                    {
                        "id": "1",
                        "attributes": {
                            "store_id": 1,
                            "customer_id": 1,
                            "identifier": "104e18a2-d755-4d4b-80c4-a6c1dcbe1c10",
                            "order_number": 1,
                            "user_name": "Alice",
                            "user_email": "alice@verifiabl.dev",
                            "currency": "USD",
                            "subtotal": 1999,
                            "total": 1999,
                            "status": "paid",
                            "status_formatted": "Paid",
                            "refunded": False,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                    {
                        "id": "2",
                        "attributes": {
                            "store_id": 1,
                            "customer_id": 2,
                            "identifier": "204e18a2-d755-4d4b-80c4-a6c1dcbe1c11",
                            "order_number": 2,
                            "user_name": "Bob",
                            "user_email": "bob@verifiabl.dev",
                            "currency": "USD",
                            "subtotal": 9999,
                            "total": 9999,
                            "status": "paid",
                            "status_formatted": "Paid",
                            "refunded": False,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                ],
            )
        )

    @route("GET", "/v1/orders/{id}", writes=False)
    async def get_order(self, request, id="", **kw):
        return MockResponse(
            body=_one(
                "orders",
                id or "1",
                {
                    "store_id": 1,
                    "customer_id": 1,
                    "identifier": "104e18a2-d755-4d4b-80c4-a6c1dcbe1c10",
                    "order_number": 1,
                    "user_name": "Alice",
                    "user_email": "alice@verifiabl.dev",
                    "currency": "USD",
                    "subtotal": 1999,
                    "total": 1999,
                    "status": "paid",
                    "status_formatted": "Paid",
                    "refunded": False,
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": False,
                },
            )
        )

    @route("GET", "/v1/customers", writes=False)
    async def list_customers(self, request, **kw):
        return MockResponse(
            body=_list(
                "customers",
                [
                    {
                        "id": "1",
                        "attributes": {
                            "store_id": 1,
                            "name": "Alice",
                            "email": "alice@verifiabl.dev",
                            "status": "subscribed",
                            "country": "US",
                            "total_revenue_currency": 1999,
                            "mrr": 1999,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                    {
                        "id": "2",
                        "attributes": {
                            "store_id": 1,
                            "name": "Bob",
                            "email": "bob@verifiabl.dev",
                            "status": "subscribed",
                            "country": "US",
                            "total_revenue_currency": 9999,
                            "mrr": 0,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                ],
            )
        )

    @route("GET", "/v1/customers/{id}", writes=False)
    async def get_customer(self, request, id="", **kw):
        return MockResponse(
            body=_one(
                "customers",
                id or "1",
                {
                    "store_id": 1,
                    "name": "Alice",
                    "email": "alice@verifiabl.dev",
                    "status": "subscribed",
                    "country": "US",
                    "total_revenue_currency": 1999,
                    "mrr": 1999,
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": False,
                },
            )
        )

    @route("POST", "/v1/customers")
    async def create_customer(self, request, **kw):
        return MockResponse(
            status=201,
            body=_one(
                "customers",
                "1",
                {
                    "store_id": 1,
                    "name": "New Customer",
                    "email": "new@verifiabl.dev",
                    "status": "subscribed",
                    "country": "US",
                    "total_revenue_currency": 0,
                    "mrr": 0,
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": True,
                },
            ),
        )

    @route("GET", "/v1/subscriptions", writes=False)
    async def list_subscriptions(self, request, **kw):
        return MockResponse(
            body=_list(
                "subscriptions",
                [
                    {
                        "id": "1",
                        "attributes": {
                            "store_id": 1,
                            "customer_id": 1,
                            "order_id": 1,
                            "product_id": 1,
                            "variant_id": 1,
                            "product_name": "Pro Plan",
                            "variant_name": "Monthly",
                            "user_name": "Alice",
                            "user_email": "alice@verifiabl.dev",
                            "status": "active",
                            "status_formatted": "Active",
                            "renews_at": "2025-06-24T00:00:00.000000Z",
                            "ends_at": None,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                    {
                        "id": "2",
                        "attributes": {
                            "store_id": 1,
                            "customer_id": 2,
                            "order_id": 2,
                            "product_id": 1,
                            "variant_id": 2,
                            "product_name": "Pro Plan",
                            "variant_name": "Yearly",
                            "user_name": "Bob",
                            "user_email": "bob@verifiabl.dev",
                            "status": "active",
                            "status_formatted": "Active",
                            "renews_at": "2026-05-24T00:00:00.000000Z",
                            "ends_at": None,
                            "created_at": TS,
                            "updated_at": TS,
                            "test_mode": False,
                        },
                    },
                ],
            )
        )

    @route("GET", "/v1/subscriptions/{id}", writes=False)
    async def get_subscription(self, request, id="", **kw):
        return MockResponse(
            body=_one(
                "subscriptions",
                id or "1",
                {
                    "store_id": 1,
                    "customer_id": 1,
                    "order_id": 1,
                    "product_id": 1,
                    "variant_id": 1,
                    "product_name": "Pro Plan",
                    "variant_name": "Monthly",
                    "user_name": "Alice",
                    "user_email": "alice@verifiabl.dev",
                    "status": "active",
                    "status_formatted": "Active",
                    "renews_at": "2025-06-24T00:00:00.000000Z",
                    "ends_at": None,
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": False,
                },
            )
        )

    @route("POST", "/v1/checkouts")
    async def create_checkout(self, request, **kw):
        return MockResponse(
            status=201,
            body=_one(
                "checkouts",
                "5e8b546c-c561-4a2c-a586-40c18bb2a195",
                {
                    "store_id": 1,
                    "variant_id": 1,
                    "url": "https://mock-store.lemonsqueezy.com/checkout/custom/5e8b546c-c561-4a2c-a586-40c18bb2a195",
                    "created_at": TS,
                    "updated_at": TS,
                    "test_mode": True,
                },
            ),
        )
