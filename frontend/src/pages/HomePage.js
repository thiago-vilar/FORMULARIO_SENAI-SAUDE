// frontend/src/pages/HomePage.js
import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <main style={{ maxWidth: 1100, margin: "32px auto", padding: "0 16px" }}>
      <section
        style={{
          textAlign: "center",
          marginBottom: 24,
          background: "var(--color-card)",
          border: "1px solid var(--color-border)",
          borderRadius: 12,
          padding: "28px 16px",
        }}
      >
        <h2 style={{ marginTop: 0, color: "var(--color-primary)" }}>
          Bem-vindo ao SENAI-Saúde
        </h2>
        <p style={{ margin: "8px 0 20px" }}>
          Crie formulários dinâmicos, responda e veja indicadores (IMC e
          classificação) em tempo real.
        </p>

        <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
          <Link to="/formularios/novo">
            <button type="button">Criar Formulário</button>
          </Link>
          <Link to="/formularios">
            <button type="button" style={{ background: "var(--color-secondary)" }}>
              Ver Formulários
            </button>
          </Link>
          <Link to="/dashboard">
            <button type="button">Dashboard (IMC)</button>
          </Link>
        </div>
      </section>
    </main>
  );
};

export default HomePage;
