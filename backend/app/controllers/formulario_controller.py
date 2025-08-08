# backend/app/controllers/formulario_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.schemas.formulario_schema import FormularioSchema, FormularioCreateSchema
from backend.app.services.formulario_service import FormularioService
from backend.app.db.session import DatabaseSessionFactory

router = APIRouter()

def get_db():
    db = DatabaseSessionFactory()()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/formularios",
    response_model=FormularioSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo formulário",
)
def criar(formulario: FormularioCreateSchema, db: Session = Depends(get_db)):
    try:
        return FormularioService.criar_formulario(db, formulario)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get(
    "/formularios",
    response_model=List[FormularioSchema],
    summary="Listar todos os formulários",
)
def listar(usuario: Optional[str] = None, db: Session = Depends(get_db)):
    if usuario:
        return FormularioService.obter_formularios_por_usuario(db, usuario)
    return FormularioService.listar_formularios(db)

@router.get(
    "/formularios/{id}",
    response_model=FormularioSchema,
    summary="Buscar formulário por ID",
)
def get_formulario(id: str, db: Session = Depends(get_db)):
    formulario = FormularioService.obter_formulario(db, id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return formulario

@router.put(
    "/formularios/{id}",
    response_model=FormularioSchema,
    summary="Atualizar formulário (incrementa schema_version)",
)
def update_formulario(id: str, form: FormularioCreateSchema, db: Session = Depends(get_db)):
    try:
        formulario = FormularioService.atualizar_formulario(db, id, form)
        if not formulario:
            raise HTTPException(status_code=404, detail="Formulário não encontrado")
        return formulario
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete(
    "/formularios/{id}",
    summary="Remover formulário (remoção lógica)",
)
def delete_formulario(id: str, db: Session = Depends(get_db)):
    removido = FormularioService.deletar_formulario(db, id)
    if not removido:
        raise HTTPException(status_code=404, detail="Formulário não encontrado ou já removido")
    return {"ok": True, "message": "Formulário removido"}

# ---- Versionamento ----

# Atalho: atualiza schema e incrementa versão (sem histórico materializado)
@router.post(
    "/formularios/{id}/versionar-atalho",
    response_model=FormularioSchema,
    summary="Criar nova versão do formulário (atalho, sem histórico)",
)
def versionar_atalho(id: str, form: FormularioCreateSchema, db: Session = Depends(get_db)):
    try:
        formulario = FormularioService.atualizar_formulario(db, id, form)
        if not formulario:
            raise HTTPException(status_code=404, detail="Formulário não encontrado")
        return formulario
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

# Oficial: cria snapshot da versão atual no histórico e só então incrementa a versão
@router.post(
    "/formularios/{id}/versionar",
    summary="Versionar formulário e salvar histórico (snapshot da versão atual)",
)
def versionar_oficial(id: str, db: Session = Depends(get_db)):
    try:
        historico = FormularioService.versionar_formulario(db, id)
        return {
            "mensagem": "Formulário versionado com sucesso",
            "historico_id": historico.id,
            "schema_version_snapshot": historico.schema_version,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
