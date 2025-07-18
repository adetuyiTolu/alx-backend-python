#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    """unit test for client.py
    """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Test that GithubOrgClient.org returns the correct value"""
        expected = {"login": org_name, "id": 123}
        mock_get.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property"""

        expected_url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {"repos_url": expected_url}

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
