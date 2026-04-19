# CHANGELOG: https://www.linkedin.com/developers/news (no RSS/atom feed as of 2026-03)
# SPEC:      https://learn.microsoft.com/en-us/linkedin/sales/
# SANDBOX:   https://business.linkedin.com/sales-solutions/partners/become-a-partner
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class SalesnavigatorMock(BaseMock):
    prefix = "/salesnavigator"
    spec_url = "https://learn.microsoft.com/en-us/linkedin/sales/"
    sandbox_base = "https://api.linkedin.com"

    @route("GET", "/v2/salesContracts", writes=False)
    async def list_contracts(self, request, **kw):
        return MockResponse(
            body={
                "elements": [
                    {
                        "contract": "urn:li:contract:123456",
                        "name": "North America Sales Team",
                        "description": "Organic american apparel.",
                        "hasReportingAccess": True,
                    },
                    {
                        "contract": "urn:li:contract:1234560",
                        "name": "EMEA Sales-EnterpriseLicense",
                        "description": "Ut enim ad minim veniam.",
                        "hasReportingAccess": False,
                    },
                ],
                "paging": {"count": 10, "start": 0, "links": []},
            }
        )

    @route("POST", "/v2/salesAnalyticsExportJobs")
    async def create_export_job(self, request, **kw):
        return MockResponse(status=201, body={"value": {"id": 100004, "status": "ENQUEUED"}})

    @route("GET", "/v2/salesAnalyticsExportJobs/{jobId}", writes=False)
    async def get_export_job(self, request, jobId="", **kw):
        return MockResponse(
            body={
                "id": int(jobId) if jobId.isdigit() else 100004,
                "status": "COMPLETED",
                "downloadUrl": "https://www.linkedin.com/ambry/?x-li-ambry-ep=mock_verifiabl",
                "rowCount": 42,
                "expireAt": 1710400000000,
            }
        )

    @route("GET", "/v2/salesNavigatorProfileAssociations", writes=False)
    async def batch_profile_associations(self, request, **kw):
        return MockResponse(
            body={
                "statuses": {},
                "results": {
                    "(instanceId:foo,partner:bar,recordId:001)": {
                        "profilePhoto": "https://media.licdn.com/mock_001",
                        "profile": "https://www.linkedin.com/sales/lead/mock_001",
                        "member": "urn:li:person:mock_001",
                    },
                    "(instanceId:foo,partner:bar,recordId:002)": {
                        "profile": "https://www.linkedin.com/sales/lead/mock_002",
                        "member": "urn:li:person:mock_002",
                    },
                },
                "errors": {},
            }
        )

    @route("GET", "/v2/salesNavigatorProfileAssociations/{key}", writes=False)
    async def get_profile_association(self, request, key="", **kw):
        return MockResponse(
            body={
                "profilePhoto": "https://media.licdn.com/mock_verifiabl",
                "profile": "https://www.linkedin.com/sales/lead/mock_verifiabl",
                "member": "urn:li:person:mock_verifiabl",
            }
        )

    @route("POST", "/v2/crmDataValidationExportJobs")
    async def create_validation_export_job(self, request, **kw):
        return MockResponse(status=201, body=None, headers={"X-RestLi-Id": "148"})

    @route("GET", "/v2/crmDataValidationExportJobs/{jobId}", writes=False)
    async def get_validation_export_job(self, request, jobId="", **kw):
        return MockResponse(
            body={
                "jobId": int(jobId) if jobId.isdigit() else 148,
                "exportStartAt": 1538947151337,
                "exportEndAt": 1541539151570,
                "downloadUrls": ["https://www.linkedin.com/ambry/?x-li-ambry-ep=mock_verifiabl"],
                "nextExportStartAt": 1538947151337,
                "expireAt": 1541635625000,
                "status": "COMPLETED",
            }
        )
