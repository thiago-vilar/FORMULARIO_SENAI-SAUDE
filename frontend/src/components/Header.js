// frontend/src/components/Header.js
import React from "react";
import logo1 from "../assets/logo1.png"; // ou logo2.png, troque conforme preferir

const Header = () => (
  <header className="app-header">
    <img src={logo1} alt="SENAI Saúde" className="logo-senai" />
    <h1>SENAI-Saúde</h1>
  </header>
);

export default Header;
