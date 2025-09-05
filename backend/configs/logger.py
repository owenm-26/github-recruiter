import logging

logging.basicConfig(
    level=logging.INFO,  # Set the minimum level of messages to capture
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Define log message format
    handlers=[
        logging.StreamHandler()  # Handler to output logs to the console
    ]
)

logger = logging.getLogger(__name__)
