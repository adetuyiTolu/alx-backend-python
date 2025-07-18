import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
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


if __name__ == "__main__":
    unittest.main()
