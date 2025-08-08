// frontend/src/App.js
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import FormCreatePage from "./pages/FormCreatePage";
import FormListPage from "./pages/FormListPage";
import ResultsDashboard from "./pages/ResultsDashboard";
import FormAnswerPage from "./pages/FormAnswerPage";
import "./styles/theme.css";
import "./styles/variables.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/formularios" replace />} />
        <Route path="/formularios" element={<FormListPage />} />
        <Route path="/formularios/novo" element={<FormCreatePage />} />
        <Route path="/formularios/:id/responder" element={<FormAnswerPage />} />
        <Route path="/dashboard" element={<ResultsDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
