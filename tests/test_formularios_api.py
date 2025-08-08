# tests/test_formularios_api.py

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
FORMULARIO_ID = None  # Variável global para compartilhamento entre testes

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensagem"] == "API SENAI Saúde rodando!"

def test_post_formulario():
    global FORMULARIO_ID
    response = client.post("/formularios", json={
        "nome": "Teste CRUD",
        "descricao": "Formulário de teste CRUD",
        "usuario": "pytest_user",
        "campos": [
            {"tipo": "text", "label": "Nome", "obrigatorio": True},
            {"tipo": "float", "label": "Peso", "obrigatorio": True}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    FORMULARIO_ID = data["id"]
    assert data["nome"] == "Teste CRUD"

def test_post_formulario_invalid():
    response = client.post("/formularios", json={
        "descricao": "Sem nome e campos"
    })
    assert response.status_code == 422  # FastAPI retorna 422 para schema inválido

def test_get_formularios():
    response = client.get("/formularios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_formularios_usuario_not_found():
    response = client.get("/formularios/usuario/usuario_inexistente")
    assert response.status_code == 200
    assert response.json() == []

def test_get_formulario_by_id():
    global FORMULARIO_ID
    response = client.get(f"/formularios/{FORMULARIO_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == FORMULARIO_ID

def test_put_formulario():
    global FORMULARIO_ID
    response = client.put(f"/formularios/{FORMULARIO_ID}", json={
        "nome": "Teste CRUD Atualizado",
        "descricao": "Formulário atualizado via Pytest",
        "usuario": "pytest_user",
        "campos": [
            {"tipo": "text", "label": "Nome", "obrigatorio": True},
            {"tipo": "float", "label": "Peso", "obrigatorio": True},
            {"tipo": "float", "label": "Altura", "obrigatorio": True}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Teste CRUD Atualizado"
    assert len(data["campos"]) == 3

def test_get_formulario_by_id_after_put():
    global FORMULARIO_ID
    response = client.get(f"/formularios/{FORMULARIO_ID}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["campos"]) == 3

def test_delete_formulario():
    global FORMULARIO_ID
    response = client.delete(f"/formularios/{FORMULARIO_ID}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_get_formulario_deleted():
    global FORMULARIO_ID
    response = client.get(f"/formularios/{FORMULARIO_ID}")
    assert response.status_code == 404

def test_get_formulario_not_found():
    response = client.get("/formularios/naoexiste-uuid")
    assert response.status_code == 404

def test_put_formulario_not_found():
    response = client.put("/formularios/naoexiste-uuid", json={
        "nome": "Nada",
        "descricao": "Nada",
        "usuario": "none",
        "campos": []
    })
    assert response.status_code == 404  

def test_delete_formulario_not_found():
    response = client.delete("/formularios/naoexiste-uuid")
    assert response.status_code == 404  

def test_double_delete_formulario():
    global FORMULARIO_ID
    response = client.delete(f"/formularios/{FORMULARIO_ID}")
    assert response.status_code == 404  
