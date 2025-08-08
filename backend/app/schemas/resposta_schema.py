# backend/app/schemas/resposta_schema.py
from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RespostaCreateSchema(BaseModel):
    respostas: Dict[str, Any] = Field(..., description="Mapa campo->valor (apenas não calculados)")

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class RespostaSchema(BaseModel):
    id: str
    formulario_id: str
    schema_version: int
    respostas: Dict[str, Any]
    calculados: Optional[Dict[str, Any]] = None
    criado_em: Optional[datetime] = None  

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class RespostaListSchema(BaseModel):
    total: int
    itens: List[RespostaSchema]

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)
