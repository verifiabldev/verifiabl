# CHANGELOG: https://developer.paddle.com/changelog/overview (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/PaddleHQ/paddle-openapi
# SANDBOX:   https://vendors.paddle.com (Developer tools → Authentication)
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (API key; per developer.paddle.com)
from mocks.base import BaseMock, route
from models import MockResponse

_TS = "2024-03-14T12:00:00Z"
_META = {"request_id": "req_mock_verifiabl", "pagination": {"per_page": 50, "next": None}}


# LOC EXCEPTION: 11 endpoints with Paddle data+meta envelope; fewer would break subscription/transaction workflow testing.
class PaddleMock(BaseMock):
    prefix = "/paddle"
    spec_url = "https://github.com/PaddleHQ/paddle-openapi"
    sandbox_base = "https://sandbox-api.paddle.com"

    @route("GET", "/customers", writes=False)
    async def list_customers(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "ctm_mock_001",
                        "email": "alice@verifiabl.dev",
                        "name": "Alice",
                        "status": "active",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                    {
                        "id": "ctm_mock_002",
                        "email": "bob@verifiabl.dev",
                        "name": "Bob",
                        "status": "active",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                ],
                "meta": _META,
            }
        )

    @route("POST", "/customers")
    async def create_customer(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "data": {
                    "id": "ctm_mock_verifiabl",
                    "email": "test@verifiabl.dev",
                    "name": None,
                    "status": "active",
                    "created_at": _TS,
                    "updated_at": _TS,
                },
                "meta": _META,
            },
        )

    @route("GET", "/customers/{id}", writes=False)
    async def get_customer(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "ctm_mock_verifiabl",
                    "email": "test@verifiabl.dev",
                    "name": None,
                    "status": "active",
                    "created_at": _TS,
                    "updated_at": _TS,
                },
                "meta": _META,
            }
        )

    @route("GET", "/products", writes=False)
    async def list_products(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "pro_mock_001",
                        "name": "Pro plan",
                        "description": None,
                        "status": "active",
                        "tax_category": "standard",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                    {
                        "id": "pro_mock_002",
                        "name": "Enterprise",
                        "description": None,
                        "status": "active",
                        "tax_category": "standard",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                ],
                "meta": _META,
            }
        )

    @route("GET", "/products/{id}", writes=False)
    async def get_product(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "pro_mock_001",
                    "name": "Pro plan",
                    "description": None,
                    "status": "active",
                    "tax_category": "standard",
                    "created_at": _TS,
                    "updated_at": _TS,
                },
                "meta": _META,
            }
        )

    @route("GET", "/prices", writes=False)
    async def list_prices(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "pri_mock_001",
                        "product_id": "pro_mock_001",
                        "description": "Monthly",
                        "unit_price": {"amount": "2000", "currency_code": "USD"},
                        "status": "active",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                    {
                        "id": "pri_mock_002",
                        "product_id": "pro_mock_002",
                        "description": "Annual",
                        "unit_price": {"amount": "20000", "currency_code": "USD"},
                        "status": "active",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                ],
                "meta": _META,
            }
        )

    @route("GET", "/subscriptions", writes=False)
    async def list_subscriptions(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "sub_mock_001",
                        "customer_id": "ctm_mock_001",
                        "status": "active",
                        "currency_code": "USD",
                        "created_at": _TS,
                        "updated_at": _TS,
                        "next_billed_at": _TS,
                    },
                    {
                        "id": "sub_mock_002",
                        "customer_id": "ctm_mock_002",
                        "status": "active",
                        "currency_code": "USD",
                        "created_at": _TS,
                        "updated_at": _TS,
                        "next_billed_at": _TS,
                    },
                ],
                "meta": _META,
            }
        )

    @route("GET", "/subscriptions/{id}", writes=False)
    async def get_subscription(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "sub_mock_001",
                    "customer_id": "ctm_mock_001",
                    "status": "active",
                    "currency_code": "USD",
                    "created_at": _TS,
                    "updated_at": _TS,
                    "next_billed_at": _TS,
                },
                "meta": _META,
            }
        )

    @route("GET", "/transactions", writes=False)
    async def list_transactions(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "txn_mock_001",
                        "customer_id": "ctm_mock_001",
                        "status": "completed",
                        "currency_code": "USD",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                    {
                        "id": "txn_mock_002",
                        "customer_id": "ctm_mock_002",
                        "status": "billed",
                        "currency_code": "USD",
                        "created_at": _TS,
                        "updated_at": _TS,
                    },
                ],
                "meta": _META,
            }
        )

    @route("GET", "/transactions/{id}", writes=False)
    async def get_transaction(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "txn_mock_001",
                    "customer_id": "ctm_mock_001",
                    "status": "completed",
                    "currency_code": "USD",
                    "created_at": _TS,
                    "updated_at": _TS,
                },
                "meta": _META,
            }
        )

    @route("POST", "/transactions")
    async def create_transaction(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "data": {
                    "id": "txn_mock_verifiabl",
                    "customer_id": "ctm_mock_verifiabl",
                    "status": "ready",
                    "currency_code": "USD",
                    "created_at": _TS,
                    "updated_at": _TS,
                },
                "meta": _META,
            },
        )
