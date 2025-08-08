// frontend/src/App.js
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import FormListPage from "./pages/FormListPage";
import FormCreatePage from "./pages/FormCreatePage";
import FormAnswerPage from "./pages/FormAnswerPage";
import ResultsDashboard from "./pages/ResultsDashboard";
import FormResponsesPage from "./pages/FormResponsesPage";



function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/formularios" element={<FormListPage />} />
        <Route path="/formularios/novo" element={<FormCreatePage />} />
        <Route path="/formularios/:id/responder" element={<FormAnswerPage />} />
        <Route path="/formularios/:formularioId/respostas" element={<FormResponsesPage />} />
        <Route path="/dashboard" element={<ResultsDashboard />} />
        {/* fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
