"""Base AWS client for EC2 and EBS operations."""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional
from ..ui.theme import print_error, print_info


class AWSClient:
    """Wrapper for AWS EC2/EBS service operations."""

    def __init__(self, region: Optional[str] = None):
        """Initialize AWS client with optional region."""
        self.region = region or boto3.session.Session().region_name
        self.ec2 = None
        self.ec2_client = None

    def validate_credentials(self) -> bool:
        """Validate AWS credentials are available."""
        try:
            sts = boto3.client("sts", region_name=self.region)
            sts.get_caller_identity()
            return True
        except NoCredentialsError:
            print_error("AWS credentials not found")
            return False
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"AWS credential validation failed [{code}]: {message}")
            return False

    def get_regions(self) -> list[str]:
        """Get list of available AWS regions."""
        try:
            ec2 = boto3.client("ec2")
            response = ec2.describe_regions()
            return sorted([r["RegionName"] for r in response["Regions"]])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to fetch AWS regions [{code}]: {message}")
            return []

    def set_region(self, region: str) -> None:
        """Set the AWS region."""
        self.region = region
        self.ec2 = boto3.resource("ec2", region_name=region)
        self.ec2_client = boto3.client("ec2", region_name=region)

    def get_instances(self) -> list[dict]:
        """Get list of running/stopped EC2 instances."""
        if not self.ec2_client:
            return []
        try:
            instances = []
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        "Name": "instance-state-name",
                        "Values": ["pending", "running", "stopping", "stopped"],
                    }
                ]
            )
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    state = instance.get("State", {}).get("Name", "unknown")
                    if state in ["running", "stopped", "stopping"]:
                        tags = {
                            tag["Key"]: tag["Value"]
                            for tag in instance.get("Tags", [])
                            if "Key" in tag and "Value" in tag
                        }
                        instances.append(
                            {
                                "id": instance["InstanceId"],
                                "name": tags.get("Name", "N/A"),
                                "state": state,
                                "type": instance.get("InstanceType", "N/A"),
                                "az": instance.get("Placement", {}).get(
                                    "AvailabilityZone", "N/A"
                                ),
                            }
                        )
            return sorted(instances, key=lambda x: x["name"])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to fetch EC2 instances [{code}]: {message}")
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
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to fetch volumes for instance {instance_id} [{code}]: {message}"
            )
            return []

    def modify_volume_size(self, volume_id: str, size: int, dry_run: bool = False) -> bool:
        """Modify EBS volume size."""
        if not self.ec2_client:
            return False
        if dry_run:
            print_info(f"[DRY-RUN] Would modify volume {volume_id} to {size}GB")
            return True
        try:
            self.ec2_client.modify_volume(VolumeId=volume_id, Size=size)
            return True
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to modify volume {volume_id} [{code}]: {message}")
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
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to fetch modification status for volume {volume_id} [{code}]: {message}"
            )
            return []

    def detach_volume(self, volume_id: str, instance_id: str, dry_run: bool = False) -> bool:
        """Detach volume from instance."""
        if not self.ec2_client:
            return False
        if dry_run:
            print_info(
                f"[DRY-RUN] Would detach volume {volume_id} from instance {instance_id}"
            )
            return True
        try:
            self.ec2_client.detach_volume(VolumeId=volume_id, InstanceId=instance_id)
            return True
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to detach volume {volume_id} from instance {instance_id} [{code}]: {message}"
            )
            return False

    def reattach_volume(
        self, volume_id: str, instance_id: str, device: str, dry_run: bool = False
    ) -> bool:
        """Reattach volume to instance."""
        if not self.ec2_client:
            return False
        if dry_run:
            print_info(
                f"[DRY-RUN] Would attach volume {volume_id} to instance {instance_id} on {device}"
            )
            return True
        try:
            self.ec2_client.attach_volume(
                VolumeId=volume_id, InstanceId=instance_id, Device=device
            )
            return True
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(
                f"Failed to attach volume {volume_id} to instance {instance_id} [{code}]: {message}"
            )
            return False

    def stop_instance(self, instance_id: str, dry_run: bool = False) -> bool:
        """Stop an EC2 instance."""
        if not self.ec2_client:
            return False
        if dry_run:
            print_info(f"[DRY-RUN] Would stop instance {instance_id}")
            return True
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            return True
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to stop instance {instance_id} [{code}]: {message}")
            return False

    def start_instance(self, instance_id: str, dry_run: bool = False) -> bool:
        """Start an EC2 instance."""
        if not self.ec2_client:
            return False
        if dry_run:
            print_info(f"[DRY-RUN] Would start instance {instance_id}")
            return True
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            return True
        except ClientError as error:
            code = error.response["Error"]["Code"]
            message = error.response["Error"]["Message"]
            print_error(f"Failed to start instance {instance_id} [{code}]: {message}")
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
