# backend/app/models/resposta.py

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from .base import Base

class Resposta(Base):
    __tablename__ = 'respostas'
    id = Column(String, primary_key=True)
    formulario_id = Column(String, ForeignKey('formularios.id'), nullable=False)
    schema_version = Column(Integer, nullable=False)
    respostas = Column(JSON, nullable=False)
    calculados = Column(JSON, nullable=True)
    criado_em = Column(DateTime, server_default=func.now())
    is_ativo = Column(Boolean, default=True)
    data_remocao = Column(DateTime, nullable=True)
    usuario_remocao = Column(String, nullable=True)

    formulario = relationship('Formulario', back_populates='respostas')
