import pytest
from sqlalchemy import select, delete
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from tests.conftest import db_session


@pytest.fixture()
def client():

    client = TestClient(app)
    yield client

def test_register_user(client, db_session):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }

    response = client.post("/auth/register", json=data)
    print(response.json())


    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == data["email"]


    with db_session.begin():
        user_in_db = db_session.execute(
            select(User).filter(User.email == data["email"])
        ).scalars().first()
        assert user_in_db is not None
        assert user_in_db.email == data["email"]

    with db_session.begin():
        db_session.execute(delete(User).filter(User.email == data["email"]))

def test_register_user_existing_email(client, db_session):

    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response1 = client.post("/auth/register", json=data)
    print(response1.json())

    response = client.post("/auth/register", json=data)
    print(response.json())

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    with db_session.begin():
        db_session.execute(delete(User).filter(User.email == data["email"]))

def test_login_user(client, db_session):
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    response1 = client.post("/auth/register", json=data)
    print(response1.json())


    response = client.post("/auth/login", data=data)
    print(response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()

    with db_session.begin():
        db_session.execute(delete(User).filter(User.email == data["email"]))

def test_login_user_invalid_credentials(client, db_session):
    data = {
        "email": "test@example.com",
        "password": "incorrectpassword"
    }

    response = client.post("/auth/login", data=data)
    print(response.json())

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    with db_session.begin():
        db_session.execute(delete(User).filter(User.email == data["email"]))
