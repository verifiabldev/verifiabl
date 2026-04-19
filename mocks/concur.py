# CHANGELOG: https://developer.concur.com/tools-support/release-notes/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.concur.com/api-explorer
# SANDBOX:   https://us2.api.concursolutions.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class ConcurMock(BaseMock):
    prefix = "/concur"
    spec_url = "https://developer.concur.com/api-reference/expense/expense-report/v4.reports.html"
    sandbox_base = "https://us2.api.concursolutions.com"

    @route("GET", "/expensereports/v4/users/{userID}/context/{contextType}/reports", writes=False)
    async def list_reports(self, request, userID="", contextType="TRAVELER", **kw):
        return MockResponse(
            body={
                "content": [
                    {
                        "reportId": "rpt_mock_001",
                        "reportDate": "2024-03-01",
                        "approvalStatus": "Not Submitted",
                        "claimedAmount": {"value": 525.00, "currencyCode": "USD"},
                    },
                    {
                        "reportId": "rpt_mock_002",
                        "reportDate": "2024-03-15",
                        "approvalStatus": "Approved",
                        "claimedAmount": {"value": 120.50, "currencyCode": "USD"},
                    },
                ],
            }
        )

    @route("POST", "/expensereports/v4/users/{userID}/context/{contextType}/reports")
    async def create_report(self, request, userID="", contextType="TRAVELER", **kw):
        return MockResponse(
            status=201,
            body={
                "uri": f"https://us2.api.concursolutions.com/expensereports/v4/users/{userID}/context/{contextType}/reports/rpt_mock_new",
            },
        )

    @route(
        "GET",
        "/expensereports/v4/users/{userID}/context/{contextType}/reports/{reportId}",
        writes=False,
    )
    async def get_report(self, request, userID="", contextType="TRAVELER", reportId="", **kw):
        return MockResponse(
            body={
                "reportId": reportId or "rpt_mock_001",
                "reportDate": "2024-03-01",
                "approvalStatus": "Not Submitted",
                "approvalStatusId": "A_NOTF",
                "paymentStatus": "Not Paid",
                "paymentStatusId": "P_NOTP",
                "claimedAmount": {"value": 525.00, "currencyCode": "USD"},
                "approvedAmount": {"value": 525.00, "currencyCode": "USD"},
                "reportTotal": {"value": 525.00, "currencyCode": "USD"},
                "currencyCode": "USD",
                "name": "Mock expense report",
            }
        )

    @route("PATCH", "/expensereports/v4/users/{userID}/context/{contextType}/reports/{reportId}")
    async def update_report(self, request, userID="", contextType="TRAVELER", reportId="", **kw):
        return MockResponse(
            body={
                "reportId": reportId,
                "reportDate": "2024-03-01",
                "approvalStatus": "Not Submitted",
                "claimedAmount": {"value": 525.00, "currencyCode": "USD"},
                "currencyCode": "USD",
            }
        )

    @route("GET", "/expensereports/v4/reports/{reportId}/formFields", writes=False)
    async def get_report_form_fields(self, request, reportId="", **kw):
        return MockResponse(
            body={
                "items": [
                    {"id": "reportName", "label": "Report Name", "defaultValue": ""},
                    {"id": "businessPurpose", "label": "Business Purpose", "defaultValue": ""},
                ],
            }
        )

    @route(
        "GET",
        "/expensereports/v4/users/{userId}/context/{contextType}/reportsToApprove",
        writes=False,
    )
    async def reports_to_approve(self, request, userId="", contextType="MANAGER", **kw):
        return MockResponse(
            body={
                "content": [
                    {
                        "reportId": "rpt_mock_002",
                        "reportDate": "2024-03-15",
                        "approvalStatus": "Pending",
                        "claimedAmount": {"value": 120.50, "currencyCode": "USD"},
                    },
                ],
            }
        )
