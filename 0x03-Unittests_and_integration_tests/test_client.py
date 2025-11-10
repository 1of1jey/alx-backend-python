#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up a mock for requests.get before running tests."""
        cls.get_patcher = patch('requests.get')

        # Start patcher and get mock object
        mock_get = cls.get_patcher.start()

        # Create a side_effect function to simulate different API responses
        def get_json_side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response = MagicMock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == cls.org_payload.get("repos_url"):
                mock_response = MagicMock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response

        # Set side_effect for mock_get
        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos returns repos filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
