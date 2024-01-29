import unittest
from unittest.mock import patch
from src.utils.env_manager import EnvironmentManager

class TestEnvironmentManager(unittest.TestCase):
    @patch('os.environ.get')
    def test_get_environment_variable_exists(self, mock_get):
        mock_get.return_value = 'test_value'
        key = 'TEST_KEY'
        result = EnvironmentManager.get_environment_variable(key)
        self.assertEqual(result, 'test_value')

    @patch('os.environ.get')
    def test_get_environment_variable_not_exists(self, mock_get):
        mock_get.return_value = None
        key = 'NON_EXISTING_KEY'
        with self.assertRaises(Exception) as context:
            EnvironmentManager.get_environment_variable(key)

        self.assertIn('Environment variable NON_EXISTING_KEY not found.', str(context.exception))

if __name__ == '__main__':
    unittest.main()