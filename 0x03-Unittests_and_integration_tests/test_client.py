#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org method.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        Ensures get_json is called once with the expected URL.
        """
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
