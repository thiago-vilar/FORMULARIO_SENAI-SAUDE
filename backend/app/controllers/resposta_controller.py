from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# IMC por Factory
from backend.app.services.campo_factory import CampoCalculadoFactory

# Respostas de formulário
from backend.app.db.session import DatabaseSessionFactory
from backend.app.schemas.resposta_schema import (
    RespostaCreateSchema,
    RespostaSchema,
    RespostaListSchema,
)
from backend.app.services.resposta_service import RespostaService

router = APIRouter()


# ====== MODELOS (IMC) =========================================================
class DadosIMC(BaseModel):
    # Aceita cm ou m: se altura <= 3, consideramos metros; caso contrário, cm.
    peso: float = Field(..., gt=0, json_schema_extra={"example": 80.0}, description="Peso em kg")
    altura: float = Field(..., gt=0, json_schema_extra={"example": 180.0}, description="Altura em cm (ou metros se <= 3.0)")


class RespostaIMC(BaseModel):
    peso: float
    altura: float  # normalizada para metros na resposta
    imc: float
    classificacao: str


# ====== HELPERS ===============================================================
def _normalizar_altura_para_cm(altura: float) -> float:
    """
    Se altura <= 3, assume metros e converte para cm.
    Se altura > 3, assume cm e mantém.
    """
    return altura * 100.0 if altura <= 3 else altura


def _processar_resposta_imc(dados_resposta: Dict[str, Any]) -> Dict[str, Any]:
    peso = dados_resposta.get("peso")
    altura = dados_resposta.get("altura")

    # valida cedo para evitar TypeError
    if peso is None or altura is None:
        raise ValueError("Peso e altura são obrigatórios.")
    if peso <= 0 or altura <= 0:
        raise ValueError("Peso e altura devem ser valores positivos.")

    # Factory espera altura em cm
    altura_cm = _normalizar_altura_para_cm(float(altura))
    imc = CampoCalculadoFactory.criar_campo_calculado("imc", peso=float(peso), altura=float(altura_cm))
    classificacao = CampoCalculadoFactory.criar_campo_calculado("classificacao", imc=float(imc))

    # Resposta com altura em metros
    return {
        "peso": float(peso),
        "altura": float(altura_cm / 100.0),
        "imc": float(imc),
        "classificacao": str(classificacao),
    }


# ---- Compat com testes antigos (mantém import esperado) ----------------------
def _processar_resposta(dados_resposta: Dict[str, Any]) -> Dict[str, Any]:
    return _processar_resposta_imc(dados_resposta)


# ====== ENDPOINTS (IMC) =======================================================
@router.post(
    "/calcular-imc",
    response_model=RespostaIMC,
    summary="Calcular IMC",
    description="Recebe peso e altura (em cm ou m) e retorna IMC e classificação de risco.",
)
def calcular_imc_endpoint(dados: DadosIMC):
    """
    Calcula o IMC e a classificação de risco a partir do peso e altura informados.
    """
    try:
        # Pydantic v2
        result = _processar_resposta_imc(dados.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ====== DEPENDÊNCIAS (DB) ====================================================
def get_db():
    db = DatabaseSessionFactory()()
    try:
        yield db
    finally:
        db.close()


# ====== ENDPOINTS (RESPOSTAS DE FORMULÁRIOS) =================================
@router.post(
    "/formularios/{formulario_id}/respostas",
    response_model=RespostaSchema,
    summary="Enviar respostas de um formulário",
)
def enviar_respostas(
    formulario_id: str,
    body: RespostaCreateSchema,
    db: Session = Depends(get_db),
):
    try:
        r = RespostaService.criar_resposta(db, formulario_id, body.respostas)
        return r
    except ValueError as e:
        msg = str(e)
        if msg.startswith("campo_obrigatorio_faltando"):
            raise HTTPException(status_code=422, detail=msg)
        if msg == "formulario_nao_encontrado":
            raise HTTPException(status_code=404, detail=msg)
        # ciclos/fórmulas inválidas → 500 (como no desafio)
        raise HTTPException(status_code=500, detail=msg)


@router.get(
    "/formularios/{formulario_id}/respostas",
    response_model=RespostaListSchema,
    summary="Listar respostas",
)
def listar_respostas(
    formulario_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    total, itens = RespostaService.listar_respostas(db, formulario_id, limit, offset)
    return {"total": total, "itens": itens}


@router.delete(
    "/formularios/{formulario_id}/respostas/{resposta_id}",
    summary="Remover resposta (soft delete)",
)
def deletar_resposta(
    formulario_id: str,
    resposta_id: str,
    db: Session = Depends(get_db),
):
    ok = RespostaService.deletar_resposta(db, formulario_id, resposta_id)
    if not ok:
        raise HTTPException(status_code=404, detail="resposta_nao_encontrada")
    return {"ok": True}
