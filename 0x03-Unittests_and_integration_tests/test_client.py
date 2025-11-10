#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
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
        """Set up patcher for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Mock responses for org and repos URLs
        def get_json_side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                return MockResponse(cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)

        # Helper mock response
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

