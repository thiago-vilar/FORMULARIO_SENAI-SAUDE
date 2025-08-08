# backend/migrations/versions/20250808_add_campos_calculados.py
"""Add colunas de campos calculados e constraint de unicidade (formulario_id, nome)

Revision ID: 20250808_add_campos_calculados
Revises: f0745692056c
Create Date: 2025-08-08 18:00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20250808_add_campos_calculados"
down_revision: Union[str, Sequence[str], None] = "f0745692056c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # novas colunas em 'campos' (todas nullable=True para não quebrar dados existentes)
    with op.batch_alter_table("campos") as batch:
        batch.add_column(sa.Column("nome", sa.String(), nullable=True))
        batch.add_column(sa.Column("expressao", sa.String(), nullable=True))
        batch.add_column(sa.Column("dependencias", sa.JSON(), nullable=True))
        batch.add_column(sa.Column("opcoes", sa.JSON(), nullable=True))
        batch.add_column(sa.Column("condicional", sa.JSON(), nullable=True))
        batch.add_column(sa.Column("precisao", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("formato", sa.String(), nullable=True))

    # constraint única: (formulario_id, nome)
    op.create_unique_constraint(
        "uq_campos_formulario_nome",
        "campos",
        ["formulario_id", "nome"],
    )

    # (opcional) índice para acelerar listagem de respostas por formulário
    op.create_index(
        "ix_respostas_formulario_criadoem",
        "respostas",
        ["formulario_id", "criado_em"],
        unique=False,
    )


def downgrade() -> None:
    # remove índice opcional
    op.drop_index("ix_respostas_formulario_criadoem", table_name="respostas")

    # remove unique
    op.drop_constraint("uq_campos_formulario_nome", "campos", type_="unique")

    # remove colunas novas
    with op.batch_alter_table("campos") as batch:
        batch.drop_column("formato")
        batch.drop_column("precisao")
        batch.drop_column("condicional")
        batch.drop_column("opcoes")
        batch.drop_column("dependencias")
        batch.drop_column("expressao")
        batch.drop_column("nome")
