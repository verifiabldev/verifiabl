# CHANGELOG: https://developer.microsoft.com/en-us/graph/changelog/rss
# SPEC:      https://learn.microsoft.com/en-us/graph/api/overview
# SANDBOX:   https://developer.microsoft.com/en-us/graph/graph-explorer
# SKILL:     —
# MCP:       https://learn.microsoft.com/en-us/graph/mcp-server/overview
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_ctx = "https://graph.microsoft.com/v1.0/$metadata#"


def _user(id_: str, display_name: str, mail: str):
    return {
        "id": id_,
        "displayName": display_name,
        "mail": mail,
        "userPrincipalName": mail,
        "givenName": display_name.split()[0] if display_name else "",
        "surname": display_name.split()[-1] if len(display_name.split()) > 1 else "",
    }


class MicrosoftMock(BaseMock):
    prefix = "/microsoft"
    spec_url = "https://learn.microsoft.com/en-us/graph/api/overview"
    sandbox_base = "https://graph.microsoft.com"

    @route("GET", "/v1.0/me", writes=False)
    async def me(self, request, **kw):
        return MockResponse(body=_user("user_mock_verifiabl", "Mock User", "mock@verifiabl.dev"))

    @route("GET", "/v1.0/users", writes=False)
    async def users_list(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "users",
                "value": [
                    _user("user_mock_001", "Alice Verifiabl", "alice@verifiabl.dev"),
                    _user("user_mock_002", "Bob Dev", "bob@verifiabl.dev"),
                ],
            }
        )

    @route("GET", "/v1.0/users/{id}", writes=False)
    async def user_get(self, request, id="", **kw):
        return MockResponse(
            body=_user(id or "user_mock_001", "Alice Verifiabl", "alice@verifiabl.dev")
        )

    @route("GET", "/v1.0/me/mailFolders", writes=False)
    async def mail_folders_list(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "users('user_mock_verifiabl')/mailFolders",
                "value": [
                    {"id": "inbox_mock", "displayName": "Inbox", "totalItemCount": 42},
                    {"id": "sent_mock", "displayName": "Sent Items", "totalItemCount": 10},
                ],
            }
        )

    @route("GET", "/v1.0/me/messages", writes=False)
    async def messages_list(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "users('user_mock_verifiabl')/messages",
                "value": [
                    {
                        "id": "msg_mock_001",
                        "subject": "Welcome",
                        "bodyPreview": "Hello from the mock.",
                        "receivedDateTime": "2024-03-14T12:00:00Z",
                    },
                    {
                        "id": "msg_mock_002",
                        "subject": "Re: Welcome",
                        "bodyPreview": "Thanks!",
                        "receivedDateTime": "2024-03-14T13:00:00Z",
                    },
                ],
            }
        )

    @route("GET", "/v1.0/me/calendar/events", writes=False)
    async def events_list(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "users('user_mock_verifiabl')/events",
                "value": [
                    {
                        "id": "event_mock_001",
                        "subject": "Team standup",
                        "start": {"dateTime": "2024-03-14T09:00:00", "timeZone": "UTC"},
                        "end": {"dateTime": "2024-03-14T09:30:00", "timeZone": "UTC"},
                    },
                ],
            }
        )

    @route("GET", "/v1.0/me/drive/root/children", writes=False)
    async def drive_children(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "users('user_mock_verifiabl')/drive/root/children",
                "value": [
                    {"id": "item_mock_001", "name": "Document.pdf", "size": 1024, "file": {}},
                    {"id": "item_mock_002", "name": "Folder", "folder": {"childCount": 3}},
                ],
            }
        )

    @route("POST", "/v1.0/me/sendMail")
    async def send_mail(self, request, **kw):
        return MockResponse(status=202, body={})

    @route("GET", "/v1.0/organization", writes=False)
    async def organization(self, request, **kw):
        return MockResponse(
            body={
                "@odata.context": _ctx + "organization",
                "value": [
                    {
                        "id": "org_mock_verifiabl",
                        "displayName": "Verifiabl Dev",
                        "verifiedDomains": [{"name": "verifiabl.dev", "isDefault": True}],
                    },
                ],
            }
        )
