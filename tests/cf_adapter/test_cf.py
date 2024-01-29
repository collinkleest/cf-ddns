import unittest
from unittest.mock import MagicMock, patch
from src.cf_adapter.cf import CfAdapter  # Assuming your file is named cf_adapter.py

class TestCfAdapter(unittest.TestCase):

    def setUp(self):
        self.cf_adapter = CfAdapter(api_key='your_api_key', cf_email='your_email',
                                    zone_ids='zone_id_1, zone_id_2', ip_address='your_ip_address')

    @patch('requests.get')
    def test_fetch_domains_success(self, mock_get):
        # Mocking the requests.get method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': [{'name': 'example.com', 'type': 'A', 'content': '127.0.0.1'}]}
        mock_get.return_value = mock_response

        result = self.cf_adapter.fetch_domains('zone_id_1')

        self.assertEqual(result, {'result': [{'name': 'example.com', 'type': 'A', 'content': '127.0.0.1'}]})
        mock_get.assert_called_once_with(
            'https://api.cloudflare.com/client/v4/zones/zone_id_1/dns_records', headers=self.cf_adapter.construct_headers())

    @patch('requests.get')
    def test_fetch_domains_failure(self, mock_get):
        # Mocking the requests.get method for a failure scenario
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.cf_adapter.fetch_domains('zone_id_1')

        self.assertEqual(result, [])
        mock_get.assert_called_once_with(
            'https://api.cloudflare.com/client/v4/zones/zone_id_1/dns_records', headers=self.cf_adapter.construct_headers())

    def test_construct_zone_ids(self):
        result = self.cf_adapter.construct_zone_ids('zone_id_1, zone_id_2')
        self.assertEqual(result, ['zone_id_1', 'zone_id_2'])

    # Add more test cases for other methods as needed

if __name__ == '__main__':
    unittest.main()
