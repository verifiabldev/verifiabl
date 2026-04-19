# CHANGELOG: https://developer.ukg.com/hcm/docs/news-doc  (no RSS/atom feed found as of 2026-03)
# SPEC:      https://developer.ukg.com/hcm/reference/welcome-to-the-ukg-pro-api
# SANDBOX:   https://developer.ukg.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class UkgproMock(BaseMock):
    prefix = "/ukgpro"
    spec_url = "https://developer.ukg.com/hcm/reference/welcome-to-the-ukg-pro-api"
    sandbox_base = "https://service.ukg.com"

    @route("GET", "/personnel/v1/person-details", writes=False)
    async def person_details_list(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "EmployeeIdentifier": "emp_mock_001",
                    "FirstName": "Jane",
                    "LastName": "Doe",
                    "EmailAddress": "jane@verifiabl.dev",
                },
                {
                    "EmployeeIdentifier": "emp_mock_002",
                    "FirstName": "John",
                    "LastName": "Smith",
                    "EmailAddress": "john@verifiabl.dev",
                },
            ]
        )

    @route("GET", "/personnel/v1/person-details/{employeeId}", writes=False)
    async def person_details_get(self, request, employeeId="", **kw):
        return MockResponse(
            body={
                "EmployeeIdentifier": employeeId or "emp_mock_001",
                "FirstName": "Jane",
                "LastName": "Doe",
                "EmailAddress": "jane@verifiabl.dev",
                "MiddleName": "",
            }
        )

    @route("GET", "/personnel/v1/employee-demographic-details", writes=False)
    async def employee_demographic_details(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "EmployeeIdentifier": "emp_mock_001",
                    "DateOfBirth": "1990-01-15",
                    "GenderCode": "F",
                },
                {
                    "EmployeeIdentifier": "emp_mock_002",
                    "DateOfBirth": "1985-06-20",
                    "GenderCode": "M",
                },
            ]
        )

    @route("GET", "/personnel/v1/employment-details", writes=False)
    async def employment_details(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "EmployeeIdentifier": "emp_mock_001",
                    "CompanyCode": "CC001",
                    "JobCode": "ENG",
                    "HireDate": "2020-03-01",
                },
                {
                    "EmployeeIdentifier": "emp_mock_002",
                    "CompanyCode": "CC001",
                    "JobCode": "MGR",
                    "HireDate": "2019-01-15",
                },
            ]
        )

    @route("GET", "/personnel/v1/contacts", writes=False)
    async def contacts_list(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "ContactId": "con_mock_001",
                    "EmployeeIdentifier": "emp_mock_001",
                    "ContactType": "Work",
                    "PhoneNumber": "+15551234567",
                },
                {
                    "ContactId": "con_mock_002",
                    "EmployeeIdentifier": "emp_mock_002",
                    "ContactType": "Work",
                    "PhoneNumber": "+15559876543",
                },
            ]
        )

    @route("GET", "/personnel/v1/compensation-details", writes=False)
    async def compensation_details(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "EmployeeIdentifier": "emp_mock_001",
                    "PayGroupCode": "PG1",
                    "AnnualSalary": 95000,
                    "CurrencyCode": "USD",
                },
                {
                    "EmployeeIdentifier": "emp_mock_002",
                    "PayGroupCode": "PG1",
                    "AnnualSalary": 120000,
                    "CurrencyCode": "USD",
                },
            ]
        )

    @route("GET", "/personnel/v1/pto-plans", writes=False)
    async def pto_plans_list(self, request, **kw):
        return MockResponse(
            body=[
                {"PtoPlanCode": "PTO_VAC", "Description": "Vacation", "AccrualMethod": "Annual"},
                {"PtoPlanCode": "PTO_SICK", "Description": "Sick", "AccrualMethod": "Annual"},
            ]
        )

    @route("GET", "/configuration/v1/company-details", writes=False)
    async def company_details(self, request, **kw):
        return MockResponse(
            body=[
                {"CompanyCode": "CC001", "CompanyName": "Verifiabl Inc", "CountryCode": "USA"},
            ]
        )

    @route("GET", "/configuration/v1/jobs", writes=False)
    async def jobs_list(self, request, **kw):
        return MockResponse(
            body=[
                {"Code": "ENG", "Description": "Engineer", "JobFamily": "Technology"},
                {"Code": "MGR", "Description": "Manager", "JobFamily": "Management"},
            ]
        )

    @route("POST", "/personnel/v1/employee-ids", writes=False)
    async def employee_ids_lookup(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "EmployeeIdentifier": "emp_mock_001",
                    "AlternateIdType": "Badge",
                    "AlternateIdValue": "BADGE001",
                },
            ]
        )

    @route("POST", "/payroll/v1/employees/pay-statements")
    async def pay_statements(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "PayIdentifier": "pay_mock_001",
                    "EmployeeIdentifier": "emp_mock_001",
                    "PayDate": "2024-03-15",
                    "GrossPay": 3653.85,
                },
                {
                    "PayIdentifier": "pay_mock_002",
                    "EmployeeIdentifier": "emp_mock_002",
                    "PayDate": "2024-03-15",
                    "GrossPay": 4615.38,
                },
            ]
        )
