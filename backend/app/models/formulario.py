# backend/app/models/formulario.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class Formulario(Base):
    __tablename__ = 'formularios'

    id = Column(String, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500))
    usuario = Column(String(255), nullable=True)

    schema_version = Column(Integer, nullable=False, default=1)

    is_ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, server_default=func.now())
    data_remocao = Column(DateTime, nullable=True)
    usuario_remocao = Column(String, nullable=True)
    protegido = Column(Boolean, default=False)

    campos = relationship('Campo', back_populates='formulario', cascade='all, delete-orphan')
    respostas = relationship('Resposta', back_populates='formulario', cascade='all, delete-orphan')
