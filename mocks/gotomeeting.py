# CHANGELOG: https://developer.goto.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.goto.com/GoToMeetingV1/
# SANDBOX:   https://developer.goto.com
# FAVICON:   https://goto.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class GoToMeetingMock(BaseMock):
    prefix = "/gotomeeting"
    spec_url = "https://developer.goto.com/GoToMeetingV1/"
    sandbox_base = "https://api.getgo.com/G2M/rest"

    @route("GET", "/G2M/rest/organizers", writes=False)
    async def list_organizers(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "lastName": "Verifiabl",
                    "groupId": 1,
                    "groupName": "Default",
                    "status": "active",
                    "organizerKey": 9001,
                    "organizerkey": 9001,
                    "email": "organizer@verifiabl.dev",
                    "firstName": "Mock",
                    "products": ["G2M"],
                    "maxNumAttendeesAllowed": 25,
                },
            ]
        )

    @route("GET", "/G2M/rest/organizers/{organizerKey}", writes=False)
    async def get_organizer(self, request, organizerKey="", **kw):
        return MockResponse(
            body={
                "lastName": "Verifiabl",
                "groupId": 1,
                "groupName": "Default",
                "status": "active",
                "organizerKey": int(organizerKey) if organizerKey.isdigit() else 9001,
                "email": "organizer@verifiabl.dev",
                "firstName": "Mock",
                "products": ["G2M"],
                "maxNumAttendeesAllowed": 25,
            }
        )

    @route("GET", "/G2M/rest/organizers/{organizerKey}/upcomingMeetings", writes=False)
    async def upcoming_meetings_by_organizer(self, request, organizerKey="", **kw):
        return MockResponse(
            body=[
                {
                    "startTime": "2025-04-01T18:00:00.+0000",
                    "endTime": "2025-04-01T19:00:00.+0000",
                    "subject": "Mock sync",
                    "meetingId": 123456789,
                    "meetingType": "scheduled",
                    "joinURL": "https://meet.goto.com/mock_verifiabl",
                    "conferenceCallInfo": "Hybrid",
                    "status": "ACTIVE",
                }
            ]
        )

    @route("GET", "/G2M/rest/meetings", writes=False)
    async def list_meetings(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "startTime": "2025-04-01T18:00:00.+0000",
                    "endTime": "2025-04-01T19:00:00.+0000",
                    "createTime": "",
                    "meetingid": 123456789,
                    "maxParticipants": 25,
                    "passwordRequired": "false",
                    "status": "ACTIVE",
                    "subject": "Mock sync",
                    "meetingType": "scheduled",
                    "uniqueMeetingId": 123456789,
                    "conferenceCallInfo": "Hybrid",
                }
            ]
        )

    @route("POST", "/G2M/rest/meetings")
    async def create_meeting(self, request, **kw):
        return MockResponse(
            status=201,
            body=[
                {
                    "joinURL": "https://meet.goto.com/mock_new",
                    "meetingid": 987654321,
                    "maxParticipants": 25,
                    "uniqueMeetingId": 987654321,
                    "conferenceCallInfo": "Hybrid",
                }
            ],
        )

    @route("GET", "/G2M/rest/meetings/{meetingId}", writes=False)
    async def get_meeting(self, request, meetingId="", **kw):
        mid = int(meetingId) if meetingId.isdigit() else 123456789
        return MockResponse(
            body={
                "createTime": "",
                "passwordRequired": "false",
                "status": "ACTIVE",
                "subject": "Mock sync",
                "conferenceCallInfo": "Hybrid",
                "maxParticipants": 25,
                "meetingId": mid,
                "meetingKey": mid,
                "meetingType": "scheduled",
                "uniqueMeetingId": mid,
                "coorganizerKeys": [],
                "joinURL": "https://meet.goto.com/mock_verifiabl",
                "startTime": "2025-04-01T18:00:00.+0000",
                "endTime": "2025-04-01T19:00:00.+0000",
                "duration": 60,
            }
        )

    @route("PUT", "/G2M/rest/meetings/{meetingId}")
    async def update_meeting(self, request, meetingId="", **kw):
        return MockResponse(
            body={
                "meetingId": int(meetingId) if meetingId.isdigit() else 123456789,
                "joinURL": "https://meet.goto.com/mock_verifiabl",
                "subject": "Updated sync",
            }
        )

    @route("DELETE", "/G2M/rest/meetings/{meetingId}")
    async def delete_meeting(self, request, meetingId="", **kw):
        return MockResponse(status=204, body=None)

    @route("GET", "/G2M/rest/meetings/{meetingId}/start", writes=False)
    async def start_meeting(self, request, meetingId="", **kw):
        return MockResponse(body={"hostURL": "https://meet.goto.com/start/mock_verifiabl"})

    @route("GET", "/G2M/rest/meetings/{meetingId}/attendees", writes=False)
    async def get_attendees_by_meeting(self, request, meetingId="", **kw):
        return MockResponse(
            body=[
                {
                    "name": "Alice",
                    "email": "alice@verifiabl.dev",
                    "joinTime": "2025-04-01T18:05:00.+0000",
                    "leaveTime": "2025-04-01T18:55:00.+0000",
                }
            ]
        )

    @route("GET", "/G2M/rest/groups", writes=False)
    async def list_groups(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "groupkey": 1,
                    "groupName": "Default",
                    "parentKey": 1,
                    "status": "active",
                    "numOrganizers": 2,
                }
            ]
        )

    @route("GET", "/G2M/rest/groups/{groupKey}/organizers", writes=False)
    async def get_organizers_by_group(self, request, groupKey="", **kw):
        return MockResponse(
            body=[
                {
                    "lastName": "Verifiabl",
                    "groupId": 1,
                    "groupName": "Default",
                    "status": "active",
                    "organizerKey": 9001,
                    "email": "organizer@verifiabl.dev",
                    "firstName": "Mock",
                    "products": ["G2M"],
                    "maxNumAttendeesAllowed": 25,
                }
            ]
        )
