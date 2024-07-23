
import numpy as np
import pandas as pd
import logging

# Initialize logger
logger = logging.getLogger(__name__)

class TimeAwareFactorModel:
    def __init__(self, n_factors, lr, reg, n_epochs):
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.n_epochs = n_epochs
        self.global_mean = None
        self.user_factors = None
        self.item_factors = None
        self.user_bias = None
        self.item_bias = None
        self.user_time_bias = None
        self.item_time_bias = None

    def fit(self, data):
        """
        Train the timeSVD++ model.
        Args:
            data (pd.DataFrame): Training data containing User_ID, Product_ID, Rating, and Purchase_Date.
        """
        logger.info("Training timeSVD++ model...")
        try:
            # Initialize parameters
            self.global_mean = data['Rating'].mean()
            self.user_factors = {}
            self.item_factors = {}
            self.user_bias = {}
            self.item_bias = {}
            self.user_time_bias = {}
            self.item_time_bias = {}

            # Preprocessing
            user_ids = data['User_ID'].unique()
            item_ids = data['Product_ID'].unique()

            for user in user_ids:
                self.user_factors[user] = np.random.normal(scale=1./self.n_factors, size=self.n_factors)
                self.user_bias[user] = 0
                self.user_time_bias[user] = {}

            for item in item_ids:
                self.item_factors[item] = np.random.normal(scale=1./self.n_factors, size=self.n_factors)
                self.item_bias[item] = 0
                self.item_time_bias[item] = {}

            # Training
            for epoch in range(self.n_epochs):
                for idx, row in data.iterrows():
                    user, item, rating, date = row['User_ID'], row['Product_ID'], row['Rating'], row['Purchase_Date']

                    if item not in self.item_factors:
                        self.item_factors[item] = np.random.normal(scale=1./self.n_factors, size=self.n_factors)
                        self.item_bias[item] = 0
                        self.item_time_bias[item] = {}

                    if date not in self.user_time_bias[user]:
                        self.user_time_bias[user][date] = 0

                    if date not in self.item_time_bias[item]:
                        self.item_time_bias[item][date] = 0

                    pred = self.predict(user, item, date)
                    err = rating - pred

                    # Update biases
                    self.user_bias[user] += self.lr * (err - self.reg * self.user_bias[user])
                    self.item_bias[item] += self.lr * (err - self.reg * self.item_bias[item])
                    self.user_time_bias[user][date] += self.lr * (err - self.reg * self.user_time_bias[user][date])
                    self.item_time_bias[item][date] += self.lr * (err - self.reg * self.item_time_bias[item][date])

                    # Update factors
                    user_factors = self.user_factors[user]
                    item_factors = self.item_factors[item]
                    self.user_factors[user] += self.lr * (err * item_factors - self.reg * user_factors)
                    self.item_factors[item] += self.lr * (err * user_factors - self.reg * item_factors)

                logger.info(f"Epoch {epoch + 1}/{self.n_epochs} completed.")
        except Exception as e:
            logger.error(f"Error during training: {e}")
            raise

    def predict(self, user, item, date):
        """
        Predict the rating for a given user, item, and date.
        Args:
            user (str): User ID.
            item (str): Product ID.
            date (str): Purchase date.
        Returns:
            float: Predicted rating.
        """
        pred = self.global_mean + self.user_bias.get(user, 0) + self.item_bias.get(item, 0)
        pred += self.user_time_bias.get(user, {}).get(date, 0)
        pred += self.item_time_bias.get(item, {}).get(date, 0)
        pred += np.dot(self.user_factors.get(user, np.zeros(self.n_factors)),
                       self.item_factors.get(item, np.zeros(self.n_factors)))
        return pred
