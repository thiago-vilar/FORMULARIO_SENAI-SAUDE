// frontend/src/index.js
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

// Estilos globais do tema SENAI-Saúde
import "./styles/variables.css";
import "./styles/theme.css";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);
