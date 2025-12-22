import logging
import os
from datetime import datetime

# Set up logging configuration
def setup_logging():
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set up file handler for authentication events
    auth_log_file = os.path.join(logs_dir, f"auth_{datetime.now().strftime('%Y%m%d')}.log")
    auth_handler = logging.FileHandler(auth_log_file)
    auth_handler.setLevel(logging.INFO)
    auth_handler.setFormatter(formatter)

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(auth_handler)
    root_logger.addHandler(console_handler)

    # Create specific loggers for different components
    auth_logger = logging.getLogger('auth')
    auth_logger.setLevel(logging.INFO)

    db_logger = logging.getLogger('database')
    db_logger.setLevel(logging.INFO)

    return auth_logger, db_logger

# Initialize logging
auth_logger, db_logger = setup_logging()

# Export loggers for use in other modules
__all__ = ['auth_logger', 'db_logger']