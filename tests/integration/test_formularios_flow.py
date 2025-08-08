# tests/integration/test_formularios_flow.py

import pytest
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

# Payload base alinhado ao Caso de Uso (tipos válidos: text, number, date, select, boolean, calculated)
def make_form_payload(nome="Ficha de Admissão", descricao="Formulário usado no onboarding"):
    return {
        "nome": nome,
        "descricao": descricao,
        "campos": [
            {
                "id": "nome_completo",
                "label": "Nome completo",
                "tipo": "text",
                "obrigatorio": True,
                "capitalizar": True,
                "multilinha": False,
                "validacoes": [
                    {"tipo": "tamanho_minimo", "valor": 5},
                ],
            },
            {
                "id": "idade",
                "label": "Idade",
                "tipo": "number",
                "formato": "inteiro",
                "obrigatorio": True,
                "validacoes": [
                    {"tipo": "minimo", "valor": 18},
                    {"tipo": "maximo", "valor": 65},
                ],
            },
            {
                "id": "aceita_termos",
                "label": "Aceita os termos e condições?",
                "tipo": "boolean",
                "obrigatorio": True,
                "condicional": "idade >= 18",
            },
        ],
    }


@pytest.mark.integration
def test_criar_e_listar_formularios(client):
    # Cria
    payload = make_form_payload()
    r = client.post("/formularios", json=payload)
    assert r.status_code == HTTP_201_CREATED, r.text
    data = r.json()
    assert "id" in data
    form_id = data["id"]
    assert data.get("schema_version") == 1

    # Lista (GET /formularios)
    r = client.get("/formularios")
    assert r.status_code == HTTP_200_OK
    lst = r.json()
    assert "formularios" in lst
    assert any(f["id"] == form_id for f in lst["formularios"])


@pytest.mark.integration
def test_detalhar_formulario_por_id(client):
    # cria um
    r = client.post("/formularios", json=make_form_payload(nome="Onboarding RH"))
    assert r.status_code == HTTP_201_CREATED
    form_id = r.json()["id"]

    # busca por id
    r = client.get(f"/formularios/{form_id}")
    assert r.status_code == HTTP_200_OK, r.text
    data = r.json()
    assert data["id"] == form_id
    assert data["schema_version"] == 1
    assert isinstance(data.get("campos"), list) and len(data["campos"]) >= 1


@pytest.mark.integration
def test_soft_delete_formulario(client):
    # cria
    r = client.post("/formularios", json=make_form_payload())
    assert r.status_code == HTTP_201_CREATED
    form_id = r.json()["id"]

    # apaga (soft delete)
    r = client.delete(f"/formularios/{form_id}")
    assert r.status_code == HTTP_200_OK
    body = r.json()
    assert body.get("status") in {"soft_deleted", "inativo", "ok"}  # tolerante a mensagem

    # agora GET por id deve sinalizar inativo ou 404 (depende da sua regra)
    r = client.get(f"/formularios/{form_id}")
    # Conforme o Caso de Uso, GET pode retornar inativo com mensagem OU 404.
    # Vamos aceitar as duas abordagens:
    if r.status_code == HTTP_200_OK:
        assert r.json().get("is_ativo") is False
    else:
        assert r.status_code == HTTP_404_NOT_FOUND
