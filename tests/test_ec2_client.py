"""Tests for EC2Client."""

from unittest.mock import MagicMock
from aws_plumber.aws import EC2Client


def test_ec2_client_init():
    """Test EC2Client initialization."""
    client = EC2Client(region="us-east-1")
    assert client.region == "us-east-1"
    assert client.ec2 is None
    assert client.ec2_client is None


def test_ec2_client_init_no_region():
    """Test EC2Client initialization without region."""
    mock_session = MagicMock()
    mock_session.region_name = "eu-west-1"
    client = EC2Client(session=mock_session)
    assert client.region == "eu-west-1"
    assert client.ec2 is None
    assert client.ec2_client is None


def test_ec2_client_get_regions():
    """Test getting AWS regions."""
    mock_ec2 = MagicMock()
    mock_ec2.describe_regions.return_value = {
        "Regions": [
            {"RegionName": "us-east-1"},
            {"RegionName": "us-west-2"},
        ]
    }
    mock_session = MagicMock()
    mock_session.region_name = "us-east-1"
    mock_session.client.return_value = mock_ec2

    client = EC2Client(session=mock_session)
    regions = client.get_regions()
    assert len(regions) == 2
    assert "us-east-1" in regions
    assert "us-west-2" in regions


def test_ec2_client_validate_credentials_failure():
    """Test credential validation failure."""
    client = EC2Client()
    result = client.validate_credentials()
    assert result is False


def test_ec2_client_init_no_region_when_session_has_none():
    """Test EC2Client initialization keeps region None if boto3 session has no region."""
    mock_session = MagicMock()
    mock_session.region_name = None
    client = EC2Client(session=mock_session)
    assert client.region is None


def test_modify_volume_size_dry_run_skips_api_call():
    """Test dry-run mode returns True without calling the modify_volume API."""
    client = EC2Client(region="us-east-1")
    client.ec2_client = MagicMock()

    result = client.modify_volume_size("vol-123", 100, dry_run=True)

    assert result is True
    client.ec2_client.modify_volume.assert_not_called()
