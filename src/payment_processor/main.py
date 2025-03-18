import json
import os
import asyncio
from dotenv import load_dotenv
from aiokafka import AIOKafkaConsumer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import logging

from ..models import Transaction, TransactionStatus

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TRANSACTIONS_TOPIC = "payment_transactions"

async def process_transaction(transaction_data: dict) -> bool:
    """
    Simulate payment processing with artificial delay and random success/failure
    """
    transaction_id = transaction_data["transaction_id"]
    amount = transaction_data["amount"]
    
    logger.info(f"Processing transaction {transaction_id} for amount {amount}")
    
    # Simulate processing delay
    await asyncio.sleep(2)
    
    # Simulate success rate (90% success, 10% failure)
    import random
    success = random.random() < 0.9
    
    return success

async def update_transaction_status(
    session: AsyncSession,
    transaction_id: str,
    status: TransactionStatus,
    error_message: str = None
):
    """
    Update transaction status in database
    """
    async with session.begin():
        result = await session.execute(
            select(Transaction).where(Transaction.transaction_id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        
        if transaction:
            transaction.status = status
            if error_message:
                transaction.error_message = error_message
            await session.commit()

async def process_messages():
    consumer = AIOKafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="payment_processor_group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    await consumer.start()
    
    try:
        async for msg in consumer:
            transaction_data = msg.value
            transaction_id = transaction_data["transaction_id"]
            
            logger.info(f"Received transaction: {transaction_id}")
            
            async with async_session() as session:
                # Update status to processing
                await update_transaction_status(
                    session,
                    transaction_id,
                    TransactionStatus.PROCESSING
                )
                
                # Process the transaction
                try:
                    success = await process_transaction(transaction_data)
                    
                    if success:
                        await update_transaction_status(
                            session,
                            transaction_id,
                            TransactionStatus.COMPLETED
                        )
                        logger.info(f"Transaction {transaction_id} completed successfully")
                    else:
                        await update_transaction_status(
                            session,
                            transaction_id,
                            TransactionStatus.FAILED,
                            "Transaction processing failed"
                        )
                        logger.error(f"Transaction {transaction_id} failed")
                
                except Exception as e:
                    logger.error(f"Error processing transaction {transaction_id}: {str(e)}")
                    await update_transaction_status(
                        session,
                        transaction_id,
                        TransactionStatus.FAILED,
                        str(e)
                    )
    
    finally:
        await consumer.stop()

async def main():
    try:
        await process_messages()
    except Exception as e:
        logger.error(f"Main process error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 