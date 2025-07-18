#!/usr/bin/env python3
"""
    Unit tests for client.py
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @patch("client.get_json")
    def test_public_repos(self, mock_get):
        """Unit-test public_repos method"""

        expected_payload = [
            {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
            {"id": 2, "name": "repo2", "license": {"key": "other"}},
        ]
        mock_get.return_value = expected_payload

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_url:
            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit test for has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos,
    }
    for org_payload, repos_payload,
    expected_repos, apache2_repos in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""
    @classmethod
    def setUpClass(cls):
        """Patch requests.get to mock external HTTP responses."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Setup mock response per call
        def side_effect(url):
            mock_response = Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by Apache-2.0 license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(
            license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
