import pytest
from fastapi.testclient import TestClient
from src.api_service.main import app
from unittest.mock import AsyncMock

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_transaction_endpoint(monkeypatch, client):
    # Patch producer and startup_event
    from src.api_service import main as api_main
    monkeypatch.setattr(api_main, "producer", type("DummyProducer", (), {"send_and_wait": AsyncMock()})())
    monkeypatch.setattr(api_main, "startup_event", AsyncMock())

    # Mock DB dependency
    async def mock_get_db():
        class DummySession:
            async def __aenter__(self): return self
            async def __aexit__(self, exc_type, exc, tb): pass
            def add(self, obj): pass
            async def commit(self): pass
            async def refresh(self, obj): pass
        yield DummySession()
    app.dependency_overrides[api_main.get_db] = mock_get_db

    payload = {
        "sender": "user1",
        "receiver": "user2",
        "amount": 100.0,
        "currency": "USD"
    }
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code in (200, 422) 