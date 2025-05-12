import pytest
from src.app import create_app
from config import TestConfig
from src.model import db

@pytest.fixture
def app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_access_without_token(client):
    # Access protected endpoint without token
    response = client.get("/reembolso/todos-reembolsos")
    assert response.status_code == 401

def test_access_with_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/reembolso/todos-reembolsos", headers=headers)
    assert response.status_code in [422, 401]

def test_register_colaborador_missing_fields(client):
    data = {
        "nome": "Test User",
        # missing email, senha, cargo, salario
    }
    response = client.post("/colaborador/cadastrar", json=data)
    assert response.status_code in [400, 422]

def test_reembolso_missing_required_fields(client):
    # First register and login to get token
    register_data = {
        "nome": "Test User",
        "email": "testuser@example.com",
        "senha": "testpass",
        "cargo": "Dev",
        "salario": 1000.0,
    }
    client.post("/colaborador/cadastrar", json=register_data)
    login_data = {
        "email": "testuser@example.com",
        "senha": "testpass",
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Missing required fields in reimbursement
    reembolso_data = {
        "colaborador": "Test User",
        # missing empresa, num_prestacao, data, tipo_reembolso, centro_custo, moeda, valor_faturado
    }
    response = client.post("/reembolso/solicitar", json=reembolso_data, headers=headers)
    assert response.status_code in [400, 422]

def test_swagger_docs_accessible(client):
    response = client.get("/apidocs/")
    assert response.status_code == 200
    assert b"Swagger" in response.data or b"swagger" in response.data
