"""AWS WAF service integration."""

import boto3
from botocore.exceptions import ClientError
from typing import Optional
from ..ui.theme import print_error


class WAFClient:
    """Wrapper for AWS WAF operations."""

    def __init__(self, region: str):
        """Initialize WAF client."""
        self.region = region
        self.waf_client = boto3.client("wafv2", region_name=region)
        self.logs_client = boto3.client("logs", region_name=region)

    def list_waf_resources(self, scope: str = "REGIONAL") -> list[dict]:
        """List WAF Web ACLs."""
        try:
            response = self.waf_client.list_web_acls(Scope=scope)
            return response.get("WebACLs", [])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to list WAF Web ACLs [{code}]: {message}")
            return []

    def get_waf_logs_config(self, web_acl_arn: str) -> Optional[dict]:
        """Get WAF logging configuration for a Web ACL."""
        try:
            response = self.waf_client.get_logging_configuration(ResourceArn=web_acl_arn)
            return response.get("LoggingConfiguration")
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to fetch WAF logging configuration for {web_acl_arn} [{code}]: {message}"
            )
            return None

    def get_recent_blocking_events(
        self, log_group_name: str, minutes: int = 15
    ) -> list[dict]:
        """Get recent WAF blocking events from CloudWatch Logs."""
        try:
            import time

            start_time = int((time.time() - minutes * 60) * 1000)
            end_time = int(time.time() * 1000)

            query = """
            fields @timestamp, httpRequest.clientIp, httpRequest.uri, action, ruleGroupList, terminatingRuleId
            | filter action = "BLOCK"
            | stats count() as block_count by terminatingRuleId, ruleGroupList
            | sort block_count desc
            """

            response = self.logs_client.start_query(
                logGroupName=log_group_name,
                startTime=start_time,
                endTime=end_time,
                queryString=query,
            )

            query_id = response["queryId"]

            # Wait for query to complete
            import time as time_module

            max_attempts = 30
            for _ in range(max_attempts):
                response = self.logs_client.get_query_results(queryId=query_id)
                if response["status"] == "Complete":
                    break
                time_module.sleep(0.1)

            results = []
            for record in response.get("results", []):
                result = {}
                for field in record:
                    result[field["field"]] = field["value"]
                results.append(result)

            return results
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to fetch WAF blocking events from {log_group_name} [{code}]: {message}"
            )
            return []
