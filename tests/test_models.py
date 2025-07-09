import pytest
from src.models import TransactionCreate, TransactionResponse, TransactionStatus
from datetime import datetime

def test_transaction_create_valid():
    data = {"sender": "user1", "receiver": "user2", "amount": 50.0, "currency": "USD"}
    model = TransactionCreate(**data)
    assert model.sender == "user1"
    assert model.amount == 50.0

def test_transaction_create_invalid_amount():
    data = {"sender": "user1", "receiver": "user2", "amount": -10.0, "currency": "USD"}
    with pytest.raises(Exception):
        TransactionCreate(**data)

def test_transaction_response():
    now = datetime.utcnow()
    data = {
        "transaction_id": "abc",
        "sender": "user1",
        "receiver": "user2",
        "amount": 100.0,
        "currency": "USD",
        "status": TransactionStatus.PENDING,
        "created_at": now,
        "updated_at": now,
        "error_message": None
    }
    model = TransactionResponse(**data)
    assert model.status == TransactionStatus.PENDING 