# backend/app/schemas/formulario_schema.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from backend.app.schemas.campo_schema import CampoCreateSchema

class FormularioCreateSchema(BaseModel):
    nome: str
    descricao: Optional[str] = None
    usuario: Optional[str] = None
    campos: List[CampoCreateSchema]

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class FormularioSchema(FormularioCreateSchema):
    id: str
    schema_version: int
    is_ativo: bool
    data_criacao: datetime

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)
