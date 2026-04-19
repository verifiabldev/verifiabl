# CHANGELOG: https://developer.zendesk.com/changelog/feed.xml
# SPEC:      https://developer.zendesk.com/api-reference/ticketing/introduction/
# SANDBOX:   https://www.zendesk.com/register/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_TICKET = {
    "id": 35436,
    "url": "https://example.zendesk.com/api/v2/tickets/35436",
    "subject": "Help, my printer is on fire!",
    "description": "The fire is very colorful.",
    "status": "open",
    "priority": "high",
    "type": "incident",
    "requester_id": 20978392,
    "submitter_id": 76872,
    "assignee_id": None,
    "group_id": None,
    "created_at": "2009-07-20T22:55:29Z",
    "updated_at": "2011-05-05T10:38:52Z",
    "via": {"channel": "web"},
    "tags": ["enterprise"],
}
_USER = {
    "id": 35436,
    "url": "https://example.zendesk.com/api/v2/users/35436",
    "name": "Johnny Agent",
    "email": "johnny@verifiabl.dev",
    "role": "agent",
    "created_at": "2009-07-20T22:55:29Z",
    "updated_at": "2011-05-05T10:38:52Z",
    "active": True,
    "verified": True,
}


class ZendeskMock(BaseMock):
    prefix = "/zendesk"
    spec_url = "https://developer.zendesk.com/api-reference"
    sandbox_base = "https://your-subdomain.zendesk.com"

    @route("GET", "/api/v2/users/me", writes=False)
    async def me(self, request, **kw):
        return MockResponse(
            body={
                "user": {
                    **_USER,
                    "id": 1,
                    "name": "Mock Agent",
                    "email": "mock@verifiabl.dev",
                    "role": "admin",
                }
            }
        )

    @route("GET", "/api/v2/tickets", writes=False)
    async def list_tickets(self, request, **kw):
        return MockResponse(
            body={
                "tickets": [
                    _TICKET,
                    {**_TICKET, "id": 35437, "subject": "Second ticket", "status": "pending"},
                ]
            }
        )

    @route("GET", "/api/v2/tickets/{ticket_id}", writes=False)
    async def show_ticket(self, request, ticket_id="", **kw):
        return MockResponse(
            body={"ticket": {**_TICKET, "id": int(ticket_id) if ticket_id.isdigit() else 35436}}
        )

    @route("POST", "/api/v2/tickets")
    async def create_ticket(self, request, **kw):
        return MockResponse(status=201, body={"ticket": {**_TICKET, "id": 42, "status": "new"}})

    @route("PUT", "/api/v2/tickets/{ticket_id}")
    async def update_ticket(self, request, ticket_id="", **kw):
        return MockResponse(
            body={
                "ticket": {
                    **_TICKET,
                    "id": int(ticket_id) if ticket_id.isdigit() else 35436,
                    "status": "open",
                }
            }
        )

    @route("GET", "/api/v2/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "users": [
                    _USER,
                    {**_USER, "id": 35437, "name": "Alice End User", "role": "end-user"},
                ]
            }
        )

    @route("GET", "/api/v2/users/{user_id}", writes=False)
    async def show_user(self, request, user_id="", **kw):
        return MockResponse(
            body={"user": {**_USER, "id": int(user_id) if user_id.isdigit() else 35436}}
        )

    @route("POST", "/api/v2/users")
    async def create_user(self, request, **kw):
        return MockResponse(status=201, body={"user": {**_USER, "id": 99}})

    @route("PUT", "/api/v2/users/{user_id}")
    async def update_user(self, request, user_id="", **kw):
        return MockResponse(
            body={"user": {**_USER, "id": int(user_id) if user_id.isdigit() else 35436}}
        )

    @route("GET", "/api/v2/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(
            body={
                "count": 2,
                "results": [
                    {**_TICKET, "result_type": "ticket"},
                    {**_USER, "result_type": "user"},
                ],
                "next_page": None,
                "previous_page": None,
            }
        )
