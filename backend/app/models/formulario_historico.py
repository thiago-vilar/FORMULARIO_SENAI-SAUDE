# backend/app/models/formulario_historico.py
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.models.base import Base
import uuid

class FormularioHistorico(Base):
    __tablename__ = "formularios_historico"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    formulario_id = Column(String, ForeignKey("formularios.id"), nullable=False)
    schema_version = Column(Integer, nullable=False)
    # 🔧 alinhado com Formulario.nome (ANTES: titulo)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500))
    is_ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    campos = relationship(
        "CampoHistorico",
        back_populates="formulario",
        cascade="all, delete-orphan"
    )


class CampoHistorico(Base):
    __tablename__ = "campos_historico"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    formulario_historico_id = Column(String, ForeignKey("formularios_historico.id"), nullable=False)

    nome = Column(String(255))
    label = Column(String(255))
    tipo = Column(String(50))
    obrigatorio = Column(Boolean, default=False)
    expressao = Column(String)
    dependencias = Column(JSON)
    opcoes = Column(JSON)
    condicional = Column(String)
    precisao = Column(Integer)
    formato = Column(String)

    formulario = relationship("FormularioHistorico", back_populates="campos")
