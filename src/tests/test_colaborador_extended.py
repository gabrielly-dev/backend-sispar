import pytest
from src.app import create_app
from config import TestConfig
from src.model import db
import json

@pytest.fixture
def app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_update_colaborador(client):
    # Register a colaborador first
    data = {
        "nome": "Update Test",
        "email": "update@example.com",
        "senha": "senha123",
        "cargo": "Dev",
        "salario": 3000.00,
    }
    response = client.post("/colaborador/cadastrar", json=data)
    assert response.status_code == 201

    # Login to get token
    login_data = {
        "email": "update@example.com",
        "senha": "senha123"
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Get colaborador id
    response = client.get("/colaborador/todos-colaboradores")
    colaboradores = response.json.get("colaboradores")
    colaborador_id = next((c["id"] for c in colaboradores if c["email"] == "update@example.com"), None)
    assert colaborador_id is not None

    # Update colaborador
    update_data = {
        "nome": "Updated Name",
        "cargo": "Senior Dev",
        "salario": 4000.00
    }
    update_response = client.put(f"/colaborador/atualizar/{colaborador_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert b'atualizados com sucesso' in update_response.data

def test_delete_colaborador(client):
    # Register a colaborador first
    data = {
        "nome": "Delete Test",
        "email": "delete@example.com",
        "senha": "senha123",
        "cargo": "Dev",
        "salario": 3000.00,
    }
    response = client.post("/colaborador/cadastrar", json=data)
    assert response.status_code == 201

    # Login to get token
    login_data = {
        "email": "delete@example.com",
        "senha": "senha123"
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Get colaborador id
    response = client.get("/colaborador/todos-colaboradores")
    colaboradores = response.json.get("colaboradores")
    colaborador_id = next((c["id"] for c in colaboradores if c["email"] == "delete@example.com"), None)
    assert colaborador_id is not None

    # Delete colaborador
    delete_response = client.delete(f"/colaborador/deletar/{colaborador_id}", headers=headers)
    assert delete_response.status_code == 200
    assert b'deletado com sucesso' in delete_response.data
