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

def test_update_reembolso(client):
    # Register and login colaborador first
    data = {
        "nome": "Reembolso Update",
        "email": "reembolso_update@example.com",
        "senha": "senha123",
        "cargo": "Dev",
        "salario": 3000.00,
    }
    client.post("/colaborador/cadastrar", json=data)
    login_data = {
        "email": "reembolso_update@example.com",
        "senha": "senha123"
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit reimbursement
    reembolso_data = {
        "colaborador": "Reembolso Update",
        "empresa": "Empresa X",
        "num_prestacao": 1,
        "descricao": "Despesa de viagem",
        "data": "2023-01-01",
        "tipo_reembolso": "Viagem",
        "centro_custo": "CC123",
        "ordem_interna": "OI456",
        "divisao": "Div1",
        "pep": "PEP789",
        "moeda": "BRL",
        "distancia_km": "100",
        "valor_km": "1.5",
        "valor_faturado": 150.00,
        "despesa": 150.00,
        "id_colaborador": 1,
        "status": "Em analise"
    }
    response = client.post("/reembolso/solicitar", json=reembolso_data, headers=headers)
    assert response.status_code == 201

    # Get reimbursement id
    response = client.get("/reembolso/todos-reembolsos", headers=headers)
    reembolsos = response.json
    reembolso_id = next((r["id"] for r in reembolsos if r["colaborador"] == "Reembolso Update"), None)
    assert reembolso_id is not None

    # Update reimbursement
    update_data = {
        "status": "Aprovado",
        "descricao": "Despesa de viagem atualizada"
    }
    update_response = client.put(f"/reembolso/atualizar/{reembolso_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert b'atualizado com sucesso' in update_response.data

def test_delete_reembolso(client):
    # Register and login colaborador first
    data = {
        "nome": "Reembolso Delete",
        "email": "reembolso_delete@example.com",
        "senha": "senha123",
        "cargo": "Dev",
        "salario": 3000.00,
    }
    client.post("/colaborador/cadastrar", json=data)
    login_data = {
        "email": "reembolso_delete@example.com",
        "senha": "senha123"
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit reimbursement
    reembolso_data = {
        "colaborador": "Reembolso Delete",
        "empresa": "Empresa X",
        "num_prestacao": 1,
        "descricao": "Despesa de viagem",
        "data": "2023-01-01",
        "tipo_reembolso": "Viagem",
        "centro_custo": "CC123",
        "ordem_interna": "OI456",
        "divisao": "Div1",
        "pep": "PEP789",
        "moeda": "BRL",
        "distancia_km": "100",
        "valor_km": "1.5",
        "valor_faturado": 150.00,
        "despesa": 150.00,
        "id_colaborador": 1,
        "status": "Em analise"
    }
    response = client.post("/reembolso/solicitar", json=reembolso_data, headers=headers)
    assert response.status_code == 201

    # Get reimbursement id
    response = client.get("/reembolso/todos-reembolsos", headers=headers)
    reembolsos = response.json
    reembolso_id = next((r["id"] for r in reembolsos if r["colaborador"] == "Reembolso Delete"), None)
    assert reembolso_id is not None

    # Delete reimbursement
    delete_response = client.delete(f"/reembolso/deletar/{reembolso_id}", headers=headers)
    assert delete_response.status_code == 200
    assert b'deletado com sucesso' in delete_response.data
