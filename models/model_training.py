import logging
import pickle
from models.time_aware_factor_model import TimeAwareFactorModel

# Initialize logger
logger = logging.getLogger(__name__)


def train_model(data, config):
    """
    Train the Time-Aware Factor Model using the preprocessed data.
    Args:
        data (pd.DataFrame): Preprocessed data for training.
        config (dict): Configuration settings for model training.
    Returns:
        model: Trained model.
    """
    try:
        logger.info("Starting model training...")
        logger.info(f"Training data columns: {data.columns}")

        # Initialize the timeSVD++ model
        model = TimeAwareFactorModel(
            n_factors=config['n_factors'],
            lr=config['lr'],
            reg=config['reg'],
            n_epochs=config['n_epochs']
        )

        # Train the model
        model.fit(data)

        logger.info("Model training completed successfully.")
        return model
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise


def save_model(model, model_path):
    """
    Save the trained model to disk.
    Args:
        model: Trained model.
        model_path (str): Path to save the model.
    """
    try:
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")
    except Exception as e:
        logger.error(f"Error saving the model: {e}")
        raise


if __name__ == '__main__':
    from data.data_loader import load_data
    from data.feature_extractor import extract_features
    from config.config_settings import get_config

    # Load configuration
    CONFIG_PATH = 'config/development.yaml'
    config = get_config(CONFIG_PATH)

    # Load and preprocess data
    file_path = 'data/Customer_Purchase_History.xlsx'
    raw_data = load_data(file_path)
    preprocessed_data = extract_features(raw_data)

    # Train model
    model = train_model(preprocessed_data, config['model_training'])

    # Save model
    model_path = 'models/trained_model.pkl'
    save_model(model, model_path)