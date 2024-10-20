import unittest
from unittest.mock import patch, MagicMock
from src.utils.ip_util import IPUtility
from src.utils.logger import Logger


class TestIPUtility(unittest.TestCase):

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.logger = Logger("cf-ddns.log").get_logger()

    @patch("requests.get")
    def test_get_public_ip_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "fake_ip"}
        mock_get.return_value = mock_response

        ip_utility = IPUtility()

        result = ip_utility.get_public_ip(self.logger)

        self.assertEqual(result, "fake_ip")

    @patch("requests.get")
    def test_get_public_ip_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        ip_utility = IPUtility()

        result = ip_utility.get_public_ip(self.logger)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
