# Pipeline de Execução (Flowchart)

```mermaid
flowchart TD
  A[Início da Requisição] --> B{Rota}
  B -->|POST /formularios| C[Validar payload do schema (Pydantic)]
  B -->|PUT /formularios/:id/schema_version| C
  B -->|GET /formularios| L[Listar formulários (filtros/paginação)]
  B -->|GET /formularios/:id| M[Obter schema (versão ativa)]
  B -->|DELETE /formularios/:id| Z[Soft delete formulário]

  %% Criação/versão de schema
  C --> C1[Validações sintáticas (tipos/ids únicos)]
  C1 --> C2[Validações semânticas de campos]
  C2 --> C3[Parser de expressões + DAG de dependências]
  C3 --> C4{Ciclo detectado?}
  C4 -->|Sim| C5[Erro 422: dependência circular]
  C4 -->|Não| C6[Persistir schema + versionamento (DB)]
  C6 --> C7[Registrar AuditLog]
  C7 --> R[Resposta 201/200]

  %% Submissão de resposta
  B -->|POST /formularios/:id/respostas| D[Carregar schema vigente (+ opcional schema_version)]
  D --> E[Aplicar condicional para visibilidade]
  E --> F[Validar obrigatórios visíveis + tipos + regras]
  F --> G[Montar grafo topológico (calculated)]
  G --> H[Resolver expressões (precisão/erros)]
  H --> I{Erro de cálculo? (NaN, div/0, ref inválida)}
  I -->|Sim| I1[Acionar fallback (quando definido) + coletar erro]
  I -->|Não| J[Consolidar respostas + calculados]
  I1 --> J

  J --> K[Persistir resposta (transação)]
  K --> K1[Gerar indicadores assíncronos (opcional/worker)]
  K1 --> R
  L --> R
  M --> R
  Z --> Z1[Marcar is_ativo=false + data_remocao + usuario_remocao]
  Z1 --> Z2[Inativar versões do schema]
  Z2 --> R

  R[Responder (JSON + status code)]
