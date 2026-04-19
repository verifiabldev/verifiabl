# CHANGELOG: https://community.qualtrics.com/product-release-notes-96/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/microsoft/powerplatform-qualtrics-api (Swagger 2.0)
# SANDBOX:   https://fra1.qualtrics.com (datacenter-specific; use your brand's base URL)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _envelope(result_body, request_id="mock_verifiabl_001"):
    return {"result": result_body, "meta": {"httpStatus": "200 - OK", "requestId": request_id}}


class QualtricsMock(BaseMock):
    prefix = "/qualtrics"
    spec_url = "https://github.com/microsoft/powerplatform-qualtrics-api"
    sandbox_base = "https://fra1.qualtrics.com"

    @route("GET", "/API/v3/surveys", writes=False)
    async def list_surveys(self, request, **kw):
        return MockResponse(
            body=_envelope(
                {
                    "elements": [
                        {
                            "id": "SV_mock_001",
                            "name": "NPS Q1 2025",
                            "ownerId": "owner_mock",
                            "lastModified": "1710400000000",
                            "creationDate": "1710300000000",
                            "isActive": True,
                        },
                        {
                            "id": "SV_mock_002",
                            "name": "CSAT Survey",
                            "ownerId": "owner_mock",
                            "lastModified": "1710400000000",
                            "creationDate": "1710200000000",
                            "isActive": True,
                        },
                    ],
                    "nextPage": None,
                }
            )
        )

    @route("GET", "/API/v3/survey-definitions/{surveyId}", writes=False)
    async def get_survey(self, request, surveyId="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "id": surveyId or "SV_mock_001",
                    "name": "NPS Q1 2025",
                    "questions": {},
                    "blocks": {},
                }
            )
        )

    @route("GET", "/API/v3/distributions", writes=False)
    async def list_distributions(self, request, **kw):
        return MockResponse(
            body=_envelope(
                {
                    "elements": [
                        {
                            "id": "EM_mock_001",
                            "parentDistributionId": None,
                            "ownerId": "owner_mock",
                            "organizationId": "org_mock",
                            "requestStatus": "Done",
                            "requestType": "Invite",
                            "sendDate": "1710400000000",
                            "createdDate": "1710300000000",
                            "modifiedDate": "1710400000000",
                            "recipients": {"mailingListId": "ML_mock_001"},
                            "stats": {"sent": 50, "finished": 42},
                        },
                        {
                            "id": "EM_mock_002",
                            "parentDistributionId": None,
                            "ownerId": "owner_mock",
                            "organizationId": "org_mock",
                            "requestStatus": "Done",
                            "requestType": "Invite",
                            "sendDate": "1710350000000",
                            "createdDate": "1710250000000",
                            "modifiedDate": "1710350000000",
                            "recipients": {"mailingListId": "ML_mock_002"},
                            "stats": {"sent": 30, "finished": 28},
                        },
                    ],
                    "nextPage": None,
                }
            )
        )

    @route("POST", "/API/v3/distributions")
    async def create_distribution_links(self, request, **kw):
        return MockResponse(body=_envelope({"id": "EM_mock_new"}))

    @route("GET", "/API/v3/distributions/{distributionId}/links", writes=False)
    async def get_distribution_links(self, request, distributionId="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "elements": [
                        {
                            "contactId": "C_mock_001",
                            "link": "https://fra1.qualtrics.com/jfe/form/SV_mock_001?Q_DL=link_mock_001",
                            "firstName": "Alice",
                            "lastName": "Test",
                            "email": "alice@verifiabl.dev",
                            "status": "Created",
                            "linkExpiration": "2025-04-14T00:00:00Z",
                            "unsubscribed": False,
                        },
                        {
                            "contactId": "C_mock_002",
                            "link": "https://fra1.qualtrics.com/jfe/form/SV_mock_001?Q_DL=link_mock_002",
                            "firstName": "Bob",
                            "lastName": "Test",
                            "email": "bob@verifiabl.dev",
                            "status": "Created",
                            "linkExpiration": "2025-04-14T00:00:00Z",
                            "unsubscribed": False,
                        },
                    ],
                    "nextPage": None,
                }
            )
        )

    @route("POST", "/API/v3/directories/{directoryId}/mailinglists/{mailingListId}/contacts")
    async def create_contact(self, request, directoryId="", mailingListId="", **kw):
        return MockResponse(body=_envelope({"id": "C_mock_new"}))

    @route("GET", "/API/v3/eventsubscriptions/{subscriptionId}", writes=False)
    async def get_eventsubscription(self, request, subscriptionId="", **kw):
        return MockResponse(
            body=_envelope(
                {
                    "id": subscriptionId or "ES_mock_001",
                    "topic": "surveyengine.completedResponse.SV_mock_001",
                    "publicationUrl": "https://verifiabl.dev/webhook",
                }
            )
        )

    @route("POST", "/API/v3/eventsubscriptions")
    async def create_eventsubscription(self, request, **kw):
        return MockResponse(body=_envelope({"id": "ES_mock_new"}))
