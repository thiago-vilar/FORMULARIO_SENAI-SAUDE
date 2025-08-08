# backend/app/services/resposta_service.py
import uuid
from typing import Dict, Any, Tuple, List, Set
from sqlalchemy.orm import Session
from backend.app.models import Formulario, Campo, Resposta

class RespostaService:
    @staticmethod
    def _mapa_campos(formulario: Formulario) -> Dict[str, Campo]:
        mapa = {}
        for c in formulario.campos:
            nome = c.nome or (c.label.strip().replace(" ", "_").lower())
            mapa[nome] = c
        return mapa

    @staticmethod
    def _detectar_ciclo(deps: Dict[str, List[str]]) -> bool:
        indeg = {k:0 for k in deps}
        for k, vs in deps.items():
            for v in vs:
                if v in indeg:
                    indeg[v] += 1
        fila = [k for k,v in indeg.items() if v == 0]
        visit = 0
        while fila:
            n = fila.pop()
            visit += 1
            for v in deps.get(n, []):
                indeg[v] -= 1
                if indeg[v] == 0:
                    fila.append(v)
        return visit != len(deps)

    @staticmethod
    def _avaliar(expr: str, ctx: Dict[str, Any]) -> Any:
        # executor simples e fechado (eval sem builtins)
        env = {**ctx, "__builtins__": {}}
        return eval(expr, env, {})

    @staticmethod
    def _calcular(formulario: Formulario, base: Dict[str, Any]) -> Dict[str, Any]:
        campos = RespostaService._mapa_campos(formulario)
        deps: Dict[str, List[str]] = {}
        exprs: Dict[str, str] = {}

        for nome, c in campos.items():
            if c.tipo == "calculated" and c.expressao:
                exprs[nome] = c.expressao
                dep = c.dependencias if isinstance(c.dependencias, list) else []
                # fallback: tenta inferir
                if not dep:
                    dep = [d for d in campos.keys() if d in c.expressao and d != nome]
                deps[nome] = dep

        if deps and RespostaService._detectar_ciclo(deps):
            raise ValueError("ciclo_dependencias")

        contexto = dict(base)
        pend = set(exprs.keys())
        guard = 0
        while pend and guard < 100:
            resolvidos = []
            for nome in list(pend):
                if all(d in contexto for d in deps.get(nome, [])):
                    contexto[nome] = RespostaService._avaliar(exprs[nome], contexto)
                    resolvidos.append(nome)
            for r in resolvidos:
                pend.remove(r)
            if not resolvidos:
                guard += 1
        if pend:
            raise ValueError(f"nao_resolvido:{sorted(pend)}")
        return {k: contexto[k] for k in exprs.keys()}

    @staticmethod
    def criar_resposta(db: Session, formulario_id: str, payload: Dict[str, Any]) -> Resposta:
        form: Formulario = db.query(Formulario).filter_by(id=formulario_id, is_ativo=True).first()
        if not form:
            raise ValueError("formulario_nao_encontrado")

        mapa = RespostaService._mapa_campos(form)
        # valida obrigatórios (não calculados)
        for nome, c in mapa.items():
            if c.tipo != "calculated" and c.obrigatorio:
                if nome not in payload or payload[nome] in (None, "", []):
                    raise ValueError(f"campo_obrigatorio_faltando:{nome}")

        calculados = RespostaService._calcular(form, payload)

        r = Resposta(
            id=str(uuid.uuid4()),
            formulario_id=form.id,
            schema_version=form.schema_version,
            respostas=payload,
            calculados=calculados or None,
        )
        db.add(r)
        db.commit()
        db.refresh(r)
        return r

    @staticmethod
    def listar_respostas(db: Session, formulario_id: str, limit: int = 50, offset: int = 0) -> Tuple[int, List[Resposta]]:
        q = db.query(Resposta).filter_by(formulario_id=formulario_id, is_ativo=True)
        total = q.count()
        itens = q.order_by(Resposta.criado_em.desc()).limit(limit).offset(offset).all()
        return total, itens

    @staticmethod
    def deletar_resposta(db: Session, formulario_id: str, resposta_id: str) -> bool:
        r = db.query(Resposta).filter_by(id=resposta_id, formulario_id=formulario_id, is_ativo=True).first()
        if not r:
            return False
        from datetime import datetime
        r.is_ativo = False
        r.data_remocao = datetime.utcnow()
        r.usuario_remocao = "system"
        db.commit()
        return True
