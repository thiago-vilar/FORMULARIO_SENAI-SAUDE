# tests/integration/test_calcular_imc.py

import math
import pytest
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.integration
def test_calcular_imc_sucesso(client):
    """
    Verifica o endpoint /calcular-imc com dados válidos.
    Espera IMC ~ 22.857 (70kg / 1.75^2)
    """
    payload = {"peso": 70.0, "altura": 1.75}
    r = client.post("/calcular-imc", json=payload)
    assert r.status_code == HTTP_200_OK, r.text
    data = r.json()
    assert "imc" in data
    assert math.isfinite(data["imc"])
    assert abs(data["imc"] - 22.8571428571) < 1e-3

@pytest.mark.integration
def test_calcular_imc_payload_invalido(client):
    """
    Verifica tratamento de erro: altura inválida (zero ou negativa).
    """
    payload = {"peso": 70.0, "altura": 0}
    r = client.post("/calcular-imc", json=payload)
    # pode ser 422 (validação) ou 400 dependendo da sua regra;
    # cobrimos 422 por ser o mais comum com Pydantic
    assert r.status_code in (HTTP_422_UNPROCESSABLE_ENTITY, 400)
