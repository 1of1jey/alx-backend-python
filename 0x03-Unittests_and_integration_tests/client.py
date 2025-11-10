"""Minimal client module used by unit tests.

Provides:
- get_json(url): small wrapper around requests.get(...).json()
- GithubOrgClient: class with an `org` property that returns organization data

Tests patch `client.get_json`, so this simple implementation is sufficient.
"""
from typing import Any, Dict
import requests


def get_json(url: str) -> Any:
    """Fetch JSON from a URL.

    A thin wrapper over requests.get that raises for bad status codes.
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


class GithubOrgClient:
    """Client to fetch GitHub organization information."""

    def __init__(self, org: str) -> None:
        self._org = org

    @property
    def org(self) -> Dict[str, Any]:
        """Return the organization information fetched from GitHub API."""
        url = f"https://api.github.com/orgs/{self._org}"
        return get_json(url)
