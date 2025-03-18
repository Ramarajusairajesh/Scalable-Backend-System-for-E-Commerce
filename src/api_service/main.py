import uuid
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from aiokafka import AIOKafkaProducer
import json
import os
from dotenv import load_dotenv

from ..models import TransactionCreate, TransactionResponse, Transaction, TransactionStatus

load_dotenv()

app = FastAPI(title="Payment Transaction API")

# Database configuration
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TRANSACTIONS_TOPIC = "payment_transactions"

# Kafka producer
producer = None

async def get_db():
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        await producer.stop()

@app.post("/api/v1/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    # Create transaction record
    transaction_id = str(uuid.uuid4())
    db_transaction = Transaction(
        transaction_id=transaction_id,
        sender=transaction.sender,
        receiver=transaction.receiver,
        amount=transaction.amount,
        currency=transaction.currency,
        status=TransactionStatus.PENDING
    )
    
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)

    # Send to Kafka
    message = {
        "transaction_id": transaction_id,
        "sender": transaction.sender,
        "receiver": transaction.receiver,
        "amount": transaction.amount,
        "currency": transaction.currency
    }
    
    await producer.send_and_wait(
        TRANSACTIONS_TOPIC,
        json.dumps(message).encode()
    )

    return db_transaction

@app.get("/api/v1/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.get(Transaction, transaction_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

@app.get("/api/v1/transactions", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction)
        .offset(skip)
        .limit(limit)
    )
    transactions = result.scalars().all()
    return transactions 