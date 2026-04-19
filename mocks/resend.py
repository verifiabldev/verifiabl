# CHANGELOG: https://resend.com/changelog  (no RSS/atom feed found as of 2026-03)
# SPEC:      https://github.com/resend/resend-openapi
# SANDBOX:   https://resend.com/emails
# SKILL:     —
# MCP:       —
# LLMS:      https://resend.com/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class ResendMock(BaseMock):
    prefix = "/resend"
    spec_url = "https://github.com/resend/resend-openapi"
    sandbox_base = "https://api.resend.com"

    @route("GET", "/emails", writes=False)
    async def list_emails(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "object": "email",
                        "id": "email_mock_001",
                        "to": ["delivered@verifiabl.dev"],
                        "from": "onboarding@verifiabl.dev",
                        "subject": "Hello World",
                        "created_at": "2023-04-03T22:13:42.674981+00:00",
                        "last_event": "delivered",
                    },
                    {
                        "object": "email",
                        "id": "email_mock_002",
                        "to": ["recipient@verifiabl.dev"],
                        "from": "onboarding@verifiabl.dev",
                        "subject": "Welcome",
                        "created_at": "2023-04-03T22:14:00.000000+00:00",
                        "last_event": "delivered",
                    },
                ],
            }
        )

    @route("POST", "/emails")
    async def send_email(self, request, **kw):
        return MockResponse(status=200, body={"id": "email_mock_verifiabl"})

    @route("GET", "/emails/{email_id}", writes=False)
    async def get_email(self, request, email_id="", **kw):
        return MockResponse(
            body={
                "object": "email",
                "id": email_id or "email_mock_001",
                "to": ["delivered@verifiabl.dev"],
                "from": "onboarding@verifiabl.dev",
                "subject": "Hello World",
                "created_at": "2023-04-03T22:13:42.674981+00:00",
                "last_event": "delivered",
            }
        )

    @route("POST", "/emails/batch")
    async def send_batch(self, request, **kw):
        return MockResponse(
            status=200, body={"data": [{"id": "email_mock_b1"}, {"id": "email_mock_b2"}]}
        )

    @route("GET", "/domains", writes=False)
    async def list_domains(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "domain_mock_001",
                        "name": "verifiabl.dev",
                        "status": "verified",
                        "created_at": "2023-04-26T20:21:26.347412+00:00",
                        "region": "us-east-1",
                    },
                    {
                        "id": "domain_mock_002",
                        "name": "app.verifiabl.dev",
                        "status": "pending",
                        "created_at": "2023-04-26T20:22:00.000000+00:00",
                        "region": "us-east-1",
                    },
                ],
            }
        )

    @route("POST", "/domains")
    async def create_domain(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "domain_mock_new",
                "name": "new.verifiabl.dev",
                "status": "pending",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
                "records": [],
            },
        )

    @route("GET", "/domains/{domain_id}", writes=False)
    async def get_domain(self, request, domain_id="", **kw):
        return MockResponse(
            body={
                "object": "domain",
                "id": domain_id or "domain_mock_001",
                "name": "verifiabl.dev",
                "status": "verified",
                "created_at": "2023-04-26T20:21:26.347412+00:00",
                "region": "us-east-1",
            }
        )

    @route("GET", "/api-keys", writes=False)
    async def list_api_keys(self, request, **kw):
        return MockResponse(
            body={
                "object": "list",
                "has_more": False,
                "data": [
                    {
                        "id": "key_mock_001",
                        "name": "Production",
                        "created_at": "2023-04-26T20:21:26.347412+00:00",
                    },
                    {
                        "id": "key_mock_002",
                        "name": "Development",
                        "created_at": "2023-04-26T20:22:00.000000+00:00",
                    },
                ],
            }
        )
