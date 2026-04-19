# CHANGELOG: https://help.sap.com/docs/successfactors-platform (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.sap.com/docs/successfactors-platform/sap-successfactors-api-reference-guide-odata-v2
# SANDBOX:   https://api.sap.com/successfactors
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _d_list(results: list) -> dict:
    return {"d": {"results": results}}


def _d_entity(entity_id: str, entity_set: str, **props) -> dict:
    uri = f"https://host/odata/v2/{entity_set}('{entity_id}')"
    return {"d": {"__metadata": {"uri": uri, "type": f"SFOData.{entity_set}"}, **props}}


class SuccessfactorsMock(BaseMock):
    prefix = "/successfactors"
    spec_url = "https://help.sap.com/docs/successfactors-platform/sap-successfactors-api-reference-guide-odata-v2"
    sandbox_base = "https://api.successfactors.com"

    @route("GET", "/odata/v2/User", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body=_d_list(
                [
                    {
                        "userId": "user_mock_001",
                        "username": "alice",
                        "status": "ACTIVE",
                        "email": "alice@verifiabl.dev",
                    },
                    {
                        "userId": "user_mock_002",
                        "username": "bob",
                        "status": "ACTIVE",
                        "email": "bob@verifiabl.dev",
                    },
                ]
            )
        )

    @route("GET", "/odata/v2/User('{userId}')", writes=False)
    async def get_user(self, request, userId="", **kw):
        return MockResponse(
            body=_d_entity(
                userId,
                "User",
                userId=userId,
                username="mockuser",
                status="ACTIVE",
                email="mock@verifiabl.dev",
            )
        )

    @route("GET", "/odata/v2/JobRequisition", writes=False)
    async def list_job_requisitions(self, request, **kw):
        return MockResponse(
            body=_d_list(
                [
                    {
                        "jobReqId": "jr_mock_001",
                        "status": "OPEN",
                        "templateId": "5427",
                        "numberOfOpenings": 1,
                    },
                    {
                        "jobReqId": "jr_mock_002",
                        "status": "OPEN",
                        "templateId": "5427",
                        "numberOfOpenings": 2,
                    },
                ]
            )
        )

    @route("GET", "/odata/v2/JobRequisition('{id}')", writes=False)
    async def get_job_requisition(self, request, id="", **kw):
        return MockResponse(
            body=_d_entity(
                id,
                "JobRequisition",
                jobReqId=id,
                status="OPEN",
                templateId="5427",
                numberOfOpenings=1,
            )
        )

    @route("POST", "/odata/v2/JobRequisition")
    async def create_job_requisition(self, request, **kw):
        return MockResponse(
            status=201,
            body=_d_entity(
                "jr_mock_new",
                "JobRequisition",
                jobReqId="jr_mock_new",
                status="OPEN",
                templateId="5427",
                numberOfOpenings=1,
            ),
        )

    @route("GET", "/odata/v2/PerPerson", writes=False)
    async def list_per_person(self, request, **kw):
        return MockResponse(
            body=_d_list(
                [
                    {
                        "personIdExternal": "per_mock_001",
                        "firstName": "Alice",
                        "lastName": "Example",
                    },
                    {"personIdExternal": "per_mock_002", "firstName": "Bob", "lastName": "Sample"},
                ]
            )
        )

    @route("GET", "/odata/v2/Candidate", writes=False)
    async def list_candidates(self, request, **kw):
        return MockResponse(
            body=_d_list(
                [
                    {
                        "candidateId": "can_mock_001",
                        "firstName": "Jane",
                        "lastName": "Doe",
                        "status": "NEW",
                    },
                    {
                        "candidateId": "can_mock_002",
                        "firstName": "John",
                        "lastName": "Smith",
                        "status": "SCREENING",
                    },
                ]
            )
        )
