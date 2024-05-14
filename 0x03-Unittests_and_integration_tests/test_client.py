#!/usr/bin/env python3
'''This module contains unittest test cases for class "GithubOrgClient"
in "client.py"'''
import json
from typing import Any, Dict
import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from parameterized import parameterized, parameterized_class  # type: ignore
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license` method."""
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls: Any) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self: Any) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self: Any) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls: Any) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()
