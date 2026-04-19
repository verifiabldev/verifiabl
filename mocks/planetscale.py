# CHANGELOG: https://planetscale.com/changelog/feed.atom
# SPEC:      https://planetscale.com/docs/api/openapi-spec
# SANDBOX:   https://app.planetscale.com
# SKILL:     —
# MCP:       https://mcp.pscale.dev/mcp/planetscale
# LLMS:      https://planetscale.com/docs/llms.txt
# AUTH:      Bearer token (service token or OAuth) in Authorization header (per OpenAPI securitySchemes)
from mocks.base import BaseMock, route
from models import MockResponse


def _paginated(data: list, page: int = 1):
    return {
        "current_page": page,
        "next_page": page + 1 if len(data) >= 25 else None,
        "next_page_url": None,
        "prev_page": page - 1 if page > 1 else None,
        "prev_page_url": None,
        "data": data,
    }


# LOC EXCEPTION: Pagination envelope helper plus 9 schema-faithful org/database/branch endpoints.
class PlanetScaleMock(BaseMock):
    prefix = "/planetscale"
    spec_url = "https://planetscale.com/docs/api/openapi-spec"
    sandbox_base = "https://api.planetscale.com"

    @route("GET", "/v1/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "org_mock_001",
                        "name": "mock_org",
                        "billing_email": "billing@verifiabl.dev",
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                        "plan": "scaling",
                        "valid_billing_info": True,
                        "sso": False,
                        "sso_directory": False,
                        "single_tenancy": False,
                        "managed_tenancy": False,
                        "has_past_due_invoices": False,
                        "database_count": 2,
                        "sso_portal_url": "",
                        "features": {},
                        "idp_managed_roles": False,
                        "invoice_budget_amount": "0",
                        "keyspace_shard_limit": 1,
                        "has_card": True,
                        "payment_info_required": False,
                    },
                    {
                        "id": "org_mock_002",
                        "name": "other_org",
                        "billing_email": "billing-team@verifiabl.dev",
                        "created_at": "2024-01-15T10:00:00Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                        "plan": "hobby",
                        "valid_billing_info": True,
                        "sso": False,
                        "sso_directory": False,
                        "single_tenancy": False,
                        "managed_tenancy": False,
                        "has_past_due_invoices": False,
                        "database_count": 1,
                        "sso_portal_url": "",
                        "features": {},
                        "idp_managed_roles": False,
                        "invoice_budget_amount": "0",
                        "keyspace_shard_limit": 1,
                        "has_card": False,
                        "payment_info_required": False,
                    },
                ]
            )
        )

    @route("GET", "/v1/organizations/{organization}", writes=False)
    async def get_organization(self, request, organization="", **kw):
        return MockResponse(
            body={
                "id": "org_mock_001",
                "name": organization or "mock_org",
                "billing_email": "billing@verifiabl.dev",
                "created_at": "2023-03-29T16:32:59Z",
                "updated_at": "2026-03-14T12:00:00Z",
                "plan": "scaling",
                "valid_billing_info": True,
                "sso": False,
                "sso_directory": False,
                "single_tenancy": False,
                "managed_tenancy": False,
                "has_past_due_invoices": False,
                "database_count": 2,
                "sso_portal_url": "",
                "features": {},
                "idp_managed_roles": False,
                "invoice_budget_amount": "0",
                "keyspace_shard_limit": 1,
                "has_card": True,
                "payment_info_required": False,
            }
        )

    @route("GET", "/v1/organizations/{organization}/databases", writes=False)
    async def list_databases(self, request, organization="", **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "db_mock_001",
                        "url": "https://api.planetscale.com/v1/organizations/mock_org/databases/app-db",
                        "branches_url": "https://api.planetscale.com/v1/organizations/mock_org/databases/app-db/branches",
                        "branches_count": 2,
                        "open_schema_recommendations_count": 0,
                        "development_branches_count": 1,
                        "production_branches_count": 1,
                        "issues_count": 0,
                        "multiple_admins_required_for_deletion": False,
                        "ready": True,
                        "at_backup_restore_branches_limit": False,
                        "at_development_branch_usage_limit": False,
                    },
                    {
                        "id": "db_mock_002",
                        "url": "https://api.planetscale.com/v1/organizations/mock_org/databases/analytics",
                        "branches_url": "https://api.planetscale.com/v1/organizations/mock_org/databases/analytics/branches",
                        "branches_count": 1,
                        "open_schema_recommendations_count": 0,
                        "development_branches_count": 0,
                        "production_branches_count": 1,
                        "issues_count": 0,
                        "multiple_admins_required_for_deletion": False,
                        "ready": True,
                        "at_backup_restore_branches_limit": False,
                        "at_development_branch_usage_limit": False,
                    },
                ]
            )
        )

    @route("GET", "/v1/organizations/{organization}/databases/{database}", writes=False)
    async def get_database(self, request, organization="", database="", **kw):
        return MockResponse(
            body={
                "id": "db_mock_001",
                "url": f"https://api.planetscale.com/v1/organizations/{organization or 'mock_org'}/databases/{database or 'app-db'}",
                "branches_url": f"https://api.planetscale.com/v1/organizations/{organization or 'mock_org'}/databases/{database or 'app-db'}/branches",
                "branches_count": 2,
                "open_schema_recommendations_count": 0,
                "development_branches_count": 1,
                "production_branches_count": 1,
                "issues_count": 0,
                "multiple_admins_required_for_deletion": False,
                "ready": True,
                "at_backup_restore_branches_limit": False,
                "at_development_branch_usage_limit": False,
            }
        )

    @route("GET", "/v1/organizations/{organization}/databases/{database}/branches", writes=False)
    async def list_branches(self, request, organization="", database="", **kw):
        return MockResponse(
            body=_paginated(
                [
                    {
                        "id": "branch_mock_main",
                        "name": "main",
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                        "production": True,
                        "state": "ready",
                        "ready": True,
                    },
                    {
                        "id": "branch_mock_dev",
                        "name": "develop",
                        "created_at": "2024-06-01T08:00:00Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                        "production": False,
                        "state": "ready",
                        "ready": True,
                    },
                ]
            )
        )

    @route(
        "GET",
        "/v1/organizations/{organization}/databases/{database}/branches/{branch}",
        writes=False,
    )
    async def get_branch(self, request, organization="", database="", branch="", **kw):
        return MockResponse(
            body={
                "id": "branch_mock_main",
                "name": branch or "main",
                "created_at": "2023-03-29T16:32:59Z",
                "updated_at": "2026-03-14T12:00:00Z",
                "deleted_at": None,
                "restore_checklist_completed_at": None,
                "schema_last_updated_at": "2026-03-14T12:00:00Z",
                "kind": "mysql",
                "mysql_address": "main.app-db.mock_org.psdb.cloud:3306",
                "mysql_edge_address": None,
                "state": "ready",
                "direct_vtgate": False,
                "vtgate_size": "small",
                "vtgate_count": 1,
                "cluster_name": "small",
                "cluster_iops": 1000,
                "ready": True,
                "schema_ready": True,
                "metal": False,
                "production": True,
                "safe_migrations": True,
                "sharded": False,
                "shard_count": 0,
            }
        )

    @route("POST", "/v1/organizations/{organization}/databases/{database}/branches")
    async def create_branch(self, request, organization="", database="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "branch_mock_new",
                "name": "feature-xyz",
                "created_at": "2026-03-14T12:00:00Z",
                "updated_at": "2026-03-14T12:00:00Z",
                "deleted_at": None,
                "restore_checklist_completed_at": None,
                "schema_last_updated_at": "2026-03-14T12:00:00Z",
                "kind": "mysql",
                "mysql_address": "feature-xyz.app-db.mock_org.psdb.cloud:3306",
                "mysql_edge_address": None,
                "state": "ready",
                "direct_vtgate": False,
                "vtgate_size": "small",
                "vtgate_count": 1,
                "cluster_name": "small",
                "cluster_iops": 1000,
                "ready": True,
                "schema_ready": True,
                "metal": False,
                "production": False,
                "safe_migrations": True,
                "sharded": False,
                "shard_count": 0,
            },
        )

    @route("DELETE", "/v1/organizations/{organization}/databases/{database}/branches/{branch}")
    async def delete_branch(self, request, organization="", database="", branch="", **kw):
        return MockResponse(status=204, body=None)

    @route(
        "GET",
        "/v1/organizations/{organization}/databases/{database}/branches/{branch}/schema",
        writes=False,
    )
    async def get_branch_schema(self, request, organization="", database="", branch="", **kw):
        return MockResponse(
            body={
                "tables": [
                    {
                        "name": "users",
                        "schema": "CREATE TABLE `users` (\n  `id` bigint NOT NULL AUTO_INCREMENT,\n  `email` varchar(255),\n  PRIMARY KEY (`id`)\n);",
                    },
                    {
                        "name": "posts",
                        "schema": "CREATE TABLE `posts` (\n  `id` bigint NOT NULL AUTO_INCREMENT,\n  `user_id` bigint,\n  `title` varchar(255),\n  PRIMARY KEY (`id`)\n);",
                    },
                ],
            }
        )
