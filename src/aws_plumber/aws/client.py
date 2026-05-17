"""Base AWS client for EC2 and EBS operations."""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional


class AWSClient:
    """Wrapper for AWS EC2/EBS service operations."""

    def __init__(self, region: Optional[str] = None):
        """Initialize AWS client with optional region."""
        self.region = region
        self.ec2 = None
        self.ec2_client = None

    def validate_credentials(self) -> bool:
        """Validate AWS credentials are available."""
        try:
            sts = boto3.client("sts", region_name=self.region)
            sts.get_caller_identity()
            return True
        except (NoCredentialsError, ClientError):
            return False

    def get_regions(self) -> list[str]:
        """Get list of available AWS regions."""
        try:
            ec2 = boto3.client("ec2")
            response = ec2.describe_regions()
            return sorted([r["RegionName"] for r in response["Regions"]])
        except ClientError:
            return []

    def set_region(self, region: str) -> None:
        """Set the AWS region."""
        self.region = region
        self.ec2 = boto3.resource("ec2", region_name=region)
        self.ec2_client = boto3.client("ec2", region_name=region)

    def get_instances(self) -> list[dict]:
        """Get list of running/stopped EC2 instances."""
        if not self.ec2:
            return []
        try:
            instances = []
            for instance in self.ec2.instances.all():
                if instance.state["Name"] in ["running", "stopped", "stopping"]:
                    instances.append({
                        "id": instance.id,
                        "name": instance.tags.get("Name", "N/A") if instance.tags else "N/A",
                        "state": instance.state["Name"],
                        "type": instance.instance_type,
                        "az": instance.placement["AvailabilityZone"],
                    })
            return sorted(instances, key=lambda x: x["name"])
        except ClientError:
            return []

    def get_instance_volumes(self, instance_id: str) -> list[dict]:
        """Get volumes attached to an instance."""
        if not self.ec2_client:
            return []
        try:
            response = self.ec2_client.describe_volumes(
                Filters=[
                    {"Name": "attachment.instance-id", "Values": [instance_id]},
                ]
            )
            volumes = []
            for vol in response["Volumes"]:
                for attachment in vol["Attachments"]:
                    volumes.append({
                        "id": vol["VolumeId"],
                        "size": vol["Size"],
                        "type": vol["VolumeType"],
                        "state": vol["State"],
                        "device": attachment["Device"],
                        "attachment_id": attachment["AttachmentId"],
                    })
            return volumes
        except ClientError:
            return []

    def modify_volume_size(self, volume_id: str, size: int) -> bool:
        """Modify EBS volume size."""
        if not self.ec2_client:
            return False
        try:
            self.ec2_client.modify_volume(VolumeId=volume_id, Size=size)
            return True
        except ClientError:
            return False

    def get_volume_modifications(self, volume_id: str) -> list[dict]:
        """Get volume modification status."""
        if not self.ec2_client:
            return []
        try:
            response = self.ec2_client.describe_volumes_modifications(
                Filters=[{"Name": "volume-id", "Values": [volume_id]}]
            )
            return response["VolumesModifications"]
        except ClientError:
            return []

    def detach_volume(self, volume_id: str, instance_id: str) -> bool:
        """Detach volume from instance."""
        if not self.ec2_client:
            return False
        try:
            self.ec2_client.detach_volume(VolumeId=volume_id, InstanceId=instance_id)
            return True
        except ClientError:
            return False

    def reattach_volume(self, volume_id: str, instance_id: str, device: str) -> bool:
        """Reattach volume to instance."""
        if not self.ec2_client:
            return False
        try:
            self.ec2_client.attach_volume(
                VolumeId=volume_id, InstanceId=instance_id, Device=device
            )
            return True
        except ClientError:
            return False

    def stop_instance(self, instance_id: str) -> bool:
        """Stop an EC2 instance."""
        if not self.ec2_client:
            return False
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            return True
        except ClientError:
            return False

    def start_instance(self, instance_id: str) -> bool:
        """Start an EC2 instance."""
        if not self.ec2_client:
            return False
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            return True
        except ClientError:
            return False

    def wait_for_volume_available(self, volume_id: str, timeout: int = 300) -> bool:
        """Wait for volume to become available."""
        if not self.ec2_client:
            return False
        try:
            waiter = self.ec2_client.get_waiter("volume_available")
            waiter.wait(VolumeIds=[volume_id], WaiterConfig={"Delay": 5, "MaxAttempts": timeout // 5})
            return True
        except Exception:
            return False

    def wait_for_instance_stopped(self, instance_id: str, timeout: int = 300) -> bool:
        """Wait for instance to stop."""
        if not self.ec2_client:
            return False
        try:
            waiter = self.ec2_client.get_waiter("instance_stopped")
            waiter.wait(InstanceIds=[instance_id], WaiterConfig={"Delay": 5, "MaxAttempts": timeout // 5})
            return True
        except Exception:
            return False

    def wait_for_instance_running(self, instance_id: str, timeout: int = 300) -> bool:
        """Wait for instance to start."""
        if not self.ec2_client:
            return False
        try:
            waiter = self.ec2_client.get_waiter("instance_running")
            waiter.wait(InstanceIds=[instance_id], WaiterConfig={"Delay": 5, "MaxAttempts": timeout // 5})
            return True
        except Exception:
            return False
