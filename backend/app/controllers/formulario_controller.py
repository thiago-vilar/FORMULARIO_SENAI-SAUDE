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
    """
    Cria um novo formulário com os campos especificados.
    """
    try:
        return FormularioService.criar_formulario(db, formulario)
    except ValueError as e:
        # Validações de schema (tipos, opções, dependências, ciclo...)
        raise HTTPException(status_code=422, detail=str(e))

@router.get(
    "/formularios",
    response_model=List[FormularioSchema],
    summary="Listar todos os formulários",
)
def listar(usuario: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Lista todos os formulários ativos.
    Opcionalmente, pode filtrar por usuário: /formularios?usuario=fulano
    """
    if usuario:
        return FormularioService.obter_formularios_por_usuario(db, usuario)
    return FormularioService.listar_formularios(db)

@router.get(
    "/formularios/{id}",
    response_model=FormularioSchema,
    summary="Buscar formulário por ID",
)
def get_formulario(id: str, db: Session = Depends(get_db)):
    """
    Retorna um formulário específico pelo seu ID.
    """
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
    """
    Atualiza um formulário existente, **recria os campos** e **incrementa `schema_version`**.
    """
    try:
        formulario = FormularioService.atualizar_formulario(db, id, form)
        if not formulario:
            raise HTTPException(status_code=404, detail="Formulário não encontrado")
        return formulario
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post(
    "/formularios/{id}/versionar",
    response_model=FormularioSchema,
    summary="Criar nova versão do formulário (atalho de versionamento)",
)
def versionar_formulario(id: str, form: FormularioCreateSchema, db: Session = Depends(get_db)):
    """
    Endpoint **explícito** de versionamento.  
    Aplica as mesmas validações do update, **recria campos** e **incrementa `schema_version`**.
    """
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
    """
    Remove logicamente um formulário (não apaga do banco, apenas marca como inativo).
    """
    removido = FormularioService.deletar_formulario(db, id)
    if not removido:
        raise HTTPException(status_code=404, detail="Formulário não encontrado ou já removido")
    return {"ok": True, "message": "Formulário removido"}

@router.get(
    "/formularios/usuario/{usuario}",
    response_model=List[FormularioSchema],
    summary="Buscar formulários por usuário",
)
def get_formularios_por_usuario(usuario: str, db: Session = Depends(get_db)):
    """
    Retorna todos os formulários criados pelo usuário informado.
    """
    return FormularioService.obter_formularios_por_usuario(db, usuario)
