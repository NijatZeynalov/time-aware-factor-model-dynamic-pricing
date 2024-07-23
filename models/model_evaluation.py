import logging
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Initialize logger
logger = logging.getLogger(__name__)

def load_model(model_path):

    """
    Load the trained model from disk.
    Args:
        model_path (str): Path to the saved model.
    Returns:
        model: Loaded model.
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading the model: {e}")
        raise


def evaluate_model(model, data):
    """
    Evaluate the trained model on the test set.
    Args:
        model: Trained model.
        data (pd.DataFrame): Test data for evaluation.
    Returns:
        dict: Evaluation metrics.
    """
    try:
        logger.info("Starting model evaluation...")

        # Prepare data for evaluation
        y_true = data['Rating']
        y_pred = data.apply(lambda row: model.predict(row['User_ID'], row['Product_ID'], row['Purchase_Date']), axis=1)

        # Calculate evaluation metrics
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        mae = mean_absolute_error(y_true, y_pred)

        metrics = {
            'RMSE': rmse,
            'MAE': mae
        }

        logger.info("Model evaluation completed successfully.")
        return metrics
    except Exception as e:
        logger.error(f"Error during model evaluation: {e}")
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

    model_path = 'models/trained_model.pkl'
    loaded_model = load_model(model_path)

    # Evaluate model
    metrics = evaluate_model(loaded_model, preprocessed_data)
    print(metrics)