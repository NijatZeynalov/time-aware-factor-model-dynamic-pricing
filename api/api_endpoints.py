from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from price_engine.dynamic_pricing_calculation import calculate_price
from config.config_settings import get_config
from models.model_evaluation import load_model

# Initialize FastAPI app
app = FastAPI()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
CONFIG_PATH = 'config/development.yaml'
config = get_config(CONFIG_PATH)

model_path = 'models/trained_model.pkl'
model = load_model(model_path)

# Define request model
class PriceRequest(BaseModel):
    user_id: str
    product_id: str
    purchase_date: str
    base_price: float

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

@app.post("/api/calculate_price")
async def calculate_price_endpoint(request: PriceRequest):
    """
    API endpoint to calculate the dynamic price for a product.
    Expects JSON input with user_id, product_id, purchase_date, and base_price.
    """
    try:
        user_id = request.user_id
        product_id = request.product_id
        purchase_date = request.purchase_date
        base_price = request.base_price

        logger.info(f"API request to calculate price for User: {user_id}, Product: {product_id}, Date: {purchase_date}")

        final_price = calculate_price(model, user_id, product_id, purchase_date, base_price)

        response = {'final_price': final_price}
        return response
    except Exception as e:
        logger.error(f"Error in /api/calculate_price endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config['api']['port'])
