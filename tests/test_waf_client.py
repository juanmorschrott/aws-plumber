"""Tests for WAFClient."""

from unittest.mock import MagicMock
from aws_plumber.aws.waf import WAFClient


def test_waf_client_initialization():
    """Test WAFClient initialization."""
    mock_waf = MagicMock()
    mock_logs = MagicMock()
    waf_client = WAFClient(region="us-east-1", waf_client=mock_waf, logs_client=mock_logs)
    assert waf_client.region == "us-east-1"
    assert waf_client.waf_client is mock_waf
    assert waf_client.logs_client is mock_logs


def test_waf_client_list_resources():
    """Test listing WAF resources."""
    mock_waf = MagicMock()
    mock_waf.list_web_acls.return_value = {
        "WebACLs": [
            {"Name": "test-acl", "ARN": "arn:aws:wafv2:us-east-1:123456789012:global/webacl/test/a1234567"}
        ]
    }

    waf_client = WAFClient(region="us-east-1", waf_client=mock_waf, logs_client=MagicMock())
    resources = waf_client.list_waf_resources("REGIONAL")

    assert len(resources) == 1
    assert resources[0]["Name"] == "test-acl"

