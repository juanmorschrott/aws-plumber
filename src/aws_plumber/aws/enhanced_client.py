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
