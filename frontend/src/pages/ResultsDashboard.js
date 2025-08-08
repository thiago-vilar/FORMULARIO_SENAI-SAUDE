// frontend/src/pages/ResultsDashboard.js

import React, { useState } from "react";
import { calcularIMC } from "../api/respostaApi";
import FormCard from "../components/FormCard";
import CampoInput from "../components/CampoInput";

const ResultsDashboard = () => {
  const [peso, setPeso] = useState("");
  const [altura, setAltura] = useState("");
  const [resultado, setResultado] = useState(null);
  const [mensagem, setMensagem] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    setResultado(null);
    try {
      const data = await calcularIMC({ peso: Number(peso), altura: Number(altura) });
      setResultado(data);
    } catch (e) {
      setMensagem(e?.detail || "Erro ao calcular IMC.");
    }
  };

  return (
    <div className="results-dashboard">
      <FormCard title="Calcule seu IMC" description="Preencha os dados para obter o resultado:" onSubmit={handleSubmit}>
        <CampoInput
          label="Peso (kg)"
          type="number"
          value={peso}
          name="peso"
          min="1"
          onChange={e => setPeso(e.target.value)}
          required
        />
        <CampoInput
          label="Altura (cm)"
          type="number"
          value={altura}
          name="altura"
          min="1"
          onChange={e => setAltura(e.target.value)}
          required
        />
        <button type="submit">Calcular IMC</button>
      </FormCard>
      {mensagem && <p className="mensagem">{mensagem}</p>}
      {resultado && (
        <div className="resultado-imc">
          <h4>Resultado:</h4>
          <p>IMC: <strong>{resultado.imc}</strong></p>
          <p>Classificação: <strong>{resultado.classificacao}</strong></p>
        </div>
      )}
    </div>
  );
};

export default ResultsDashboard;
