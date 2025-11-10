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

        This test ensures that:
        - The org property returns the correct value from get_json
        - get_json is called exactly once with the correct URL
        - No actual HTTP calls are made
        """
        # Set up mock return value
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Create client instance and access org property
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)

        # Verify get_json was called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the expected URL.

        This test ensures that:
        - The _public_repos_url property returns the correct repos_url
        - It correctly extracts the repos_url from the org payload
        """
        # Define the expected payload with repos_url
        expected_payload = {
            "login": "google",
            "id": 12345,
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        # Configure the mock to return our payload
        mock_org.return_value = expected_payload

        # Create client instance
        client = GithubOrgClient("google")

        # Access _public_repos_url and verify it returns the correct URL
        result = client._public_repos_url

        # Assert that the result is the expected repos_url
        self.assertEqual(result, expected_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repos.

        This test ensures that:
        - public_repos returns the correct list of repository names
        - get_json is called once
        - _public_repos_url is accessed once
        """
        # Define the payload that get_json will return
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "bsd-3-clause"}},
        ]

        # Configure mock_get_json to return our test payload
        mock_get_json.return_value = test_payload

        # Use patch as context manager to mock _public_repos_url
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            # Set the return value for _public_repos_url
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            # Create client instance and call public_repos
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]

            # Assert that the result matches expected repo names
            self.assertEqual(result, expected_repos)

            # Assert that _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()

        # Assert that get_json was called once
        mock_get_json.assert_called_once()


if __name__ == "__main__":
    unittest.main()
