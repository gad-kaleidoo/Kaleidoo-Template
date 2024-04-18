import logging
import sys
from jsonFormatter import JsonFormatter
import config
import utils

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure all logging is captured by handlers, if not, add a StreamHandler with JsonFormatter
if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)

class ServiceHandler:
    """Handles interactions with different service managers based on type."""
    
    def __init__(self):
        self.managers = {
            "email": self.handle_email_service,
            "document": self.handle_document_service,
            "voice": self.handle_voice_service
        }

    def handle_email_service(self, details):
        """Handles email related services."""
        # Example function that might interact with an email service manager
        email_type = details.get("type")
        logger.info(f"Handling email service for type: {email_type}")
        return {"status": "Processed", "type": email_type}

    def handle_document_service(self, details):
        """Handles document processing services."""
        document_type = details.get("type")
        logger.info(f"Handling document service for type: {document_type}")
        return {"status": "Processed", "type": document_type}

    def handle_voice_service(self, details):
        """Handles voice processing services."""
        voice_type = details.get("type")
        logger.info(f"Handling voice service for type: {voice_type}")
        return {"status": "Processed", "type": voice_type}

    def get_connection_details(self, connection_type):
        """Fetches connection details from the configuration based on type."""
        url = f"{config.SOFT_LIST_URL}/{connection_type}/details"
        return utils.get(url)

    def process_request(self, service_type, details):
        """Process request based on service type."""
        if service_type in self.managers:
            return self.managers[service_type](details)
        else:
            error_msg = f"No manager defined for service type: {service_type}"
            logger.error(error_msg)
            return {"Error": error_msg}

