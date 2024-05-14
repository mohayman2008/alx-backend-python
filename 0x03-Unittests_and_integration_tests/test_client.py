#!/usr/bin/env python3
'''This module contains unittest test cases for class "GithubOrgClient"
in "client.py"'''
import json
from typing import Dict
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from parameterized import parameterized  # type: ignore

from client import GithubOrgClient


ORG_google_RAW = """
{
  "login": "google",
  "id": 1342004,
  "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
  "url": "https://api.github.com/orgs/google",
  "repos_url": "https://api.github.com/orgs/google/repos",
  "events_url": "https://api.github.com/orgs/google/events",
  "hooks_url": "https://api.github.com/orgs/google/hooks",
  "issues_url": "https://api.github.com/orgs/google/issues",
  "members_url": "https://api.github.com/orgs/google/members{/member}",
  "public_members_url":\
"https://api.github.com/orgs/google/public_members{/member}",
  "avatar_url": "https://avatars.githubusercontent.com/u/1342004?v=4",
  "description": "Google ❤️ Open Source",
  "name": "Google",
  "company": null,
  "blog": "https://opensource.google/",
  "location": "United States of America",
  "email": "opensource@google.com",
  "twitter_username": "GoogleOSS",
  "is_verified": true,
  "has_organization_projects": true,
  "has_repository_projects": true,
  "public_repos": 2635,
  "public_gists": 0,
  "followers": 40503,
  "following": 0,
  "html_url": "https://github.com/google",
  "created_at": "2012-01-18T01:30:18Z",
  "updated_at": "2024-04-19T18:36:13Z",
  "archived_at": null,
  "type": "Organization"
}
"""

ORG_abc_RAW = """
{
  "message": "Not Found",
  "documentation_url": \
"https://docs.github.com/rest/orgs/orgs#get-an-organization"
}
"""

org_google = json.loads(ORG_google_RAW)
org_abc = json.loads(ORG_abc_RAW)


class TestGithubOrgClient(unittest.TestCase):
    '''TestCase for "client.GithubOrgClient" methods and properties'''

    @parameterized.expand([
        ("google", org_google),
        ("abc", org_abc)
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, expected_output: Dict,
                 mock_get_json: MagicMock) -> None:
        '''Testing that function "GithubOrgClient.org" returns the expected
        output'''
        mock_get_json.return_value = expected_output
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_output)

        url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(url)

    @parameterized.expand([
        ("google", org_google),
        ("abc", org_abc)
    ])
    @patch.object(GithubOrgClient, "org", new_callable=PropertyMock)
    def test_public_repos_url(self, org_name: str, org_json: Dict,
                              mock_org: MagicMock) -> None:
        '''Testing that function "GithubOrgClient._public_repos_url" returns
        the expected output'''
        client = GithubOrgClient(org_name)
        mock_org.return_value = org_json
        if "repos_url" in org_json:
            self.assertEqual(client._public_repos_url, org_json["repos_url"])
        else:
            self.assertRaises(KeyError)
