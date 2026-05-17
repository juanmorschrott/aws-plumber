"""Tests for AWS client."""

from unittest.mock import patch, MagicMock
from aws_plumber.aws import AWSClient


def test_aws_client_init():
    """Test AWSClient initialization."""
    client = AWSClient(region="us-east-1")
    assert client.region == "us-east-1"
    assert client.ec2 is None
    assert client.ec2_client is None


@patch("aws_plumber.aws.client.boto3.session.Session")
def test_aws_client_init_no_region(mock_session):
    """Test AWSClient initialization without region."""
    mock_session.return_value.region_name = "eu-west-1"
    client = AWSClient()
    assert client.region == "eu-west-1"
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


@patch("aws_plumber.aws.client.boto3.session.Session")
def test_aws_client_init_no_region_when_session_has_none(mock_session):
    """Test AWSClient initialization keeps region None if boto3 session has no region."""
    mock_session.return_value.region_name = None
    client = AWSClient()
    assert client.region is None


@patch("aws_plumber.aws.client.print_info")
def test_modify_volume_size_dry_run_skips_api_call(mock_print_info):
    """Test dry-run mode skips modify_volume API call."""
    client = AWSClient(region="us-east-1")
    client.ec2_client = MagicMock()

    result = client.modify_volume_size("vol-123", 100, dry_run=True)

    assert result is True
    client.ec2_client.modify_volume.assert_not_called()
    mock_print_info.assert_called_once()
