# CHANGELOG: https://docs.oracle.com/en/cloud/saas/human-resources/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.oracle.com/en/cloud/saas/human-resources/25b/farws/index.html
# SANDBOX:   https://www.oracle.com/cloud/free/ (instance-specific)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_HCM = "/hcmRestApi/resources/11.13.18.05"


class OracleHcmMock(BaseMock):
    prefix = "/oracle_hcm"
    spec_url = "https://docs.oracle.com/en/cloud/saas/human-resources/25b/farws/index.html"
    sandbox_base = "https://your-instance.fa.us2.oraclecloud.com"

    @route("GET", f"{_HCM}/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "OrganizationId": "org_mock_001",
                        "Name": "Engineering",
                        "OrganizationCode": "ENG",
                    },
                    {
                        "OrganizationId": "org_mock_002",
                        "Name": "Product",
                        "OrganizationCode": "PROD",
                    },
                ],
                "count": 2,
                "totalResults": 2,
            }
        )

    @route("GET", f"{_HCM}/organizations/{{organizationsUniqID}}", writes=False)
    async def get_organization(self, request, organizationsUniqID="", **kw):
        return MockResponse(
            body={
                "OrganizationId": organizationsUniqID or "org_mock_001",
                "Name": "Engineering",
                "OrganizationCode": "ENG",
                "Status": "Active",
            }
        )

    @route("GET", f"{_HCM}/locations", writes=False)
    async def list_locations(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {"LocationId": "loc_mock_001", "Name": "HQ", "LocationCode": "HQ"},
                    {"LocationId": "loc_mock_002", "Name": "Remote", "LocationCode": "REM"},
                ],
                "count": 2,
                "totalResults": 2,
            }
        )

    @route("GET", f"{_HCM}/locations/{{locationsUniqID}}", writes=False)
    async def get_location(self, request, locationsUniqID="", **kw):
        return MockResponse(
            body={
                "LocationId": locationsUniqID or "loc_mock_001",
                "Name": "HQ",
                "LocationCode": "HQ",
                "Status": "Active",
            }
        )

    @route("GET", f"{_HCM}/publicWorkers", writes=False)
    async def list_public_workers(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "PersonId": "person_mock_001",
                        "DisplayName": "Jane Doe",
                        "PersonNumber": "EMP001",
                    },
                    {
                        "PersonId": "person_mock_002",
                        "DisplayName": "John Smith",
                        "PersonNumber": "EMP002",
                    },
                ],
                "count": 2,
                "totalResults": 2,
            }
        )

    @route("GET", f"{_HCM}/publicWorkers/{{personId}}", writes=False)
    async def get_public_worker(self, request, personId="", **kw):
        return MockResponse(
            body={
                "PersonId": personId or "person_mock_001",
                "DisplayName": "Jane Doe",
                "PersonNumber": "EMP001",
                "PrimaryWorkEmail": "jane.doe@verifiabl.dev",
                "WorkerType": "Employee",
            }
        )

    @route("PATCH", f"{_HCM}/userAccounts/{{guid}}")
    async def update_user_account(self, request, guid="", **kw):
        return MockResponse(body={"UserAccountId": guid or "user_mock_001", "Status": "Active"})
