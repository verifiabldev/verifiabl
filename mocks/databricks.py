# CHANGELOG: https://docs.databricks.com/en/release-notes/index.html  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.databricks.com/api/workspace/introduction
# SANDBOX:   https://example.cloud.databricks.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class DatabricksMock(BaseMock):
    prefix = "/databricks"
    spec_url = "https://docs.databricks.com/api/workspace/introduction"
    sandbox_base = "https://example.cloud.databricks.com"

    @route("GET", "/api/2.0/clusters/list", writes=False)
    async def clusters_list(self, request, **kw):
        return MockResponse(
            body={
                "clusters": [
                    {
                        "cluster_id": "0923-164208-meows279",
                        "cluster_name": "mock_cluster_1",
                        "state": "RUNNING",
                        "spark_context_id": 1,
                    },
                    {
                        "cluster_id": "0923-164209-meows280",
                        "cluster_name": "mock_cluster_2",
                        "state": "TERMINATED",
                        "spark_context_id": 2,
                    },
                ]
            }
        )

    @route("POST", "/api/2.0/clusters/create", writes=True)
    async def clusters_create(self, request, **kw):
        return MockResponse(status=201, body={"cluster_id": "0923-164210-verifiabl"})

    @route("POST", "/api/2.0/clusters/get", writes=False)
    async def clusters_get(self, request, **kw):
        return MockResponse(
            body={
                "cluster_id": "0923-164208-meows279",
                "cluster_name": "mock_cluster_1",
                "state": "RUNNING",
                "spark_version": "14.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
            }
        )

    @route("GET", "/api/2.2/jobs/list", writes=False)
    async def jobs_list(self, request, **kw):
        return MockResponse(
            body={
                "jobs": [
                    {
                        "job_id": 11223344,
                        "created_time": 1710400000000,
                        "creator_user_name": "user@verifiabl.dev",
                        "settings": {"name": "Mock ETL job", "format": "SINGLE_TASK"},
                    },
                    {
                        "job_id": 11223345,
                        "created_time": 1710400001000,
                        "creator_user_name": "user@verifiabl.dev",
                        "settings": {"name": "Mock report job", "format": "MULTI_TASK"},
                    },
                ],
            }
        )

    @route("GET", "/api/2.2/jobs/get", writes=False)
    async def jobs_get(self, request, **kw):
        return MockResponse(
            body={
                "job_id": 11223344,
                "created_time": 1710400000000,
                "creator_user_name": "user@verifiabl.dev",
                "settings": {
                    "name": "Mock ETL job",
                    "format": "SINGLE_TASK",
                    "max_concurrent_runs": 1,
                },
            }
        )

    @route("POST", "/api/2.2/jobs/create", writes=True)
    async def jobs_create(self, request, **kw):
        return MockResponse(status=201, body={"job_id": 99887766})

    @route("POST", "/api/2.2/jobs/runnow", writes=True)
    async def jobs_run_now(self, request, **kw):
        return MockResponse(body={"run_id": 55443322, "number_in_job": 1})

    @route("GET", "/api/2.0/workspace/list", writes=False)
    async def workspace_list(self, request, **kw):
        return MockResponse(
            body={
                "objects": [
                    {
                        "path": "/Users/user@verifiabl.dev/Notebooks",
                        "object_type": "DIRECTORY",
                        "language": None,
                    },
                    {
                        "path": "/Users/user@verifiabl.dev/ETL",
                        "object_type": "NOTEBOOK",
                        "language": "PYTHON",
                    },
                ]
            }
        )
