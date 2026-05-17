"""AWS ALB (Application Load Balancer) service integration."""

import boto3
from botocore.exceptions import ClientError
from aws_plumber.ui.theme import print_error


class ALBClient:
    """Wrapper for AWS ALB operations."""

    def __init__(self, region: str):
        """Initialize ALB client."""
        self.region = region
        self.elb_client = boto3.client("elbv2", region_name=region)

    def get_load_balancers(self) -> list[dict]:
        """Get all application load balancers."""
        try:
            response = self.elb_client.describe_load_balancers()
            return response.get("LoadBalancers", [])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to list ALBs [{code}]: {message}")
            return []

    def get_target_groups(self) -> list[dict]:
        """Get ALB target groups."""
        try:
            response = self.elb_client.describe_target_groups()
            return response.get("TargetGroups", [])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to list ALB target groups [{code}]: {message}")
            return []

    def get_target_health(self, target_group_arn: str) -> list[dict]:
        """Get health status of targets in a target group."""
        try:
            response = self.elb_client.describe_target_health(TargetGroupArn=target_group_arn)
            return response.get("TargetHealthDescriptions", [])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to fetch target health for {target_group_arn} [{code}]: {message}"
            )
            return []
