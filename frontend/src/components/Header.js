import React from "react";
import { Link, NavLink } from "react-router-dom";
import logo from "../assets/logo1.png";

const Header = () => {
  return (
    <header
      style={{
        background: "#ffffff",
        borderBottom: "1px solid var(--color-border)",
      }}
    >
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "12px 16px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Link
          to="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            textDecoration: "none",
          }}
        >
          <img
            src={logo}
            alt="SENAI-Saúde"
            style={{ height: 112, display: "block" }} // Dobrei o tamanho do logo
          />
          <h1 style={{ margin: 0, fontSize: 20, color: "var(--color-primary)" }}>
            SENAI-Saúde
          </h1>
        </Link>

        <nav style={{ display: "flex", gap: 16 }}>
          <NavLink
            to="/formularios"
            style={({ isActive }) => ({
              color: isActive ? "var(--color-primary)" : "var(--color-text)",
              fontWeight: 600,
              textDecoration: "none",
            })}
          >
            Formulários
          </NavLink>
          <NavLink
            to="/formularios/novo"
            style={({ isActive }) => ({
              color: isActive ? "var(--color-primary)" : "var(--color-text)",
              fontWeight: 600,
              textDecoration: "none",
            })}
          >
            Criar
          </NavLink>
          <NavLink
            to="/dashboard"
            style={({ isActive }) => ({
              color: isActive ? "var(--color-primary)" : "var(--color-text)",
              fontWeight: 600,
              textDecoration: "none",
            })}
          >
            Dashboard
          </NavLink>
        </nav>
      </div>
    </header>
  );
};

export default Header;
