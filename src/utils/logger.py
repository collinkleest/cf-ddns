import logging


class Logger:
    def __init__(self, log_file: str, log_level=logging.DEBUG):
        self.logger = logging.getLogger("cf-ddns")
        self.logger.setLevel(log_level)

        # Prevent adding multiple handlers if logger is already configured
        if not self.logger.hasHandlers():
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            # Create formatter
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # Add formatter to handlers
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
