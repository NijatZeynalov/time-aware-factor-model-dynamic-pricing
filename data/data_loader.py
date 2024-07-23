import os
import pandas as pd
import numpy as np
import logging
from config.config_settings import get_config
from utils.logger import setup_logging

# Initialize logger
setup_logging()
logger = logging.getLogger(__name__)

# Configuration Handling
CONFIG_PATH = 'config/development.yaml'
config = get_config(CONFIG_PATH)

# Cache to speed up data loading for large datasets
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def load_data(file_path):
    """
    Load data from an Excel file.
    Args:
        file_path (str): Path to the Excel file.
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        logger.info(f"Loading data from file: {file_path}")
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise

def validate_data(data, schema):
    """
    Validate the loaded data against the expected schema.
    Args:
        data (pd.DataFrame): Data to validate.
        schema (dict): Expected schema as a dictionary.
    Returns:
        bool: True if data is valid, False otherwise.
    """
    for column, dtype in schema.items():
        if column not in data.columns or not np.issubdtype(data[column].dtype, dtype):
            logger.error(f"Column {column} does not match expected type {dtype}.")
            return False
    return True

def preprocess_data(data):
    """
    Preprocess the loaded data.
    Args:
        data (pd.DataFrame): Data to preprocess.
    Returns:
        pd.DataFrame: Preprocessed data.
    """
    try:
        logger.info("Starting data preprocessing...")
        # Data cleaning
        data = data.dropna()  # Drop missing values
        # Normalize price
        data['Price_Paid'] = (data['Price_Paid'] - data['Price_Paid'].mean()) / data['Price_Paid'].std()
        # Feature extraction
        logger.info("Data preprocessing completed successfully.")
        return data
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise