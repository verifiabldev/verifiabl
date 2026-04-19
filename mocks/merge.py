# CHANGELOG: https://docs.merge.dev (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.merge.dev/hris/overview and https://docs.merge.dev/ats/overview
# SANDBOX:   https://app.merge.dev
# SKILL:     —
# MCP:       —
# LLMS:      —
from typing import Optional

from mocks.base import BaseMock, route
from models import MockResponse


def _paginated(results: list, next_cursor: Optional[str] = None):
    out = {"results": results, "next": next_cursor, "previous": None}
    return out


class MergeMock(BaseMock):
    prefix = "/merge"
    spec_url = "https://docs.merge.dev/get-started/unified-api/"
    sandbox_base = "https://api.merge.dev"

    @route("GET", "/api/hris/v1/employees", writes=False)
    async def list_employees(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "remote_id": "emp_001",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "display_full_name": "Jane Doe",
                        "work_email": "jane@verifiabl.dev",
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "remote_id": "emp_002",
                        "first_name": "John",
                        "last_name": "Smith",
                        "display_full_name": "John Smith",
                        "work_email": "john@verifiabl.dev",
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "cD0yMDI0LTAzLTE0",
            )
        )

    @route("GET", "/api/hris/v1/employees/{id}", writes=False)
    async def get_employee(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "550e8400-e29b-41d4-a716-446655440001",
                "remote_id": "emp_001",
                "first_name": "Jane",
                "last_name": "Doe",
                "display_full_name": "Jane Doe",
                "work_email": "jane@verifiabl.dev",
                "created_at": "2024-03-14T12:00:00.000Z",
                "modified_at": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("GET", "/api/hris/v1/companies", writes=False)
    async def list_companies(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440010",
                        "remote_id": "co_001",
                        "legal_name": "Acme Inc",
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                ]
            )
        )

    @route("GET", "/api/ats/v1/candidates", writes=False)
    async def list_candidates(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440021",
                        "remote_id": "cand_001",
                        "first_name": "Alex",
                        "last_name": "Candidate",
                        "email_addresses": [
                            {"value": "alex@verifiabl.dev", "email_address_type": "PERSONAL"}
                        ],
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440022",
                        "remote_id": "cand_002",
                        "first_name": "Sam",
                        "last_name": "Applicant",
                        "email_addresses": [
                            {"value": "sam@verifiabl.dev", "email_address_type": "WORK"}
                        ],
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                ],
                "cD0yMDI0LTAzLTE0",
            )
        )

    @route("GET", "/api/ats/v1/candidates/{id}", writes=False)
    async def get_candidate(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "550e8400-e29b-41d4-a716-446655440021",
                "remote_id": "cand_001",
                "first_name": "Alex",
                "last_name": "Candidate",
                "email_addresses": [
                    {"value": "alex@verifiabl.dev", "email_address_type": "PERSONAL"}
                ],
                "created_at": "2024-03-14T12:00:00.000Z",
                "modified_at": "2024-03-14T12:00:00.000Z",
            }
        )

    @route("POST", "/api/ats/v1/candidates")
    async def create_candidate(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "550e8400-e29b-41d4-a716-446655440023",
                "remote_id": "cand_new",
                "first_name": "New",
                "last_name": "Candidate",
                "email_addresses": [],
                "created_at": "2024-03-14T12:00:00.000Z",
                "modified_at": "2024-03-14T12:00:00.000Z",
            },
        )

    @route("GET", "/api/ats/v1/jobs", writes=False)
    async def list_jobs(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440031",
                        "remote_id": "job_001",
                        "name": "Software Engineer",
                        "status": "OPEN",
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440032",
                        "remote_id": "job_002",
                        "name": "Product Manager",
                        "status": "OPEN",
                        "created_at": "2024-03-14T12:00:00.000Z",
                        "modified_at": "2024-03-14T12:00:00.000Z",
                    },
                ]
            )
        )

    @route("GET", "/api/ats/v1/jobs/{id}", writes=False)
    async def get_job(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "550e8400-e29b-41d4-a716-446655440031",
                "remote_id": "job_001",
                "name": "Software Engineer",
                "status": "OPEN",
                "created_at": "2024-03-14T12:00:00.000Z",
                "modified_at": "2024-03-14T12:00:00.000Z",
            }
        )
