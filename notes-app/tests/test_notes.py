import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base
from app.auth import get_current_user
from unittest.mock import MagicMock


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)



@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture(scope="module")
def client():
    # Mock de get_current_user
    def mock_get_current_user():
        return MagicMock(id=1)

    app.dependency_overrides[get_current_user] = mock_get_current_user
    client = TestClient(app)
    return client


def test_create_note(client, db):

    new_note_data = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }

    response = client.post("/notes", json=new_note_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"
    assert response.json()["content"] == "This is a test note"
    assert "id" in response.json()
    assert "created_at" in response.json()


def test_get_notes(client, db):

    db_note = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }
    db.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
               (db_note["title"], db_note["content"], db_note["user_id"]))
    db.commit()

    response = client.get("/notes")

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test Note"


def test_get_notes(client, db):

    db_note = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }
    db.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
               (db_note["title"], db_note["content"], db_note["user_id"]))
    db.commit()


    response = client.get("/notes")


    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test Note"


def test_get_note_by_id(client, db):

    db_note = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }
    db.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
               (db_note["title"], db_note["content"], db_note["user_id"]))
    db.commit()

    note_id = db.execute("SELECT id FROM notes WHERE title = ?", (db_note["title"],)).fetchone()[0]

    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Test Note"


def test_update_note(client, db):

    db_note = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }
    db.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
               (db_note["title"], db_note["content"], db_note["user_id"]))
    db.commit()


    note_id = db.execute("SELECT id FROM notes WHERE title = ?", (db_note["title"],)).fetchone()[0]


    updated_note_data = {
        "title": "Updated Test Note",
        "content": "This is an updated test note",
        "user_id": 1
    }


    response = client.put(f"/notes/{note_id}", json=updated_note_data)


    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Note"
    assert response.json()["content"] == "This is an updated test note"


def test_delete_note(client, db):

    db_note = {
        "title": "Test Note",
        "content": "This is a test note",
        "user_id": 1
    }
    db.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
               (db_note["title"], db_note["content"], db_note["user_id"]))
    db.commit()

    note_id = db.execute("SELECT id FROM notes WHERE title = ?", (db_note["title"],)).fetchone()[0]

    response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
