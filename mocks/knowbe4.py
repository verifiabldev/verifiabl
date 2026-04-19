# CHANGELOG: https://developer.knowbe4.com/rest/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.knowbe4.com/rest/reporting
# SANDBOX:   https://training.knowbe4.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class Knowbe4Mock(BaseMock):
    prefix = "/knowbe4"
    spec_url = "https://developer.knowbe4.com/rest/reporting"
    sandbox_base = "https://us.api.knowbe4.com"

    @route("GET", "/v1/account", writes=False)
    async def get_account(self, request, **kw):
        return MockResponse(
            body={
                "name": "KB4-Demo",
                "type": "paid",
                "domains": ["kb4-demo.com"],
                "admins": [
                    {
                        "id": 974278,
                        "first_name": "Grace",
                        "last_name": "O'Malley",
                        "email": "grace.o@kb4-demo.com",
                    }
                ],
                "subscription_level": "Diamond",
                "subscription_end_date": "2021-03-06",
                "number_of_seats": 25,
                "current_risk_score": 45.742,
            }
        )

    @route("GET", "/v1/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 667542,
                    "employee_number": "19425",
                    "first_name": "William",
                    "last_name": "Marcoux",
                    "job_title": "VP of Sales",
                    "email": "wmarcoux@kb4-demo.com",
                    "phish_prone_percentage": 14.235,
                    "groups": [3264],
                    "current_risk_score": 45.742,
                    "joined_on": "2019-04-02T15:02:38.000Z",
                    "status": "active",
                    "organization": "KB4-Demo",
                },
                {
                    "id": 667543,
                    "employee_number": "19426",
                    "first_name": "Sarah",
                    "last_name": "Thomas",
                    "job_title": "Engineer",
                    "email": "s_thomas@kb4-demo.com",
                    "phish_prone_percentage": 8.1,
                    "groups": [3264],
                    "current_risk_score": 38.2,
                    "joined_on": "2019-04-02T15:02:38.000Z",
                    "status": "active",
                    "organization": "KB4-Demo",
                },
            ]
        )

    @route("GET", "/v1/users/{user_id}", writes=False)
    async def get_user(self, request, user_id="", **kw):
        return MockResponse(
            body={
                "id": int(user_id) if user_id.isdigit() else 667542,
                "employee_number": "19425",
                "first_name": "William",
                "last_name": "Marcoux",
                "job_title": "VP of Sales",
                "email": "wmarcoux@kb4-demo.com",
                "phish_prone_percentage": 14.235,
                "groups": [3264],
                "current_risk_score": 45.742,
                "joined_on": "2019-04-02T15:02:38.000Z",
                "status": "active",
                "organization": "KB4-Demo",
            }
        )

    @route("GET", "/v1/groups", writes=False)
    async def list_groups(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": 3142,
                    "name": "Customer Service",
                    "group_type": "console_group",
                    "member_count": 42,
                    "current_risk_score": 45.742,
                    "status": "active",
                },
                {
                    "id": 3264,
                    "name": "All Users",
                    "group_type": "console_group",
                    "member_count": 25,
                    "current_risk_score": 45.742,
                    "status": "active",
                },
            ]
        )

    @route("GET", "/v1/groups/{group_id}", writes=False)
    async def get_group(self, request, group_id="", **kw):
        return MockResponse(
            body={
                "id": int(group_id) if group_id.isdigit() else 3142,
                "name": "Customer Service",
                "group_type": "console_group",
                "member_count": 42,
                "current_risk_score": 45.742,
                "status": "active",
            }
        )

    @route("GET", "/v1/groups/{group_id}/members", writes=False)
    async def list_group_members(self, request, group_id="", **kw):
        return MockResponse(
            body=[
                {
                    "id": 667542,
                    "first_name": "William",
                    "last_name": "Marcoux",
                    "email": "wmarcoux@kb4-demo.com",
                    "current_risk_score": 45.742,
                    "status": "active",
                },
            ]
        )

    @route("GET", "/v1/training/campaigns", writes=False)
    async def list_campaigns(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "campaign_id": 4261,
                    "name": "Annual Training",
                    "groups": [{"group_id": 0, "name": "All Users"}],
                    "status": "Completed",
                    "start_date": "2019-04-02T15:02:38.000Z",
                    "end_date": "2019-04-02T15:02:38.000Z",
                },
                {
                    "campaign_id": 4262,
                    "name": "New Employee Policies",
                    "groups": [{"group_id": 3142, "name": "Customer Service"}],
                    "status": "Active",
                    "start_date": "2019-04-02T15:02:38.000Z",
                    "end_date": "2019-05-02T15:02:38.000Z",
                },
            ]
        )

    @route("GET", "/v1/training/campaigns/{campaign_id}", writes=False)
    async def get_campaign(self, request, campaign_id="", **kw):
        return MockResponse(
            body={
                "campaign_id": int(campaign_id) if campaign_id.isdigit() else 4261,
                "name": "Annual Training",
                "groups": [{"group_id": 0, "name": "All Users"}],
                "status": "Completed",
                "start_date": "2019-04-02T15:02:38.000Z",
                "end_date": "2019-04-02T15:02:38.000Z",
            }
        )

    @route("GET", "/v1/training/enrollments", writes=False)
    async def list_enrollments(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "enrollment_id": 1425526,
                    "content_type": "Uploaded Policy",
                    "module_name": "Acceptable Use Policy",
                    "user": {
                        "id": 796742,
                        "first_name": "Sarah",
                        "last_name": "Thomas",
                        "email": "s_thomas@kb4-demo.com",
                    },
                    "campaign_name": "New Employee Policies",
                    "enrollment_date": "2019-04-02T15:02:38.000Z",
                    "status": "Passed",
                    "time_spent": 2340,
                },
                {
                    "enrollment_id": 1425527,
                    "content_type": "Store Purchase",
                    "module_name": "Security Awareness Training",
                    "user": {
                        "id": 667542,
                        "first_name": "William",
                        "last_name": "Marcoux",
                        "email": "wmarcoux@kb4-demo.com",
                    },
                    "campaign_name": "Annual Training",
                    "enrollment_date": "2019-04-02T15:02:38.000Z",
                    "status": "Passed",
                    "time_spent": 2520,
                },
            ]
        )

    @route("GET", "/v1/training/enrollments/{enrollment_id}", writes=False)
    async def get_enrollment(self, request, enrollment_id="", **kw):
        return MockResponse(
            body={
                "enrollment_id": int(enrollment_id) if enrollment_id.isdigit() else 1425526,
                "content_type": "Uploaded Policy",
                "module_name": "Acceptable Use Policy",
                "user": {
                    "id": 796742,
                    "first_name": "Sarah",
                    "last_name": "Thomas",
                    "email": "s_thomas@kb4-demo.com",
                },
                "campaign_name": "New Employee Policies",
                "enrollment_date": "2019-04-02T15:02:38.000Z",
                "completion_date": "2019-04-02T15:02:38.000Z",
                "status": "Passed",
                "time_spent": 2340,
            }
        )

    @route("GET", "/v1/training/policies", writes=False)
    async def list_policies(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "policy_id": 2420,
                    "content_type": "Uploaded Policy",
                    "name": "Physical Security Policy",
                    "minimum_time": 3,
                    "default_language": "en-us",
                    "status": 1,
                },
                {
                    "policy_id": 2421,
                    "content_type": "Uploaded Policy",
                    "name": "Security Awareness Policy",
                    "minimum_time": 3,
                    "default_language": "en-us",
                    "status": 1,
                },
            ]
        )

    @route("GET", "/v1/training/policies/{policy_id}", writes=False)
    async def get_policy(self, request, policy_id="", **kw):
        return MockResponse(
            body={
                "policy_id": int(policy_id) if policy_id.isdigit() else 2420,
                "content_type": "Uploaded Policy",
                "name": "Physical Security Policy",
                "minimum_time": 3,
                "default_language": "en-us",
                "status": 1,
            }
        )
