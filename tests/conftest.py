"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def mock_aws_client():
    """Mock AWS client for testing."""
    from unittest.mock import MagicMock
    from aws_plumber.aws import AWSClient

    client = AWSClient(region="us-east-1")
    client.ec2_client = MagicMock()
    client.ec2 = MagicMock()
    return client
