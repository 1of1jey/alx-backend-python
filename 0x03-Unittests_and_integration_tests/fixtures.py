#!/usr/bin/env python3
org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "truth", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "autopilot", "license": {"key": "mit"}},
]

expected_repos = ["truth", "autopilot"]
apache2_repos = ["truth"]

