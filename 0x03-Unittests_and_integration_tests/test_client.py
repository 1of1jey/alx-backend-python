#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        
        Args:
            org_name: The organization name to test
            mock_get_json: Mock for the get_json function
        """
        # Set up the mock return value
        expected_result = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_result
        
        # Create instance of GithubOrgClient
        client = GithubOrgClient(org_name)
        
        # Call the org property
        result = client.org
        
        # Assert that the result matches the expected value
        self.assertEqual(result, expected_result)
        
        # Assert that get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()

