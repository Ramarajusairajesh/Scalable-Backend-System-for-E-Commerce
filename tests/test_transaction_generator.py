import pytest
from src.transaction_generator.main import generate_transaction, USERS, CURRENCIES, MIN_AMOUNT, MAX_AMOUNT
import asyncio

pytestmark = pytest.mark.asyncio

async def test_generate_transaction():
    txn = await generate_transaction()
    assert txn["sender"] in USERS
    assert txn["receiver"] in USERS and txn["receiver"] != txn["sender"]
    assert MIN_AMOUNT <= txn["amount"] <= MAX_AMOUNT
    assert txn["currency"] in CURRENCIES 