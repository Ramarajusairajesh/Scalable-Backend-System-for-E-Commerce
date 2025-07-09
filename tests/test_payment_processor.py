import pytest
import asyncio
import src.payment_processor.main as ppm
from src.payment_processor.main import process_transaction

pytestmark = pytest.mark.asyncio

async def test_process_transaction_success(monkeypatch):
    monkeypatch.setattr(ppm.asyncio, "sleep", lambda x: None)
    monkeypatch.setattr(ppm.random, "random", lambda: 0.5)
    transaction_data = {"transaction_id": "abc", "amount": 100}
    result = await process_transaction(transaction_data)
    assert result is True

async def test_process_transaction_failure(monkeypatch):
    monkeypatch.setattr(ppm.asyncio, "sleep", lambda x: None)
    monkeypatch.setattr(ppm.random, "random", lambda: 0.95)
    transaction_data = {"transaction_id": "abc", "amount": 100}
    result = await process_transaction(transaction_data)
    assert result is False 