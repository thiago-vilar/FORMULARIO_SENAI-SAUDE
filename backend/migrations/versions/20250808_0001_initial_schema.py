"""Initial schema (formularios, campos, respostas)"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql

revision = "20250808_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    op.create_table(
        "formularios",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.String(length=500), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("protegido", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("data_criacao", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("data_remocao", sa.DateTime(timezone=True), nullable=True),
        sa.Column("usuario_remocao", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_formularios_nome", "formularios", ["nome"])

    op.create_table(
        "campos",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("formulario_id", sa.String(length=36), sa.ForeignKey("formularios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("tipo", sa.String(length=32), nullable=False),
        sa.Column("obrigatorio", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("expressao", sa.Text(), nullable=True),
        sa.Column("dependencias", psql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("opcoes", psql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("condicional", sa.Text(), nullable=True),
        sa.Column("precisao", sa.Integer(), nullable=True),
        sa.Column("formato", sa.String(length=32), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("ix_campos_formulario", "campos", ["formulario_id"])
    op.create_index("ix_campos_nome_unq_por_form", "campos", ["formulario_id", "nome"], unique=True)

    op.create_table(
        "respostas",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("formulario_id", sa.String(length=36), sa.ForeignKey("formularios.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("respostas", psql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("calculados", psql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("data_remocao", sa.DateTime(timezone=True), nullable=True),
        sa.Column("usuario_remocao", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_respostas_formulario", "respostas", ["formulario_id"])
    op.create_index("ix_respostas_schema_version", "respostas", ["schema_version"])

def downgrade():
    op.drop_index("ix_respostas_schema_version", table_name="respostas")
    op.drop_index("ix_respostas_formulario", table_name="respostas")
    op.drop_table("respostas")

    op.drop_index("ix_campos_nome_unq_por_form", table_name="campos")
    op.drop_index("ix_campos_formulario", table_name="campos")
    op.drop_table("campos")

    op.drop_index("ix_formularios_nome", table_name="formularios")
    op.drop_table("formularios")
