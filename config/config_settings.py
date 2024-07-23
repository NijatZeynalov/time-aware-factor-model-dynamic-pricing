

import yaml
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def get_config(config_path):
    """
    Load configuration settings from a YAML file.
    Args:
        config_path (str): Path to the YAML configuration file.
    Returns:
        dict: Configuration settings.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration from {config_path}: {e}")
        raise

