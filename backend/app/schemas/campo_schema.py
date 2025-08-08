# backend/app/schemas/campo_schema.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class CampoCreateSchema(BaseModel):
    id: Optional[str] = None
    tipo: str
    label: str
    obrigatorio: Optional[bool] = False

    # novos (todos opcionais p/ compatibilidade)
    nome: Optional[str] = None
    expressao: Optional[str] = None
    dependencias: Optional[List[str]] = None
    opcoes: Optional[List[Any]] = None         # pode ser ["A"] ou [{"label","value"}]
    condicional: Optional[Dict[str, Any]] = None
    precisao: Optional[int] = None
    formato: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
