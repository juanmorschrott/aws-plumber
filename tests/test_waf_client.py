"""Tests for WAFClient."""

from unittest.mock import patch, MagicMock
from aws_plumber.aws.waf import WAFClient


@patch("aws_plumber.aws.waf.boto3.client")
def test_waf_client_initialization(mock_boto_client):
    """Test WAFClient initialization."""
    mock_waf_client = MagicMock()
    mock_boto_client.return_value = mock_waf_client

    waf_client = WAFClient(region="us-east-1")
    assert waf_client.region == "us-east-1"
    mock_boto_client.assert_called()


@patch("aws_plumber.aws.waf.boto3.client")
def test_waf_client_list_resources(mock_boto_client):
    """Test listing WAF resources."""
    mock_waf_client = MagicMock()
    mock_boto_client.return_value = mock_waf_client

    mock_waf_client.list_web_acls.return_value = {
        "WebACLs": [
            {"Name": "test-acl", "ARN": "arn:aws:wafv2:us-east-1:123456789012:global/webacl/test/a1234567"}
        ]
    }

    waf_client = WAFClient(region="us-east-1")
    resources = waf_client.list_waf_resources("REGIONAL")

    assert len(resources) == 1
    assert resources[0]["Name"] == "test-acl"

