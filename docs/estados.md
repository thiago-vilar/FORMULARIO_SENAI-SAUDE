
---

# C) Estados & Regras Transversais (mini-estado) — `docs/estados.md`

```markdown
# Estados & Regras Transversais (Mini-Estado)

> Este diagrama mostra **estados do Formulário** e **da Resposta**, e como **regras transversais** podem bloquear/transicionar.

```mermaid
stateDiagram-v2
  direction LR

  %% -------------------------
  %% FORMULÁRIO (lifecycle)
  %% -------------------------
  state "Formulário" as FORM {
    [*] --> Draft: criação de schema (validações OK)
    Draft --> Ativo: publish (schema_version = 1)
    Ativo --> Ativo: nova versão (PUT schema_version++)
    Ativo --> Inativo: soft delete (is_ativo=false)
    Inativo --> [*]

    note right of Ativo
      Regras transversais:
      - protegido=true impede DELETE
      - GET lista só ativos (a menos de filtro explícito)
      - calculated: sem ciclos; ordem topológica
      - condicional: controla visibilidade/obrigatoriedade
    end note
  }

  %% -------------------------
  %% RESPOSTA (lifecycle)
  %% -------------------------
  state "Resposta" as RESP {
    [*] --> Submetida: POST respostas (validações OK)
    Submetida --> Inativa: soft delete (DELETE resposta)
    Inativa --> [*]

    note right of Submetida
      Regras transversais:
      - Campos calculated não podem ser enviados
      - Obrigatórios só quando visíveis
      - Erros: 400 (faltando), 422 (semântica)
      - Vinculação a schema_version (compatibilidade)
    end note
  }

  %% -------------------------
  %% REGRAS TRANSVERSAIS
  %% -------------------------
  note bottom of FORM
    Transversais (afetam múltiplos fluxos):
    • Soft delete preserva histórico (auditoria)
    • Protegido=true bloqueia remoção manual
    • Rate limit (proteção de abuso) [se habilitado]
    • Cache de DAG/calculated [se habilitado]
    • Logs estruturados + correlação de requisição
  end note

  %% -------------------------
  %% BLOQUEIOS (GUARDS)
  %% -------------------------
  FORM --> FORM: Guard: protegido=true (bloqueia DELETE)
  FORM --> RESP: Guard: is_ativo=false (bloqueia novas respostas)
  RESP --> RESP: Guard: resposta_congelada (bloqueia DELETE)
