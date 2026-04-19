# CHANGELOG: https://stripe.com/docs/changelog/feed.atom
# SPEC:      https://github.com/stripe/openapi
# SANDBOX:   https://dashboard.stripe.com/test/
# SKILL:     https://docs.stripe.com/building-with-llms
# MCP:       https://mcp.stripe.com
# LLMS:      https://stripe.com/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: 10 endpoints with Stripe list/object envelope; trimming would break agent payment-flow testing.
class StripeMock(BaseMock):
    prefix = "/stripe"
    spec_url = "https://github.com/stripe/openapi"
    sandbox_base = "https://api.stripe.com"

    @route("GET", "/v1/balance", writes=False)
    async def balance(self, request, **kw):
        return MockResponse(
            body={
                "object": "balance",
                "available": [{"amount": 1000000, "currency": "usd"}],
                "pending": [{"amount": 50000, "currency": "usd"}],
            }
        )

    @route("GET", "/v1/customers", writes=False)
    async def list_customers(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "cus_mock_001",
                        "object": "customer",
                        "email": "alice@verifiabl.dev",
                        "created": 1710400000,
                    },
                    {
                        "id": "cus_mock_002",
                        "object": "customer",
                        "email": "bob@verifiabl.dev",
                        "created": 1710400001,
                    },
                ],
                "has_more": False,
            }
        )

    @route("POST", "/v1/customers")
    async def create_customer(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "cus_mock_verifiabl",
                "object": "customer",
                "email": "test@verifiabl.dev",
                "created": 1710400000,
            },
        )

    @route("GET", "/v1/customers/{id}", writes=False)
    async def get_customer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "cus_mock_verifiabl",
                "object": "customer",
                "email": "test@verifiabl.dev",
                "created": 1710400000,
            }
        )

    @route("GET", "/v1/payment_intents", writes=False)
    async def list_payment_intents(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "pi_mock_001",
                        "object": "payment_intent",
                        "amount": 2000,
                        "currency": "usd",
                        "status": "succeeded",
                    },
                    {
                        "id": "pi_mock_002",
                        "object": "payment_intent",
                        "amount": 5000,
                        "currency": "usd",
                        "status": "requires_payment_method",
                    },
                ],
                "has_more": False,
            }
        )

    @route("POST", "/v1/payment_intents")
    async def create_payment_intent(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "pi_mock_verifiabl",
                "object": "payment_intent",
                "amount": 2000,
                "currency": "usd",
                "status": "requires_payment_method",
            },
        )

    @route("GET", "/v1/payment_intents/{id}", writes=False)
    async def get_payment_intent(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "pi_mock_verifiabl",
                "object": "payment_intent",
                "amount": 2000,
                "currency": "usd",
                "status": "requires_payment_method",
            }
        )

    @route("POST", "/v1/payment_intents/{id}/confirm")
    async def confirm_payment_intent(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "pi_mock_verifiabl",
                "object": "payment_intent",
                "amount": 2000,
                "currency": "usd",
                "status": "succeeded",
            }
        )

    @route("GET", "/v1/products", writes=False)
    async def list_products(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "prod_mock_001",
                        "object": "product",
                        "name": "Pro plan",
                        "created": 1710400000,
                    },
                    {
                        "id": "prod_mock_002",
                        "object": "product",
                        "name": "Enterprise",
                        "created": 1710400001,
                    },
                ],
                "has_more": False,
            }
        )

    @route("GET", "/v1/prices", writes=False)
    async def list_prices(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "data": [
                    {
                        "id": "price_mock_001",
                        "object": "price",
                        "unit_amount": 2000,
                        "currency": "usd",
                    },
                    {
                        "id": "price_mock_002",
                        "object": "price",
                        "unit_amount": 5000,
                        "currency": "usd",
                    },
                ],
                "has_more": False,
            }
        )
