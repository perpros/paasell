from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from .database import override_get_db, engine
from app.database import Base
import pytest

# Apply the override for the get_db dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_register_user():
    response = client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword", "role": "supplier"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert data["role"] == "supplier"
