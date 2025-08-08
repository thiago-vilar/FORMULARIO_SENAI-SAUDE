# tests/test_services.py

import pytest
from backend.app.services.calculo_saude import calcular_imc, classificar_imc
from backend.app.services.campo_factory import CampoCalculadoFactory
from backend.app.controllers.resposta_controller import _processar_resposta

def test_calcular_imc():
    assert calcular_imc(80, 180) == 24.69
    assert calcular_imc(0, 180) == 0.0
    assert calcular_imc(80, 0) == 0.0
    assert calcular_imc(50, 150) == 22.22

def test_classificar_imc():
    assert classificar_imc(15.0) == "Magreza grave"
    assert classificar_imc(16.5) == "Magreza moderada"
    assert classificar_imc(17.5) == "Magreza leve"
    assert classificar_imc(22.0) == "Eutrofia (peso normal)"
    assert classificar_imc(27.0) == "Sobrepeso"
    assert classificar_imc(32.0) == "Obesidade Grau I"
    assert classificar_imc(38.0) == "Obesidade Grau II"
    assert classificar_imc(45.0) == "Obesidade Grau III"

def test_campo_calculado_factory_imc():
    assert CampoCalculadoFactory.criar_campo_calculado("imc", peso=80, altura=180) == 24.69

def test_campo_calculado_factory_classificacao():
    assert CampoCalculadoFactory.criar_campo_calculado("classificacao", imc=24.0) == "Eutrofia (peso normal)"

def test_campo_calculado_factory_erro():
    with pytest.raises(ValueError):
        CampoCalculadoFactory.criar_campo_calculado("imc", peso=0, altura=180)
    with pytest.raises(ValueError):
        CampoCalculadoFactory.criar_campo_calculado("inexistente", peso=80, altura=180)

def test_calcular_imc_invalid():
    assert calcular_imc(0, 0) == 0.0  # Não lança exception

def test_processar_resposta_invalid():
    with pytest.raises(ValueError):
        _processar_resposta({"peso": 0, "altura": 180})
    with pytest.raises(ValueError):
        _processar_resposta({"peso": 80, "altura": 0})
    with pytest.raises(ValueError):
        _processar_resposta({"peso": None, "altura": 180})
    with pytest.raises(ValueError):
        _processar_resposta({"peso": 80})
