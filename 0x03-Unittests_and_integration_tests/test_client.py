#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
