# CHANGELOG: https://www.rippling.com/blog (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.rippling.com/documentation/base-api
# SANDBOX:   https://developer.rippling.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class RipplingMock(BaseMock):
    prefix = "/rippling"
    spec_url = "https://developer.rippling.com/documentation/base-api"
    sandbox_base = "https://api.rippling.com"

    @route("GET", "/platform/api/me", writes=False)
    async def me(self, request, **kw):
        return MockResponse(
            body={
                "id": "user_mock_verifiabl",
                "company_id": "company_mock_001",
                "email": "dev@verifiabl.dev",
                "first_name": "Dev",
                "last_name": "Mock",
            }
        )

    @route("GET", "/platform/api/employees", writes=False)
    async def list_employees(self, request, **kw):
        return MockResponse(
            body={
                "employees": [
                    {
                        "id": "emp_mock_001",
                        "user_id": "user_mock_001",
                        "first_name": "Alice",
                        "last_name": "Acme",
                        "work_email": "alice@verifiabl.dev",
                        "employment_type": "SALARIED_FT",
                        "title": "Engineer",
                        "department": "Engineering",
                        "role_state": "ACTIVE",
                    },
                    {
                        "id": "emp_mock_002",
                        "user_id": "user_mock_002",
                        "first_name": "Bob",
                        "last_name": "Acme",
                        "work_email": "bob@verifiabl.dev",
                        "employment_type": "SALARIED_FT",
                        "title": "Manager",
                        "department": "Engineering",
                        "role_state": "ACTIVE",
                    },
                ],
            }
        )

    @route("GET", "/platform/api/employees/include_terminated", writes=False)
    async def list_employees_include_terminated(self, request, **kw):
        return MockResponse(
            body={
                "employees": [
                    {
                        "id": "emp_mock_001",
                        "user_id": "user_mock_001",
                        "first_name": "Alice",
                        "last_name": "Acme",
                        "work_email": "alice@verifiabl.dev",
                        "employment_type": "SALARIED_FT",
                        "title": "Engineer",
                        "department": "Engineering",
                        "role_state": "ACTIVE",
                    },
                    {
                        "id": "emp_mock_002",
                        "user_id": "user_mock_002",
                        "first_name": "Bob",
                        "last_name": "Acme",
                        "work_email": "bob@verifiabl.dev",
                        "employment_type": "SALARIED_FT",
                        "title": "Manager",
                        "department": "Engineering",
                        "role_state": "TERMINATED",
                        "end_date": "2025-01-15",
                    },
                ],
            }
        )

    @route("GET", "/platform/api/employees/{employee_id}", writes=False)
    async def get_employee(self, request, employee_id="", **kw):
        return MockResponse(
            body={
                "id": employee_id or "emp_mock_001",
                "user_id": "user_mock_001",
                "first_name": "Alice",
                "last_name": "Acme",
                "work_email": "alice@verifiabl.dev",
                "employment_type": "SALARIED_FT",
                "title": "Engineer",
                "department": "Engineering",
                "work_location": "San Francisco",
                "role_state": "ACTIVE",
            }
        )

    @route("POST", "/platform/api/employees")
    async def create_employee(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "emp_mock_new",
                "user_id": "user_mock_new",
                "first_name": "New",
                "last_name": "Hire",
                "work_email": "new@verifiabl.dev",
                "role_state": "ACTIVE",
            },
        )

    @route("PATCH", "/platform/api/employees/{employee_id}")
    async def update_employee(self, request, employee_id="", **kw):
        return MockResponse(body={"id": employee_id or "emp_mock_001", "role_state": "ACTIVE"})
