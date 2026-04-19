# CHANGELOG: https://clay.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://claydocs.claygenius.io/  (community; official at university.clay.com/docs)
# SANDBOX:   https://app.clay.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (API key from Settings)
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: 10 endpoints for tables, records, person/company enrichment to cover prospect-research agent workflows.
class ClayMock(BaseMock):
    prefix = "/clay"
    spec_url = "https://claydocs.claygenius.io/"
    sandbox_base = "https://api.clay.com"

    @route("GET", "/v1/me", writes=False)
    async def get_me(self, request, **kw):
        return MockResponse(
            body={
                "id": "user_mock_verifiabl",
                "email": "dev@verifiabl.dev",
                "name": "Mock User",
                "created_at": 1710400000,
            }
        )

    @route("GET", "/v1/tables", writes=False)
    async def list_tables(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "tbl_mock_001",
                        "name": "Leads",
                        "created_at": 1710400000,
                        "row_count": 42,
                    },
                    {
                        "id": "tbl_mock_002",
                        "name": "Companies",
                        "created_at": 1710400001,
                        "row_count": 12,
                    },
                ],
            }
        )

    @route("GET", "/v1/tables/{table_id}", writes=False)
    async def get_table(self, request, table_id="", **kw):
        return MockResponse(
            body={
                "id": table_id or "tbl_mock_001",
                "name": "Leads",
                "created_at": 1710400000,
                "row_count": 42,
            }
        )

    @route("POST", "/v1/tables")
    async def create_table(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "tbl_mock_new",
                "name": "New Table",
                "created_at": 1710400000,
                "row_count": 0,
            },
        )

    @route("GET", "/v1/tables/{table_id}/records", writes=False)
    async def list_records(self, request, table_id="", **kw):
        return MockResponse(
            body={
                "records": [
                    {
                        "id": "rec_mock_001",
                        "cells": {"name": "Jane Doe", "email": "jane@verifiabl.dev"},
                    },
                    {
                        "id": "rec_mock_002",
                        "cells": {"name": "John Smith", "email": "john@verifiabl.dev"},
                    },
                ],
            }
        )

    @route("POST", "/v1/tables/{table_id}/records")
    async def add_records(self, request, table_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "records": [
                    {"id": "rec_mock_new", "cells": {}},
                ],
            },
        )

    @route("GET", "/v1/tables/{table_id}/count", writes=False)
    async def get_table_count(self, request, table_id="", **kw):
        return MockResponse(body={"count": 42})

    @route("POST", "/v1/people/enrich")
    async def enrich_person(self, request, **kw):
        return MockResponse(
            body={
                "id": "enr_person_mock_001",
                "full_name": "Jane Doe",
                "email": "jane@verifiabl.dev",
                "linkedin_url": "https://linkedin.com/in/janedoe",
                "company_name": "Acme Inc",
                "job_title": "VP Engineering",
                "created_at": 1710400000,
            }
        )

    @route("POST", "/v1/companies/enrich")
    async def enrich_company(self, request, **kw):
        return MockResponse(
            body={
                "id": "enr_company_mock_001",
                "name": "Acme Inc",
                "domain": "verifiabl.dev",
                "industry": "Software",
                "employee_count": 150,
                "revenue_range": "$10M-$50M",
                "created_at": 1710400000,
            }
        )

    @route("GET", "/v1/companies/search", writes=False)
    async def search_companies(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "co_mock_001",
                        "name": "Acme Inc",
                        "domain": "verifiabl.dev",
                        "industry": "Software",
                    },
                    {
                        "id": "co_mock_002",
                        "name": "Beta Corp",
                        "domain": "beta.verifiabl.dev",
                        "industry": "Technology",
                    },
                ],
            }
        )
