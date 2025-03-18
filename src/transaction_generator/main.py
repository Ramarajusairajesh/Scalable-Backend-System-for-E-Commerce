import asyncio
import random
import json
import os
from dotenv import load_dotenv
import httpx
import logging
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = "http://api-service:8000/api/v1"
MIN_AMOUNT = 10.0
MAX_AMOUNT = 1000.0
CURRENCIES = ["USD", "EUR", "GBP", "JPY"]
TRANSACTION_INTERVAL = 1.0  # seconds between transactions

# Sample user IDs for demonstration
USERS = [f"user_{i}" for i in range(1, 11)]

async def generate_transaction():
    """
    Generate a random transaction
    """
    sender = random.choice(USERS)
    receiver = random.choice([u for u in USERS if u != sender])
    amount = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT), 2)
    currency = random.choice(CURRENCIES)
    
    return {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "currency": currency
    }

async def send_transaction(transaction: dict):
    """
    Send transaction to API service
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/transactions",
                json=transaction
            )
            response.raise_for_status()
            logger.info(f"Transaction sent: {transaction}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending transaction: {str(e)}")
            return None

async def generate_transactions():
    """
    Continuously generate and send transactions
    """
    while True:
        try:
            transaction = await generate_transaction()
            result = await send_transaction(transaction)
            
            if result:
                logger.info(f"Transaction created with ID: {result['transaction_id']}")
            
            # Wait before generating next transaction
            await asyncio.sleep(TRANSACTION_INTERVAL)
            
        except Exception as e:
            logger.error(f"Error in transaction generation: {str(e)}")
            await asyncio.sleep(5)  # Wait longer on error

async def main():
    logger.info("Starting transaction generator...")
    await generate_transactions()

if __name__ == "__main__":
    asyncio.run(main()) 