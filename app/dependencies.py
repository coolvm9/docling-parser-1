import logging
from app.core.logging import setup_logging

# Set up logging configuration
setup_logging()

# Get the logger for this module
logger = logging.getLogger(__name__)

# ...existing code...