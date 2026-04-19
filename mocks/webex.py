# CHANGELOG: https://developer.webex.com/docs/api/changelog  (no RSS/atom feed found as of 2026-03)
# SPEC:      https://developer.webex.com/docs/rest-api-basics
# SANDBOX:   https://developer.webex.com/
# FAVICON:   https://webex.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class WebexMock(BaseMock):
    prefix = "/webex"
    spec_url = "https://developer.webex.com/docs/rest-api-basics"
    sandbox_base = "https://webexapis.com"

    @route("GET", "/v1/people", writes=False)
    async def list_people(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "person_mock_001",
                        "emails": ["alice@verifiabl.dev"],
                        "displayName": "Alice",
                        "created": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "person_mock_002",
                        "emails": ["bob@verifiabl.dev"],
                        "displayName": "Bob",
                        "created": "2024-03-14T12:00:00.000Z",
                    },
                ],
            }
        )

    @route("GET", "/v1/people/{personId}", writes=False)
    async def get_person(self, request, personId="", **kw):
        return MockResponse(
            body={
                "id": personId or "person_mock_001",
                "emails": ["mock@verifiabl.dev"],
                "displayName": "Mock User",
                "created": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("GET", "/v1/rooms", writes=False)
    async def list_rooms(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "room_mock_001",
                        "title": "General",
                        "type": "group",
                        "created": "2024-03-14T12:00:00.000Z",
                        "lastActivity": "2024-03-14T14:00:00.000Z",
                    },
                    {
                        "id": "room_mock_002",
                        "title": "Engineering",
                        "type": "group",
                        "created": "2024-03-14T12:00:00.000Z",
                        "lastActivity": "2024-03-14T13:00:00.000Z",
                    },
                ],
            }
        )

    @route("GET", "/v1/rooms/{roomId}", writes=False)
    async def get_room(self, request, roomId="", **kw):
        return MockResponse(
            body={
                "id": roomId or "room_mock_001",
                "title": "General",
                "type": "group",
                "created": "2024-03-14T12:00:00.000Z",
                "lastActivity": "2024-03-14T14:00:00.000Z",
            }
        )

    @route("POST", "/v1/rooms")
    async def create_room(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "room_mock_new",
                "title": "New Room",
                "type": "group",
                "created": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/v1/messages", writes=False)
    async def list_messages(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "msg_mock_001",
                        "roomId": "room_mock_001",
                        "personId": "person_mock_001",
                        "personEmail": "alice@verifiabl.dev",
                        "text": "Hello",
                        "created": "2024-03-14T13:00:00.000Z",
                    },
                    {
                        "id": "msg_mock_002",
                        "roomId": "room_mock_001",
                        "personId": "person_mock_002",
                        "personEmail": "bob@verifiabl.dev",
                        "text": "Hi there",
                        "created": "2024-03-14T13:01:00.000Z",
                    },
                ],
            }
        )

    @route("POST", "/v1/messages")
    async def create_message(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "msg_mock_new",
                "roomId": "room_mock_001",
                "personId": "person_mock_001",
                "personEmail": "mock@verifiabl.dev",
                "text": "Mock message",
                "created": "2024-03-14T14:00:00.000Z",
            },
        )

    @route("GET", "/v1/meetings/{meetingId}", writes=False)
    async def get_meeting(self, request, meetingId="", **kw):
        return MockResponse(
            body={
                "id": meetingId or "meeting_mock_001",
                "title": "Mock Meeting",
                "start": "2024-03-14T15:00:00.000Z",
                "end": "2024-03-14T16:00:00.000Z",
                "webLink": "https://meeting.webex.com/mock_meeting",
            }
        )

    @route("POST", "/v1/meetings")
    async def create_meeting(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "id": "meeting_mock_new",
                "title": "New Meeting",
                "start": "2024-03-14T17:00:00.000Z",
                "end": "2024-03-14T18:00:00.000Z",
                "webLink": "https://meeting.webex.com/mock_new",
            },
        )
