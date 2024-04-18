import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Custom formatter to output logs in JSON format.
    """

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        """
        Initialize the formatter with new format and date format.
        
        Args:
            fmt (str, optional): The format string to use. Defaults to None.
            datefmt (str, optional): The date format string to use. Defaults to None.
            style (str, optional): The style specifier. Defaults to '%'.
            validate (bool, optional): Whether to validate the format string. Defaults to True.
        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        self.datefmt = datefmt if datefmt else "%Y-%m-%d %H:%M:%S"

    def format(self, record):
        """
        Format the specified record as text.
        
        Args:
            record (logging.LogRecord): The record to be formatted.
        
        Returns:
            str: A JSON string representing the formatted log record.
        """
        # Prepare the log message as a dictionary
        log_message = {
            "time": datetime.utcnow().strftime(self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Include exception info if any
        if record.exc_info:
            log_message["exc_info"] = self.formatException(record.exc_info)

        # Include stack trace info if any
        if record.stack_info:
            log_message["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(log_message, ensure_ascii=False)

