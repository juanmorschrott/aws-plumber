"""Enhanced AWS client combining base EC2/EBS with service extensions."""

from .client import AWSClient
from .waf_extension import WAFClient
from .alb_extension import ALBClient
from typing import Optional


class EnhancedAWSClient(AWSClient):
    """Extended AWS client with additional services."""

    def __init__(self, region: Optional[str] = None):
        """Initialize enhanced AWS client."""
        super().__init__(region)
        self.waf_client: Optional[WAFClient] = None
        self.alb_client: Optional[ALBClient] = None

    def set_region(self, region: str) -> None:
        """Set the AWS region and initialize service clients."""
        super().set_region(region)
        self.waf_client = WAFClient(region)
        self.alb_client = ALBClient(region)

    def modify_volume_size(self, volume_id: str, size: int, dry_run: bool = False) -> bool:
        """Modify EBS volume size with optional dry-run simulation."""
        return super().modify_volume_size(volume_id, size, dry_run=dry_run)

    def detach_volume(self, volume_id: str, instance_id: str, dry_run: bool = False) -> bool:
        """Detach volume with optional dry-run simulation."""
        return super().detach_volume(volume_id, instance_id, dry_run=dry_run)

    def reattach_volume(
        self, volume_id: str, instance_id: str, device: str, dry_run: bool = False
    ) -> bool:
        """Attach volume with optional dry-run simulation."""
        return super().reattach_volume(
            volume_id, instance_id, device, dry_run=dry_run
        )

    def stop_instance(self, instance_id: str, dry_run: bool = False) -> bool:
        """Stop instance with optional dry-run simulation."""
        return super().stop_instance(instance_id, dry_run=dry_run)

    def start_instance(self, instance_id: str, dry_run: bool = False) -> bool:
        """Start instance with optional dry-run simulation."""
        return super().start_instance(instance_id, dry_run=dry_run)
