# backend/app/services/resposta_service.py

import uuid
from typing import Dict, Any, Tuple, List
from sqlalchemy.orm import Session
from backend.app.models import Formulario, Campo, Resposta


class RespostaService:
    # -------------------------- MAPA DE CAMPOS --------------------------
    @staticmethod
    def _mapa_campos(formulario: Formulario) -> Dict[str, Campo]:
        """
        Mapeia 'nome lógico' -> Campo.
        Se 'nome' vier vazio no banco, cria a partir do label (fallback).
        """
        mapa: Dict[str, Campo] = {}
        for c in formulario.campos:
            nome = c.nome or (c.label or "").strip().replace(" ", "_").lower()
            mapa[nome] = c
        return mapa

    # ----------------------- DETECÇÃO DE CICLO (KAHN) -------------------
    @staticmethod
    def _detectar_ciclo(deps: Dict[str, List[str]]) -> bool:
        """
        deps: {campo_calculado -> [dependencias]}
        Só consideramos nós calculados como nós do grafo.
        """
        indeg = {k: 0 for k in deps}  # apenas nós calculados
        # computa indegree apenas quando aresta aponta para outro calculado
        for k, vs in deps.items():
            for v in vs:
                if v in indeg:
                    indeg[v] += 1

        fila: List[str] = [k for k, v in indeg.items() if v == 0]
        visit = 0

        while fila:
            n = fila.pop()
            visit += 1
            for v in deps.get(n, []):
                if v in indeg:  # **importante**: só decrementa se 'v' é calculado
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        fila.append(v)

        # se há nós calculados e nem todos foram visitados, há ciclo
        return bool(deps) and visit != len(indeg)

    # -------------------------- AVALIAÇÃO DE EXPRESSÃO ------------------
    @staticmethod
    def _avaliar(expr: str, ctx: Dict[str, Any]) -> Any:
        """
        Avaliador restrito. Sem builtins.
        Você pode whitelistar funções aqui (min, max, abs, round, etc.)
        """
        env = {
            "__builtins__": {},
            # funções básicas úteis (se desejar)
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
        }
        try:
            return eval(expr, env, ctx)
        except Exception as e:
            raise ValueError(f"expressao_invalida:{expr} -> {e}")

    # ----------------------------- CÁLCULO ------------------------------
    @staticmethod
    def _calcular(formulario: Formulario, base: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve todos os campos 'calculated' em ordem topológica.
        Considera dependências apenas entre calculados; dependências em campos base
        (não calculados) são apenas checadas de existência no contexto.
        """
        campos = RespostaService._mapa_campos(formulario)

        deps: Dict[str, List[str]] = {}   # apenas para calculados
        exprs: Dict[str, str] = {}        # nome_calculado -> expressão

        # monta tabelas de expressões e dependências declaradas
        for nome, c in campos.items():
            if c.tipo == "calculated" and c.expressao:
                exprs[nome] = c.expressao
                dep = c.dependencias if isinstance(c.dependencias, list) else []
                # fallback ingênuo de inferência (opcional)
                if not dep:
                    dep = [d for d in campos.keys() if d in c.expressao and d != nome]
                deps[nome] = dep

        # detecta ciclo apenas entre calculados
        if deps and RespostaService._detectar_ciclo(deps):
            raise ValueError("ciclo_dependencias")

        contexto: Dict[str, Any] = dict(base)
        pend = set(exprs.keys())
        guard = 0

        while pend and guard < 200:  # limite de segurança
            resolvidos = []
            for nome in list(pend):
                dependencias = deps.get(nome, [])
                # só avança quando TODAS as dependências estão no contexto (base + já calculados)
                if all(d in contexto for d in dependencias):
                    contexto[nome] = RespostaService._avaliar(exprs[nome], contexto)
                    resolvidos.append(nome)

            for r in resolvidos:
                pend.remove(r)

            if not resolvidos:
                guard += 1

        if pend:
            # não conseguiu resolver algum calculado (provável dependência ausente ou erro de tipo)
            raise ValueError(f"nao_resolvido:{sorted(pend)}")

        return {k: contexto[k] for k in exprs.keys()}

    # --------------------------- COERÇÕES ÚTEIS -------------------------
    @staticmethod
    def _coagir_numeros(mapa: Dict[str, Campo], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte strings numéricas para float quando o campo é 'number'.
        Ex.: "80" -> 80.0
        """
        coerced = dict(payload)
        for nome, c in mapa.items():
            if c.tipo == "number" and nome in coerced:
                v = coerced[nome]
                if isinstance(v, str):
                    v = v.strip().replace(",", ".")
                    try:
                        coerced[nome] = float(v)
                    except Exception:
                        raise ValueError(f"valor_invalido:{nome} -> esperado numero (ex.: 80 ou 180.5)")
        return coerced

    # ------------------------------ SERVICE -----------------------------
    @staticmethod
    def criar_resposta(db: Session, formulario_id: str, payload: Dict[str, Any]) -> Resposta:
        form: Formulario = (
            db.query(Formulario)
            .filter_by(id=formulario_id, is_ativo=True)
            .first()
        )
        if not form:
            raise ValueError("formulario_nao_encontrado")

        mapa = RespostaService._mapa_campos(form)

        # valida obrigatórios (não calculados)
        for nome, c in mapa.items():
            if c.tipo != "calculated" and c.obrigatorio:
                if nome not in payload or payload[nome] in (None, "", []):
                    raise ValueError(f"campo_obrigatorio_faltando:{nome}")

        # coerção de números para evitar TypeError no cálculo
        payload = RespostaService._coagir_numeros(mapa, payload)

        # calcula
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
    def listar_respostas(
        db: Session,
        formulario_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[int, List[Resposta]]:
        q = db.query(Resposta).filter_by(formulario_id=formulario_id, is_ativo=True)
        total = q.count()
        itens = q.order_by(Resposta.criado_em.desc()).limit(limit).offset(offset).all()
        return total, itens

    @staticmethod
    def deletar_resposta(db: Session, formulario_id: str, resposta_id: str) -> bool:
        r = (
            db.query(Resposta)
            .filter_by(id=resposta_id, formulario_id=formulario_id, is_ativo=True)
            .first()
        )
        if not r:
            return False
        from datetime import datetime
        r.is_ativo = False
        r.data_remocao = datetime.utcnow()
        r.usuario_remocao = "system"
        db.commit()
        return True
