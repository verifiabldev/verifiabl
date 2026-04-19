# CHANGELOG: https://github.com/calcom/cal.com/releases.atom
# SPEC:      https://cal.com/docs/api-reference/v2
# SANDBOX:   https://api.cal.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per Cal.com API v2 docs)
from mocks.base import BaseMock, route
from models import MockResponse


def _booking(uid="bkg_mock_001", title="Consultation"):
    return {
        "id": 101,
        "uid": uid,
        "title": title,
        "description": "",
        "hosts": [{"id": 1, "name": "Host", "email": "host@verifiabl.dev", "isFixed": True}],
        "status": "accepted",
        "start": "2024-08-13T15:30:00Z",
        "end": "2024-08-13T16:30:00Z",
        "duration": 60,
        "eventTypeId": 50,
        "eventType": {"id": 50, "title": "30 Min", "slug": "30min", "length": 30},
        "location": "https://meet.verifiabl.dev/abc",
        "absentHost": False,
        "createdAt": "2024-08-13T15:00:00Z",
        "updatedAt": "2024-08-13T15:00:00Z",
        "attendees": [
            {
                "email": "attendee@verifiabl.dev",
                "name": "Attendee",
                "timeZone": "America/Los_Angeles",
            }
        ],
        "bookingFieldsResponses": {},
    }


def _event_type(eid=50, title="30 Min", slug="30min"):
    return {"id": eid, "title": title, "slug": slug, "length": 30, "hidden": False}


class CalcomMock(BaseMock):
    # LOC EXCEPTION: Cal.com v2 envelope (status/data/pagination) and repeated booking/event_type shapes require helpers.
    prefix = "/calcom"
    spec_url = "https://cal.com/docs/api-reference/v2"
    sandbox_base = "https://api.cal.com"

    @route("GET", "/v2/me", writes=False)
    async def get_me(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "data": {
                    "id": 1,
                    "username": "mockuser",
                    "email": "mock@verifiabl.dev",
                    "name": "Mock User",
                    "avatarUrl": None,
                    "bio": None,
                    "timeFormat": 12,
                    "defaultScheduleId": 1,
                    "weekStart": "Sunday",
                    "timeZone": "America/Los_Angeles",
                    "organizationId": None,
                    "organization": None,
                },
            }
        )

    @route("GET", "/v2/bookings", writes=False)
    async def list_bookings(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "data": [
                    _booking("bkg_mock_001", "Consultation"),
                    _booking("bkg_mock_002", "Demo"),
                ],
                "pagination": {"total": 2, "take": 100, "skip": 0},
            }
        )

    @route("POST", "/v2/bookings")
    async def create_booking(self, request, **kw):
        return MockResponse(
            status=201, body={"status": "success", "data": _booking("bkg_mock_new", "New Booking")}
        )

    @route("GET", "/v2/bookings/{uid}", writes=False)
    async def get_booking(self, request, uid="", **kw):
        return MockResponse(
            body={"status": "success", "data": _booking(uid or "bkg_mock_001", "Consultation")}
        )

    @route("GET", "/v2/event-types", writes=False)
    async def list_event_types(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "data": [_event_type(50, "30 Min", "30min"), _event_type(51, "60 Min", "60min")],
                "pagination": {"total": 2, "take": 100, "skip": 0},
            }
        )

    @route("GET", "/v2/event-types/{id}", writes=False)
    async def get_event_type(self, request, id="", **kw):
        eid = int(id) if id and id.isdigit() else 50
        return MockResponse(body={"status": "success", "data": _event_type(eid, "30 Min", "30min")})

    @route("POST", "/v2/event-types")
    async def create_event_type(self, request, **kw):
        return MockResponse(
            status=201, body={"status": "success", "data": _event_type(52, "New Type", "new-type")}
        )

    @route("GET", "/v2/calendars", writes=False)
    async def list_calendars(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "data": [
                    {
                        "credentialId": 1,
                        "externalId": "primary",
                        "integration": "google_calendar",
                        "primary": True,
                    },
                    {
                        "credentialId": 2,
                        "externalId": "secondary",
                        "integration": "google_calendar",
                        "primary": False,
                    },
                ],
            }
        )

    @route("GET", "/v2/schedules", writes=False)
    async def list_schedules(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "Working Hours",
                        "timeZone": "America/Los_Angeles",
                        "isDefault": True,
                    },
                    {
                        "id": 2,
                        "name": "Weekends",
                        "timeZone": "America/Los_Angeles",
                        "isDefault": False,
                    },
                ],
            }
        )
