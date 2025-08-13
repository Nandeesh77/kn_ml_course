import logging

# Configure the logger
logging.basicConfig(
    filename='application.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AppException(Exception):
    """
    Custom exception class for the application.
    Captures and logs exceptions.
    """
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception
        self.log_exception()

    def log_exception(self):
        if self.original_exception:
            logging.error(f"{self.message} | Original Exception: {str(self.original_exception)}")
        else:
            logging.error(self.message)

    def __str__(self):
        if self.original_exception:
            return f"{self.message} (Caused by: {str(self.original_exception)})"
        return self.message