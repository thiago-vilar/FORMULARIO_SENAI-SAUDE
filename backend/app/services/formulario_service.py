# backend/app/services/formulario_service.py
import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models import Formulario, Campo

# ---------- Validações de schema ----------

TIPOS_VALIDOS = {"text", "number", "select", "calculated"}

def _validar_campos_basicos(campos: List[Dict[str, Any]]):
    if not isinstance(campos, list) or len(campos) == 0:
        raise ValueError("campos_vazios")

    for i, c in enumerate(campos):
        tipo = c.get("tipo")
        label = c.get("label")
        if not tipo or tipo not in TIPOS_VALIDOS:
            raise ValueError(f"tipo_invalido:{tipo}@idx={i}")
        if not label or not isinstance(label, str):
            raise ValueError(f"label_invalido@idx={i}")

        if tipo == "select":
            opcoes = c.get("opcoes")
            if not opcoes or not isinstance(opcoes, list) or len(opcoes) == 0:
                raise ValueError(f"opcoes_select_invalidas@idx={i}")

        if tipo == "calculated":
            expr = c.get("expressao")
            if not expr or not isinstance(expr, str):
                raise ValueError(f"expressao_obrigatoria@idx={i}")

def _extrair_nomes(campos: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Define 'nome' lógico:
    - se vier 'nome', usa;
    - senão cria do label normalizado.
    Garante unicidade (em memória) antes de persistir.
    """
    nomes = {}
    for idx, c in enumerate(campos):
        nome = c.get("nome")
        if not nome or not isinstance(nome, str):
            base = (c.get("label") or f"campo_{idx}").strip().lower().replace(" ", "_")
            nome = base
            c["nome"] = nome
        if nome in nomes:
            raise ValueError(f"nome_duplicado:{nome}")
        nomes[nome] = idx
    return nomes

def _validar_dependencias(campos: List[Dict[str, Any]]):
    nomes = _extrair_nomes(campos)
    deps_graph = {c["nome"]: list(c.get("dependencias") or []) for c in campos if c.get("tipo") == "calculated"}

    # checa referências inexistentes
    for nome, deps in deps_graph.items():
        for d in deps:
            if d not in nomes:
                raise ValueError(f"dependencia_inexistente:{nome}->{d}")

    # detecta ciclo (Kahn)
    indeg = {k: 0 for k in deps_graph}
    for k, vs in deps_graph.items():
        for v in vs:
            if v in indeg:
                indeg[v] += 1
    fila = [k for k, v in indeg.items() if v == 0]
    visit = 0
    while fila:
        n = fila.pop()
        visit += 1
        for v in deps_graph.get(n, []):
            if v in indeg:
                indeg[v] -= 1
                if indeg[v] == 0:
                    fila.append(v)
    if deps_graph and visit != len(deps_graph):
        raise ValueError("ciclo_dependencias")

def _normalizar_campos(campos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # number: aceita "float" vindo do front e normaliza
    for c in campos:
        if c.get("tipo") == "float":
            c["tipo"] = "number"
        # opcional: coerção de opcoes para [{label, value}]
        if c.get("tipo") == "select":
            ops = c.get("opcoes") or []
            norm = []
            for op in ops:
                if isinstance(op, str):
                    norm.append({"label": op, "value": op})
                elif isinstance(op, dict) and "value" in op and "label" in op:
                    norm.append(op)
            c["opcoes"] = norm
    return campos

# ---------- Service ----------

class FormularioService:
    @staticmethod
    def criar_formulario(db: Session, payload) -> Formulario:
        data = payload.dict() if hasattr(payload, "dict") else dict(payload)
        campos = data.get("campos") or []

        _validar_campos_basicos(campos)
        _validar_dependencias(campos)
        _normalizar_campos(campos)

        f = Formulario(
            id=str(uuid.uuid4()),
            nome=data["nome"],
            descricao=data.get("descricao"),
            usuario=data.get("usuario"),
            schema_version=1,
            is_ativo=True,
        )
        db.add(f)
        db.flush()

        for c in campos:
            db.add(Campo(
                id=str(uuid.uuid4()),
                formulario_id=f.id,
                tipo=c["tipo"],
                label=c["label"],
                obrigatorio=bool(c.get("obrigatorio", False)),
                nome=c.get("nome"),
                expressao=c.get("expressao"),
                dependencias=c.get("dependencias"),
                opcoes=c.get("opcoes"),
                condicional=c.get("condicional"),
                precisao=c.get("precisao"),
                formato=c.get("formato"),
            ))

        db.commit()
        db.refresh(f)
        return f

    @staticmethod
    def listar_formularios(db: Session) -> List[Formulario]:
        return db.query(Formulario).filter_by(is_ativo=True).order_by(Formulario.data_criacao.desc()).all()

    @staticmethod
    def obter_formulario(db: Session, id: str) -> Formulario | None:
        return db.query(Formulario).filter_by(id=id, is_ativo=True).first()

    @staticmethod
    def obter_formularios_por_usuario(db: Session, usuario: str) -> List[Formulario]:
        return db.query(Formulario).filter_by(is_ativo=True, usuario=usuario).order_by(Formulario.data_criacao.desc()).all()

    @staticmethod
    def atualizar_formulario(db: Session, id: str, payload) -> Formulario | None:
        f = db.query(Formulario).filter_by(id=id, is_ativo=True).first()
        if not f:
            return None

        data = payload.dict() if hasattr(payload, "dict") else dict(payload)
        campos = data.get("campos") or []

        _validar_campos_basicos(campos)
        _validar_dependencias(campos)
        _normalizar_campos(campos)

        # incrementa versão e recria campos
        f.nome = data["nome"]
        f.descricao = data.get("descricao")
        f.usuario = data.get("usuario")
        f.schema_version = int((f.schema_version or 1) + 1)

        # apaga e recria (como você já vinha fazendo)
        db.query(Campo).filter_by(formulario_id=f.id).delete()
        db.flush()

        for c in campos:
            db.add(Campo(
                id=str(uuid.uuid4()),
                formulario_id=f.id,
                tipo=c["tipo"],
                label=c["label"],
                obrigatorio=bool(c.get("obrigatorio", False)),
                nome=c.get("nome"),
                expressao=c.get("expressao"),
                dependencias=c.get("dependencias"),
                opcoes=c.get("opcoes"),
                condicional=c.get("condicional"),
                precisao=c.get("precisao"),
                formato=c.get("formato"),
            ))

        db.commit()
        db.refresh(f)
        return f

    @staticmethod
    def deletar_formulario(db: Session, id: str) -> bool:
        f = db.query(Formulario).filter_by(id=id, is_ativo=True).first()
        if not f:
            return False
        from datetime import datetime
        f.is_ativo = False
        f.data_remocao = datetime.utcnow()
        f.usuario_remocao = "system"  # TODO: integrar com auth/usuário real
        db.commit()
        return True
