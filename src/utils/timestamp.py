import datetime


class TimestampService:

    @staticmethod
    def get_formatted_timestamp():
        current_datetime = datetime.datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
