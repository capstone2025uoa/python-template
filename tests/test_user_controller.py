from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest

# Import the router from the user_controller
from src.adapters.rest.user_controller import router


# Create a dummy FastAPI app and include the router under the "/users" prefix
app = FastAPI()
app.include_router(router, prefix="/users")


# Dummy user class for testing
class DummyUser:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


# Dummy async service functions
async def dummy_get_all_users():
    return [DummyUser(1, "Alice", "alice@example.com"), DummyUser(2, "Bob", "bob@example.com")]

async def dummy_get_user_by_id(user_id: int):
    if user_id == 1:
        return DummyUser(1, "Alice", "alice@example.com")
    return None

async def dummy_create_user(name: str, email: str):
    return DummyUser(3, name, email)

async def dummy_update_user(user_id: int, name: str, email: str):
    if user_id == 1:
        return DummyUser(1, name, email)
    return None


# Fixture to monkeypatch the service functions used in the controller
@pytest.fixture(autouse=True)
def patch_service_functions(monkeypatch):
    # Patch the functions in the user_controller module
    monkeypatch.setattr("src.adapters.rest.user_controller.get_all_users", dummy_get_all_users)
    monkeypatch.setattr("src.adapters.rest.user_controller.get_user_by_id", dummy_get_user_by_id)
    monkeypatch.setattr("src.adapters.rest.user_controller.service_create_user", dummy_create_user)
    monkeypatch.setattr("src.adapters.rest.user_controller.service_update_user", dummy_update_user)


client = TestClient(app)


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    # Should return two users
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Alice"
    assert data[0]["email"] == "alice@example.com"


def test_get_user_found():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


def test_create_user():
    payload = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"


def test_update_user_found():
    payload = {"name": "Alice Updated", "email": "alice_new@example.com"}
    response = client.put("/users/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Updated"
    assert data["email"] == "alice_new@example.com"


def test_update_user_not_found():
    payload = {"name": "Nonexistent", "email": "none@example.com"}
    response = client.put("/users/999", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found" 