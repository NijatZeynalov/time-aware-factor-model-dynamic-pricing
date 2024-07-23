# System Architecture Design

## Overview
This document provides a detailed description of the system architecture for the dynamic pricing strategy project. It includes components, interactions, and data flow within the system.

## Components
1. **API Layer**: Handles external requests and responses.
2. **Data Layer**: Manages data loading, preprocessing, and storage.
3. **Model Layer**: Contains the Time-Aware Factor Model (timeSVD++) and related scripts.
4. **Pricing Engine**: Applies business rules to calculate dynamic prices.
5. **Configuration**: Manages environment-specific settings.

## Architecture Diagram
Refer to the `data_flow_diagram.png` for a visual representation of the architecture.



# Usage Guide

## Introduction
This guide provides instructions on how to set up, run, and use the dynamic pricing system.

## Setup
1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the environment**:
    Ensure the configuration files are set up in the `config/` directory.

## Running the Application
1. **Train the Model**:
    ```bash
    python models/model_training.py
    ```

2. **Start the API Server**:
    ```bash
    python api/api_endpoints.py
    ```

## Using the API
Refer to the `api_docs/api_overview.md` for details on the API endpoints and their usage.


# API Overview

## Introduction
This document provides an overview of the API endpoints available in the dynamic pricing system. Each endpoint's purpose, request format, and response format are described in detail.

## Endpoints

### Calculate Price
- **Endpoint**: `/api/calculate_price`
- **Method**: POST
- **Description**: Calculates the dynamic price for a product based on user and product information.

#### Request
```json
{
    "user_id": "1001",
    "product_id": "P001",
    "purchase_date": "2023-06-15",
    "base_price": 29.99
}
```

#### Response
```json{
    "final_price": 35.99
}
```