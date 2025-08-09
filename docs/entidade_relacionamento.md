# Diagrama ER — FORMULARIO_SAUDE-SENAI

> Modelo lógico simplificado para o backend (PostgreSQL + SQLAlchemy).

```mermaid
erDiagram
    FORMULARIO {
        uuid id PK
        string nome
        string descricao
        int    schema_version
        boolean is_ativo
        timestamptz data_criacao
        timestamptz data_remocao
        string usuario_remocao
        boolean protegido
    }

    CAMPO {
        uuid   id PK
        uuid   formulario_id FK
        string nome                 // identificador técnico no schema (ex: "imc")
        string label
        string tipo                 // text|number|boolean|date|select|calculated
        boolean obrigatorio
        jsonb  opcoes               // para select
        string expressao            // para calculated
        int    precisao             // opcional (númerico)
        string formato              // inteiro|decimal (number)
        string condicional          // expressão booleana para visibilidade/obrigatoriedade
        int    ordem                // posição no formulário
        jsonb  dependencias         // ["peso","altura"]
        boolean is_ativo
    }

    RESPOSTA {
        uuid   id PK
        uuid   formulario_id FK
        int    schema_version
        timestamptz criado_em
        boolean is_ativo
        timestamptz data_remocao
        string usuario_remocao
    }

    RESPOSTA_VALOR {
        uuid   id PK
        uuid   resposta_id FK
        string campo_nome           // chave do campo (ex: "peso")
        jsonb  valor                // valor enviado (ou calculado) normalizado
        boolean is_calculado        // marca campos calculated
    }

    AUDIT_LOG {
        uuid   id PK
        string entidade             // "formulario"|"resposta"|"campo"
        string acao                 // "create"|"update"|"remocao_logica"|"execucao"
        uuid   referencia_id
        timestamptz data_hora
        string usuario
        jsonb  metadata             // diffs, contexto, regras executadas, etc.
    }

    FORMULARIO ||--o{ CAMPO : "possui"
    FORMULARIO ||--o{ RESPOSTA : "recebe"
    RESPOSTA ||--o{ RESPOSTA_VALOR : "compõe"
    FORMULARIO ||--o{ AUDIT_LOG : "gera"
    RESPOSTA ||--o{ AUDIT_LOG : "gera"
