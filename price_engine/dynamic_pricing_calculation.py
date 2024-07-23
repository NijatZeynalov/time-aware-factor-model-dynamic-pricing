import logging
import pickle
from config.config_settings import get_config

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

def apply_pricing_rules(base_price, predicted_rating):
    """
    Apply business rules to adjust the base price based on the predicted rating.
    Args:
        base_price (float): Base price of the product.
        predicted_rating (float): Predicted rating from the model.
    Returns:
        float: Adjusted price after applying pricing rules.
    """
    try:
        logger.info(f"Applying pricing rules for base price: {base_price}, predicted rating: {predicted_rating}")

        # Example pricing rule: Adjust price based on predicted rating
        if predicted_rating >= 4.5:
            final_price = base_price * 1.20  # Increase by 20% for high predicted ratings
        elif predicted_rating >= 3.0:
            final_price = base_price * 1.10  # Increase by 10% for moderate predicted ratings
        else:
            final_price = base_price * 0.90  # Decrease by 10% for low predicted ratings

        logger.info(f"Final price after applying rules: {final_price}")
        return final_price
    except Exception as e:
        logger.error(f"Error applying pricing rules: {e}")
        raise

def calculate_price(model, user_id, product_id, purchase_date, base_price):
    """
    Calculate the dynamic price for a given product based on model predictions and pricing rules.
    Args:
        model: Trained Time-Aware Factor Model.
        user_id (str): User ID.
        product_id (str): Product ID.
        purchase_date (str): Date of purchase.
        base_price (float): Base price of the product.
    Returns:
        float: Final dynamic price for the product.
    """
    try:
        logger.info(f"Calculating price for User: {user_id}, Product: {product_id}, Date: {purchase_date}")

        # Predict the rating
        predicted_rating = model.predict(user_id, product_id, purchase_date)

        # Apply pricing rules
        final_price = apply_pricing_rules(base_price, predicted_rating)

        logger.info(f"Calculated price for User: {user_id}, Product: {product_id} is {final_price}")
        return final_price
    except Exception as e:
        logger.error(f"Error calculating price for User: {user_id}, Product: {product_id}: {e}")
        raise

if __name__ == '__main__':
    # Load configuration
    CONFIG_PATH = 'config/development.yaml'
    config = get_config(CONFIG_PATH)

    # Load trained model
    model_path = 'models/trained_model.pkl'
    model = load_model(model_path)

    # Example
    user_id = '0217'
    product_id = 'P0066'
    purchase_date = '2023-01-15'
    base_price = 51.38

    # Calculate price
    final_price = calculate_price(model, user_id, product_id, purchase_date, base_price)
    print(f"Final price for the product: {final_price}")
