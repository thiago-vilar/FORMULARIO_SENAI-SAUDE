# backend/app/services/calculo_service.py
from __future__ import annotations
from typing import Dict, Any, List
from math import floor, ceil, sqrt, log
from sqlalchemy.orm import Session

from backend.app.models import Formulario, Campo
from backend.app.services.calculo_saude import calcular_imc, classificar_imc

# Funções matemáticas/auxiliares permitidas no eval controlado
_ALLOWED_GLOBALS = {
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "floor": floor,
    "ceil": ceil,
    "sqrt": sqrt,
    "log": log,
    # Funções de domínio (opcional usar nas expressões)
    "calcular_imc": calcular_imc,
    "classificar_imc": classificar_imc,
    # True/False/None para expressões condicionais
    "True": True,
    "False": False,
    "None": None,
}

def _toposort(dep_map: Dict[str, List[str]]) -> List[str]:
    """Ordena nós (campos calculados) respeitando dependências (Kahn)."""
    indeg = {k: 0 for k in dep_map}
    for k, deps in dep_map.items():
        for d in deps:
            if d in indeg:
                indeg[d] += 1
    fila = [k for k, deg in indeg.items() if deg == 0]
    ordem: List[str] = []

    while fila:
        n = fila.pop()
        ordem.append(n)
        for d in dep_map.get(n, []):
            if d in indeg:
                indeg[d] -= 1
                if indeg[d] == 0:
                    fila.append(d)

    if len(ordem) != len(dep_map):
        # ciclo detectado
        raise ValueError("ciclo_dependencias_detectado")
    return ordem

def _eval_expressao(expr: str, contexto: Dict[str, Any]) -> Any:
    """
    Avalia expressão de forma controlada:
    - troca '^' por '**' (potência)
    - usa apenas _ALLOWED_GLOBALS como globals
    - 'contexto' (respostas + calculados) como locals
    """
    if not isinstance(expr, str):
        raise ValueError("expressao_invalida")

    # Suporte a notação com '^' (documento usa ^)
    expr_python = expr.replace("^", "**")

    # Eval controlado
    try:
        return eval(expr_python, _ALLOWED_GLOBALS, dict(contexto))
    except Exception as e:
        raise ValueError(f"erro_avaliando_expressao: {e}")

def calcular_calculados(
    db: Session,
    formulario: Formulario,
    respostas_usuario: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Engine reativa:
    1) Monta grafo de dependências só dos campos 'calculated'
    2) Ordena por dependências (toposort)
    3) Avalia expressões atualizando o contexto
    4) Retorna apenas {nome_do_campo_calculado: valor}
    """
    # Contexto começa com as respostas do usuário (ids lógicos = 'nome')
    contexto: Dict[str, Any] = dict(respostas_usuario or {})
    calculados: Dict[str, Any] = {}

    # Seleciona campos calculados do formulário
    campos_calc: List[Campo] = [c for c in (formulario.campos or []) if (c.tipo or "").lower() == "calculated"]

    if not campos_calc:
        return {}

    # Mapa de dependências por nome lógico
    dep_map: Dict[str, List[str]] = {c.nome: list(c.dependencias or []) for c in campos_calc}

    # Ordenação topológica (levanta erro de ciclo)
    ordem = _toposort(dep_map)

    # Índice rápido de Campo por nome
    by_nome = {c.nome: c for c in campos_calc}

    for nome in ordem:
        campo = by_nome[nome]
        expr = campo.expressao or ""
        # Avalia expressao com o contexto atual (inclui respostas + resultados já calculados)
        valor = _eval_expressao(expr, contexto)

        # Aplica precisão (se numérico e precisão fornecida)
        if isinstance(valor, (int, float)) and campo.precisao is not None:
            try:
                valor = round(float(valor), int(campo.precisao))
            except Exception:
                pass

        # Atualiza contexto e dicionário de calculados
        contexto[nome] = valor
        calculados[nome] = valor

    return calculados
