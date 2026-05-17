"""Tests for AWS client."""

from unittest.mock import patch, MagicMock
from aws_plumber.aws import AWSClient


def test_aws_client_init():
    """Test AWSClient initialization."""
    client = AWSClient(region="us-east-1")
    assert client.region == "us-east-1"
    assert client.ec2 is None
    assert client.ec2_client is None


def test_aws_client_init_no_region():
    """Test AWSClient initialization without region."""
    client = AWSClient()
    assert client.region is None
    assert client.ec2 is None
    assert client.ec2_client is None


@patch("aws_plumber.aws.client.boto3.client")
def test_aws_client_get_regions(mock_boto_client):
    """Test getting AWS regions."""
    mock_ec2_client = MagicMock()
    mock_boto_client.return_value = mock_ec2_client
    mock_ec2_client.describe_regions.return_value = {
        "Regions": [
            {"RegionName": "us-east-1"},
            {"RegionName": "us-west-2"},
        ]
    }
    
    client = AWSClient()
    regions = client.get_regions()
    assert len(regions) == 2
    assert "us-east-1" in regions
    assert "us-west-2" in regions


def test_aws_client_validate_credentials_failure():
    """Test credential validation failure."""
    client = AWSClient()
    result = client.validate_credentials()
    assert result is False

