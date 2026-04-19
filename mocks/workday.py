# CHANGELOG: https://userguide.doc.workday.com/adaptive-planning/.../api-changes-by-release (no RSS as of 2026-03)
# SPEC:      https://community.workday.com/sites/default/files/file-hosting/productionapi/
# SANDBOX:   https://wd1.workday.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class WorkdayMock(BaseMock):
    prefix = "/workday"
    spec_url = "https://community.workday.com/sites/default/files/file-hosting/productionapi/"
    sandbox_base = "https://wd1.workday.com"

    @route("GET", "/ccx/service/{tenant}/Human_Resources/v42.1/Workers", writes=False)
    async def list_workers(self, request, tenant="", **kw):
        return MockResponse(
            body={
                "Response_Results": {"Total_Results": 2, "Total_Pages": 1, "Page": 1},
                "Response_Data": {
                    "Worker": [
                        {
                            "Worker_Descriptor": "Jane Doe",
                            "Employee_ID": "emp_mock_001",
                            "Worker_Type": "Employee",
                        },
                        {
                            "Worker_Descriptor": "John Smith",
                            "Employee_ID": "emp_mock_002",
                            "Worker_Type": "Employee",
                        },
                    ],
                },
            }
        )

    @route("GET", "/ccx/service/{tenant}/Human_Resources/v42.1/Workers/{id}", writes=False)
    async def get_worker(self, request, tenant="", id="", **kw):
        return MockResponse(
            body={
                "Worker_Descriptor": "Jane Doe",
                "Employee_ID": id or "emp_mock_001",
                "Worker_Type": "Employee",
                "Legal_Name": {"Descriptor": "Jane Doe"},
                "Primary_Work_Email": "jane.doe@verifiabl.dev",
                "Worker_Status": "Active",
            }
        )

    @route("GET", "/ccx/service/{tenant}/Human_Resources/v42.1/Get_Employees", writes=False)
    async def get_employees(self, request, tenant="", **kw):
        return MockResponse(
            body={
                "Response_Results": {"Total_Results": 2, "Total_Pages": 1, "Page": 1},
                "Response_Data": {
                    "Employee": [
                        {"Descriptor": "Jane Doe", "ID": "emp_mock_001"},
                        {"Descriptor": "John Smith", "ID": "emp_mock_002"},
                    ],
                },
            }
        )

    @route("GET", "/ccx/service/{tenant}/Human_Resources/v42.1/Get_Job_Profiles", writes=False)
    async def get_job_profiles(self, request, tenant="", **kw):
        return MockResponse(
            body={
                "Response_Results": {"Total_Results": 2, "Total_Pages": 1, "Page": 1},
                "Response_Data": {
                    "Job_Profile": [
                        {"Descriptor": "Software Engineer", "ID": "job_mock_001"},
                        {"Descriptor": "Product Manager", "ID": "job_mock_002"},
                    ],
                },
            }
        )

    @route("GET", "/ccx/service/{tenant}/Recruiting/v42.0/Get_Job_Postings", writes=False)
    async def get_job_postings(self, request, tenant="", **kw):
        return MockResponse(
            body={
                "Response_Results": {"Total_Results": 2, "Total_Pages": 1, "Page": 1},
                "Response_Data": {
                    "Job_Posting": [
                        {
                            "Descriptor": "Software Engineer - Backend",
                            "ID": "post_mock_001",
                            "Status": "Posted",
                        },
                        {
                            "Descriptor": "Product Manager",
                            "ID": "post_mock_002",
                            "Status": "Posted",
                        },
                    ],
                },
            }
        )

    @route("GET", "/ccx/service/{tenant}/Human_Resources/v42.1/Find_Organization", writes=False)
    async def find_organization(self, request, tenant="", **kw):
        return MockResponse(
            body={
                "Response_Results": {"Total_Results": 2, "Total_Pages": 1, "Page": 1},
                "Response_Data": {
                    "Organization": [
                        {
                            "Descriptor": "Engineering",
                            "ID": "org_mock_001",
                            "Organization_Type": "Supervisory",
                        },
                        {
                            "Descriptor": "Product",
                            "ID": "org_mock_002",
                            "Organization_Type": "Supervisory",
                        },
                    ],
                },
            }
        )

    @route("PUT", "/ccx/service/{tenant}/Staffing/v42.0/Put_Worker")
    async def put_worker(self, request, tenant="", **kw):
        return MockResponse(
            status=200, body={"Worker_Reference": {"Descriptor": "Jane Doe", "ID": "emp_mock_001"}}
        )
