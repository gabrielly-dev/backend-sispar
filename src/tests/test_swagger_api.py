import pytest
import requests

BASE_URL = "http://localhost:5000"  # Adjust if your app runs on a different port

def test_swagger_ui_loads():
    url = f"{BASE_URL}/apidocs/"
    response = requests.get(url)
    assert response.status_code == 200
    assert "Swagger" in response.text or "swagger-ui" in response.text.lower()

def test_get_todos_colaboradores():
    url = f"{BASE_URL}/colaborador/todos-colaboradores"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "colaboradores" in data

def test_post_cadastrar_colaborador():
    url = f"{BASE_URL}/colaborador/cadastrar"
    payload = {
        "nome": "Test User",
        "email": "testuser@example.com",
        "senha": "password123",
        "cargo": "Tester",
        "salario": 1000
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "mensagem" in data

# Additional tests for login, update, delete, and reembolso endpoints would require JWT token handling
# For brevity, only basic tests are included here
