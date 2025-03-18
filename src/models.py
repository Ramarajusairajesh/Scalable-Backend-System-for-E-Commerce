from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(SQLAEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_message = Column(String, nullable=True)

class TransactionCreate(BaseModel):
    sender: str = Field(..., example="user123")
    receiver: str = Field(..., example="user456")
    amount: float = Field(..., gt=0, example=100.00)
    currency: str = Field(..., example="USD")

class TransactionResponse(BaseModel):
    transaction_id: str
    sender: str
    receiver: str
    amount: float
    currency: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True 