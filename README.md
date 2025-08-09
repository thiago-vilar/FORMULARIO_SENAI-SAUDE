# FORMULARIO_SAUDE-SENAI

Sistema de gerenciamento e execução de **formulários dinâmicos para saúde**, desenvolvido no contexto do projeto **SENAI-Saúde**, com **backend em FastAPI** e **frontend em React.js**.  
O objetivo é permitir que instituições de saúde criem, versionem e processem formulários de forma rápida, validada e integrada.

<!-- PRINT: Logo do Projeto -->

---

## Visão Geral

O **FORMULARIO_SAUDE-SENAI** nasceu para resolver um problema comum em instituições de saúde: a necessidade de **formularios flexíveis, seguros e auditáveis** que possam ser adaptados sem refazer todo o sistema.

No cenário real, clínicas e hospitais precisam coletar informações para avaliações médicas, triagens e acompanhamentos de pacientes. Porém:
- Alterar ou criar um novo formulário muitas vezes exige **mudanças no código-fonte**.
- Não há **versionamento**: atualizações apagam o histórico.
- Validações são feitas de forma manual ou inconsistente.

Este sistema oferece:
- **Criação de formulários** via API, com suporte a múltiplos tipos de campos.
- **Versionamento seguro**, mantendo histórico.
- **Validações rigorosas** via backend.
- **Integração fácil** com qualquer frontend (React incluso no projeto).

**Benefícios principais:**
- **Confiabilidade:** garante que os dados coletados sigam padrões e regras.
- **Escalabilidade:** arquitetura extensível para novos tipos de campo e regras.
- **Agilidade:** criação e alteração de formulários sem reescrever o core do sistema.

<!-- PRINT: Visão Geral / Fluxo alto nível -->

---

## Arquitetura e Padrões

**Padrão arquitetural:**
- **MVC adaptado** com separação clara:
  - **Routers/Controllers:** definem os endpoints e tratam as requisições.
  - **Services:** implementam a lógica de negócio.
  - **Models:** representam entidades e mapeamentos ORM (SQLAlchemy).
  - **Schemas:** definem contratos de entrada e saída (Pydantic).

**Padrões de projeto:**
- **Singleton:** para gerenciar a sessão do banco de dados (`DatabaseSessionFactory`).
- **Factory:** para instanciar dinamicamente campos.
- **Clean Code + SOLID:** facilitando manutenção e evolução.

<!-- PRINT: Diagrama da Arquitetura -->

---

## Tecnologias e Diferenciais da Stack

**Backend:**  
- **Python 3.11+** – linguagem versátil, sintaxe clara e excelente ecossistema para APIs.
- **FastAPI** – framework moderno, rápido e com suporte nativo a OpenAPI/Swagger, ideal para construir APIs robustas e bem documentadas.
- **SQLAlchemy** – ORM poderoso, garantindo abstração segura do banco e suporte a migrações complexas.
- **Alembic** – controle de versionamento de banco de dados.

**Frontend:**  
- **React.js** – biblioteca moderna, focada em componentes reutilizáveis e reatividade na interface.
- **Axios** – cliente HTTP para comunicação com a API de forma simples e eficiente.

**Banco de Dados:**  
- **PostgreSQL 16** – banco relacional robusto, ideal para grandes volumes de dados, com suporte a tipos avançados e integridade transacional.

**Containerização:**  
- **Docker e Docker Compose** – empacotamento e execução consistente da aplicação em qualquer ambiente.

**Por que essa stack?**
- **Produtividade:** desenvolvimento rápido com menos código repetitivo.
- **Escalabilidade:** suporta evolução sem refazer a base.
- **Segurança:** validações de dados no backend e consistência no banco.
- **Portabilidade:** roda localmente ou em nuvem sem esforço extra.

<!-- PRINT: Telas-chave ou Swagger -->

---

## Modelagem de Domínio

**Entidades principais:**
- **Formulario** – metadados do formulário (id, nome, descrição, ativo, criado_em).
- **Campo** – definição dos campos que compõem um formulário (id, nome, tipo, obrigatório, ordem, formulário_id).
- **Resposta** – dados submetidos pelos usuários (id, formulario_id, dados, criado_em).

<!-- PRINT: Diagrama Entidade-Relacionamento -->

---

## API — Endpoints Implementados

### POST `/formularios`
Cria um novo formulário.
- **Request body:** `FormularioCreateSchema`
- **Resposta:** `201 Created` com o formulário criado.

### GET `/formularios`
Lista todos os formulários ou filtra por usuário (`?usuario=`).
- **Resposta:** `200 OK` com lista de formulários.

### GET `/formularios/{id}`
Retorna dados de um formulário específico.
- **Resposta:** `200 OK` com objeto do formulário.

<!-- PRINT: Swagger/OpenAPI navegando nos endpoints -->

---

## Passo a Passo — Clonar, Instalar e Rodar

### 1. Clonar o Repositório
```bash
git clone https://github.com/thiago-vilar/FORMULARIO_SENAI-SAUDE.git
cd FORMULARIO_SENAI-SAUDE

2. Configurar o Backend

cd backend
python -m venv env
source env/bin/activate   # Linux/Mac
.\env\Scripts\activate    # Windows

pip install -r requirements.txt

3. Configurar o Banco de Dados

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_DB=formulariosenai
PORT=4000

Criar o banco no PostgreSQL e aplicar migrations:

alembic upgrade head

4. Rodar o Backend
bash
Copiar
Editar
uvicorn app.main:app --reload --host 0.0.0.0 --port 4000
Acesse o Swagger:
http://localhost:4000/docs

5. Rodar o Frontend
bash
Copiar
Editar
cd ../frontend
npm install
npm start
Acesse:
http://localhost:3000

Execução com Docker
bash
Copiar
Editar
docker compose up -d --build
Isso irá levantar:

API na porta 4000

Frontend na porta 3000

PostgreSQL na porta 5432

Decisões Técnicas
FastAPI escolhido pela performance e geração automática de documentação.

PostgreSQL pela robustez e suporte a dados complexos.

React para garantir uma interface modular e reativa.

Docker para padronizar ambientes e facilitar o deploy.

Roadmap
Implementar endpoints para CRUD de respostas.

Adicionar validações avançadas por tipo de campo.

Criar testes automatizados com Pytest.

Melhorar logs e auditoria.

Contribuindo
Conteúdo não disponível no momento.

Licença
Conteúdo não disponível no momento.

Exemplo Rápido com curl
bash
Copiar
Editar
curl -X POST http://localhost:4000/formularios \
-H "Content-Type: application/json" \
-d '{
  "nome": "Formulário IMC",
  "descricao": "Calcula índice de massa corporal",
  "campos": []
}'
<!-- PRINT: Exemplo de erro e correção -->
Copiar
Editar
