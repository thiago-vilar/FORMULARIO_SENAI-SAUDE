from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict, field_validator


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

    # Aceita string (ex.: "idade >= 18") OU dict (ex.: {"expressao": "idade >= 18"})
    condicional: Optional[Union[str, Dict[str, Any]]] = None

    precisao: Optional[int] = None
    formato: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    # Normaliza condicional string -> dict
    @field_validator("condicional")
    @classmethod
    def normaliza_condicional(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return {"expressao": v}
        if isinstance(v, dict):
            return v
        raise TypeError("condicional deve ser string ou dict")
