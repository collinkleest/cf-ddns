import unittest
from src.utils.timestamp import TimestampService
from freezegun import freeze_time


class TestTimestampService(unittest.TestCase):

    @freeze_time("2024-10-19 15:30:45")
    def test_get_formatted_timestamp(self):
        timestamp_service = TimestampService()
        formatted_timestamp = timestamp_service.get_formatted_timestamp()
        expected_timestamp = "2024-10-19 15:30:45"
        self.assertEqual(formatted_timestamp, expected_timestamp)


if __name__ == "__main__":
    unittest.main()
