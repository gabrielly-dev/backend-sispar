import pytest
from src.app import create_app
from src.model.colaborador_model import Colaborador
from src.model.reembolso_model import Reembolso
from src.model import db
import json

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_cadastrar_colaborador(client):
    data = {
        "nome": "Reembolso Test",
        "email": "reembolso@example.com",
        "senha": "senha123",
        "cargo": "Dev",
        "salario": 5000.00,
    }
    response = client.post("/colaborador/cadastrar", json=data)
    assert response.status_code == 201
    assert b'Dado cadastrado com sucesso' in response.data
    with client.application.app_context():
        colaborador = db.session.execute(
            db.select(Colaborador).where(Colaborador.email == data["email"])
        ).scalar()
        assert colaborador is not None
        global colaborador_id
        colaborador_id = colaborador.id

def test_login_colaborador(client):
    login_data = {
        "email": "reembolso@example.com",
        "senha": "senha123",
    }
    response = client.post("/colaborador/login", json=login_data)
    assert response.status_code == 200
    assert b'Login realizado com sucesso' in response.data

def test_listar_todos_colaboradores(client):
    response = client.get("/colaborador/todos-colaboradores")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert 'colaboradores' in response.json

def test_solicitar_reembolso(client):
    global colaborador_id
    login_data = {
        "email": "reembolso@example.com",
        "senha": "senha123",
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    reembolso_data = {
        "colaborador": "Reembolso Test",
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
        "id_colaborador": colaborador_id,
        "status": "Em analise",
    }
    response = client.post("/reembolso/solicitar", json=reembolso_data, headers=headers)
    assert response.status_code in [200, 201]

def test_listar_todos_reembolsos(client):
    login_data = {
        "email": "reembolso@example.com",
        "senha": "senha123",
    }
    login_response = client.post("/colaborador/login", json=login_data)
    token = login_response.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/reembolso/todos-reembolsos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
