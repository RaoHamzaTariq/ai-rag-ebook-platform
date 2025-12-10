import logging
import sys
from datetime import datetime
from typing import Optional
import os

# Create logs directory if it doesn't exist
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging
def setup_logging():
    # Create custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create file handler for general logs
    file_handler = logging.FileHandler(f'logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create error file handler
    error_handler = logging.FileHandler(f'logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Get root logger and configure it
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # Also configure uvicorn loggers to use the same format
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = [file_handler, error_handler, console_handler]

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = [file_handler, error_handler, console_handler]

    return root_logger

# Initialize logging
logger = setup_logging()

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)

def log_agent_decision(session_id: str, query: str, agent_type: str, decision: str, sources: Optional[list] = None):
    """Log agent decisions with relevant context"""
    logger.info(f"Agent Decision - Session: {session_id}, Agent: {agent_type}, Query: {query[:50]}..., Decision: {decision}")
    if sources:
        logger.info(f"Sources used: {len(sources)} for session {session_id}")

def log_error(error_msg: str, session_id: Optional[str] = None):
    """Log an error with optional session context"""
    if session_id:
        logger.error(f"Session {session_id}: {error_msg}")
    else:
        logger.error(error_msg)