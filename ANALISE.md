# ANALISE.md — Projeto FORMULARIO_SAUDE-SENAI

---

## 1. Contexto do Projeto
O **FORMULARIO_SAUDE-SENAI** foi desenvolvido para solucionar a dificuldade que instituições de saúde enfrentam ao criar e manter **formulários dinâmicos, versionados e auditáveis**.  
O sistema permite que novas versões sejam criadas sem perder o histórico, com validações automáticas e integração simples com sistemas externos.

**Objetivos principais:**
- Criar e gerenciar formulários sem alteração de código-fonte.
- Garantir integridade, segurança e rastreabilidade dos dados.
- Integrar facilmente com frontends e outros serviços.

---

## 2. Justificativas Arquiteturais

### 2.1 Padrão Arquitetural
Optou-se por um **MVC adaptado**, separando responsabilidades:
- **Controllers/Routers:** tratam requisições HTTP e definem endpoints.
- **Services:** implementam a lógica de negócio.
- **Models:** mapeiam entidades no banco via SQLAlchemy.
- **Schemas:** validam entrada/saída com Pydantic.

**Benefícios:**
- Melhor organização e manutenção do código.
- Facilidade para testes unitários.
- Isolamento de camadas.

---

### 2.2 Padrões de Projeto
- **Singleton** — `DatabaseSessionFactory`: garante uma instância única de conexão com o banco, evitando sobrecarga.
- **Factory** — instanciamento dinâmico de campos conforme tipo.
- **Observer** — engine de cálculo reativa, notificando campos dependentes.

**Motivo da escolha:**  
Esses padrões aumentam **reutilização**, **testabilidade** e **facilidade de evolução**.

---

### 2.3 Tecnologias Escolhidas
**Backend**
- **Python 3.11+** — suporte a tipagem avançada.
- **FastAPI** — alta performance, OpenAPI nativo.
- **SQLAlchemy + Alembic** — ORM robusto com migrations versionadas.
- **Pydantic** — validação rigorosa.
- **Loguru** — logging estruturado.

**Frontend**
- **React.js** — SPA modular.
- **Axios** — consumo da API.

**Banco**
- **PostgreSQL 16** — tipos avançados e integridade transacional.

**Containerização**
- **Docker/Docker Compose** — portabilidade e padronização de ambientes.

---

## 3. Engine Reativa
O sistema implementa um **mecanismo reativo** para campos dependentes:
1. Um campo pode depender do valor de outro.
2. Alterações no campo pai disparam eventos.
3. Campos calculados são automaticamente atualizados no backend antes de persistir.

**Benefício:** garante que cálculos e validações não dependam apenas do frontend, mantendo integridade no backend.

---

## 4. Segurança e Escalabilidade
- **Segurança:** validações no backend, controle de versões, soft delete com `AuditLog`.
- **Escalabilidade:** arquitetura extensível para novos tipos de campo e novas regras de validação sem quebrar o core.

---

## 5. Decisões e Trade-offs
- Optou-se por **FastAPI** ao invés de Django REST Framework pela performance, leveza e geração automática de documentação.
- Uso de **PostgreSQL** para suportar JSONB e tipos complexos — essencial para armazenar schemas dinâmicos.
- A escolha por **MVC adaptado** traz mais clareza ao código, mas exige disciplina para manter a separação de responsabilidades.
- A **engine reativa** aumenta robustez mas também complexidade inicial de implementação.

---

## 6. Próximos Passos
- Implementar testes automatizados (Pytest).
- Adicionar autenticação e controle de permissões.
- Criar interface administrativa para construção de formulários.
- Otimizar consultas e índices no PostgreSQL para grandes volumes.

---

**(imagem)** — Diagrama de sequência mostrando fluxo de criação de formulário e submissão de respostas.
