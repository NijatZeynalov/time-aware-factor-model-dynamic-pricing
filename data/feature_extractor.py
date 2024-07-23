import pandas as pd
import numpy as np
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def extract_temporal_features(data):
    """
    Extract temporal features from purchase date and time.
    Args:
        data (pd.DataFrame): Raw data with 'Purchase_Date' and 'Purchase_Time'.
    Returns:
        pd.DataFrame: Data with new temporal features.
    """
    try:
        logger.info("Extracting temporal features...")
        logger.info(f"Before extraction, data columns: {data.columns}")
        # Convert 'Purchase_Date' to datetime
        data['Purchase_Date'] = pd.to_datetime(data['Purchase_Date'])
        data['Year'] = data['Purchase_Date'].dt.year
        data['Month'] = data['Purchase_Date'].dt.month
        data['Day'] = data['Purchase_Date'].dt.day
        data['DayOfWeek'] = data['Purchase_Date'].dt.dayofweek
        data['Hour'] = data['Purchase_Time'].apply(lambda x: int(x.split(':')[0]))
        logger.info("Temporal features extracted successfully.")
        logger.info(f"After extraction, data columns: {data.columns}")
        return data
    except Exception as e:
        logger.error(f"Error extracting temporal features: {e}")
        raise

def extract_location_features(data):
    """
    Extract location-based features.
    Args:
        data (pd.DataFrame): Raw data with 'Location'.
    Returns:
        pd.DataFrame: Data with location features.
    """
    try:
        logger.info("Extracting location features...")
        # Example: One-hot encode 'Location'
        location_dummies = pd.get_dummies(data['Location'], prefix='Loc')
        data = pd.concat([data, location_dummies], axis=1)
        logger.info("Location features extracted successfully.")
        return data
    except Exception as e:
        logger.error(f"Error extracting location features: {e}")
        raise

def extract_features(data):
    """
    Extract all relevant features from raw data.
    Args:
        data (pd.DataFrame): Raw data.
    Returns:
        pd.DataFrame: Data with extracted features.
    """
    try:
        logger.info("Starting feature extraction...")
        data = extract_temporal_features(data)
        data = extract_location_features(data)
        # Drop original columns if no longer needed
        data.drop(columns=['Purchase_Time', 'Location'], inplace=True)
        logger.info("Feature extraction completed successfully.")
        return data
    except Exception as e:
        logger.error(f"Error during feature extraction: {e}")
        raise