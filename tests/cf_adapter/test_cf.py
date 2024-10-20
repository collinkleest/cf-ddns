import unittest
from unittest.mock import patch, MagicMock
from logging import Logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cf_adapter.cf import CfAdapter  # Assuming your class is in cf_adapter.py


class TestCfAdapter(unittest.TestCase):

    def setUp(self):
        self.api_key = "fake-api-key"
        self.cf_email = "test@example.com"
        self.ip_address = "127.0.0.1"
        self.logger = MagicMock(Logger)
        self.adapter = CfAdapter(
            api_key=self.api_key,
            cf_email=self.cf_email,
            ip_address=self.ip_address,
            logger=self.logger,
        )

    @patch("cf_adapter.requests.get")
    def test_get_zone_ids_success(self, mock_get):
        # Mock response for requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [{"id": "zone-id-1"}, {"id": "zone-id-2"}]
        }
        mock_get.return_value = mock_response

        zone_ids = self.adapter.get_zone_ids()

        # Verify the behavior
        self.assertEqual(zone_ids, ["zone-id-1", "zone-id-2"])
        mock_get.assert_called_once_with(
            "https://api.cloudflare.com/client/v4/zones", headers=self.adapter.headers
        )
        self.logger.error.assert_not_called()

    @patch("cf_adapter.requests.get")
    def test_get_zone_ids_failure(self, mock_get):
        # Simulate non-200 status code
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        zone_ids = self.adapter.get_zone_ids()

        # Verify the behavior when the request fails
        self.assertEqual(zone_ids, [])
        mock_get.assert_called_once_with(
            "https://api.cloudflare.com/client/v4/zones", headers=self.adapter.headers
        )
        self.logger.error.assert_called_once_with(
            "Error when getting zone ids: Internal Server Error"
        )

    @patch("cf_adapter.requests.get")
    def test_get_zone_ids_exception(self, mock_get):
        # Simulate an exception during the request
        mock_get.side_effect = Exception("Request failed")

        zone_ids = self.adapter.get_zone_ids()

        # Verify the behavior when an exception is raised
        self.assertEqual(zone_ids, [])
        mock_get.assert_called_once_with(
            "https://api.cloudflare.com/client/v4/zones", headers=self.adapter.headers
        )
        self.logger.error.assert_called_once_with(
            "Exception found when getting zone ids: Request failed"
        )


if __name__ == "__main__":
    unittest.main()
