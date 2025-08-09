
---

### `docs/engine.md`
```markdown
# Diagrama — Engine Reativa (Topologia e Pipeline)

Mostra (A) grafo de dependências e (B) pipeline de avaliação/validação.

## A) Grafo de Dependências (exemplo IMC)
```mermaid
graph TD
    Peso[peso:number] --> IMC[imc:calculated<br/>peso/((altura/100)^2)]
    Altura[altura:number] --> IMC
    IMC --> Classe[classificacao_imc:calculated<br/>if imc ... then ...]
