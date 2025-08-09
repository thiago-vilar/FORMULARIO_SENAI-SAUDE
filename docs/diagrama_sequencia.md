
---

### `docs/sequencia.md`
```markdown
# Diagrama de Sequência — Criação e Submissão

Cobre dois fluxos: (1) criar formulário; (2) submeter respostas com cálculo reativo.

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente/Frontend
    participant API as FastAPI (Routers)
    participant SVC as Service (Forms/Responses)
    participant ENG as Engine Reativa
    participant DB as PostgreSQL

    rect rgb(245,245,245)
    note over C,DB: (1) Criar Formulário (schema_version=1)
    C->>API: POST /formularios {nome, descricao, campos[]}
    API->>SVC: validar schema (tipos, ids únicos, regras)
    SVC->>ENG: validar expressões e dependências (parse + ciclo)
    ENG-->>SVC: OK (grafo acíclico)
    SVC->>DB: INSERT FORMULARIO + CAMPOS
    DB-->>SVC: IDs persistidos
    SVC-->>API: 201 {id, schema_version:1}
    API-->>C: 201 Created
    end

    rect rgb(245,245,245)
    note over C,DB: (2) Submeter Respostas (com calculated)
    C->>API: POST /formularios/:id/respostas {respostas{...}}
    API->>SVC: carregar formulário ativo + campos
    SVC->>ENG: avaliar visibilidade/condicionais
    ENG-->>SVC: campos visíveis + obrigatórios
    SVC->>ENG: resolver dependências calculadas (topological sort)
    ENG-->>SVC: calculados {imc, classificacao_imc, ...}
    SVC->>DB: INSERT RESPOSTA + RESPOSTA_VALOR (inclui calculados)
    DB-->>SVC: persistido
    SVC->>DB: INSERT AUDIT_LOG (execução, regras avaliadas)
    DB-->>SVC: OK
    SVC-->>API: 201 {id_resposta, calculados, executado_em}
    API-->>C: 201 Created
    end
