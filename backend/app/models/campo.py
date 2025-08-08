# backend/app/models/campo.py
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Campo(Base):
    __tablename__ = 'campos'
    id = Column(String, primary_key=True)
    formulario_id = Column(String, ForeignKey('formularios.id'), nullable=False)

    # existentes
    tipo = Column(String, nullable=False)          # text | number | select | calculated
    label = Column(String, nullable=False)
    obrigatorio = Column(Boolean, default=False)

    # novos
    nome = Column(String, nullable=True)           # identificador único por formulário
    expressao = Column(String, nullable=True)      # fórmula python
    dependencias = Column(JSON, nullable=True)     # ["peso","altura"]
    opcoes = Column(JSON, nullable=True)           # select
    condicional = Column(JSON, nullable=True)      # regras de visibilidade
    precisao = Column(Integer, nullable=True)
    formato = Column(String, nullable=True)

    formulario = relationship('Formulario', back_populates='campos')

    __table_args__ = (
        UniqueConstraint('formulario_id', 'nome', name='uq_campos_formulario_nome'),
    )
