"""
logger.py - Setup logging for the application.

Objective:
    Configure the logging settings for the application to ensure that logs are captured consistently across different modules.
    This script initializes the logging configuration and provides a function to set up logging for the entire application.

Integration with Other Files:
    - All other modules use this logging configuration for consistent logging.

Usage:
    from utils.logger import setup_logging
    setup_logging()
"""

import logging
import logging.config
import yaml

def setup_logging(config_path='config/logging.yaml', default_level=logging.INFO):
    """
    Setup logging configuration.
    Args:
        config_path (str): Path to the logging configuration file.
        default_level (int): Default logging level.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logging.config.dictConfig(config)
            logging.info("Logging configuration loaded successfully from %s", config_path)
    except Exception as e:
        logging.basicConfig(level=default_level)
        logging.error("Error loading logging configuration from %s: %s", config_path, e)
        logging.info("Using default logging configuration.")


