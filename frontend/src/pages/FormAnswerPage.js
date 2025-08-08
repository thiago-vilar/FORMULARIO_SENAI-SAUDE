// frontend/src/pages/FormAnswerPage.js
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { buscarFormularioPorId } from "../api/formularioApi";
import { enviarResposta } from "../api/respostaApi";
import CampoInput from "../components/CampoInput";
import FormCard from "../components/FormCard";

const FormAnswerPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formulario, setFormulario] = useState(null);
  const [respostas, setRespostas] = useState({});
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    const fetchFormulario = async () => {
      try {
        const data = await buscarFormularioPorId(id);
        setFormulario(data);
      } catch {
        setMensagem("Erro ao carregar formulário.");
      }
    };
    fetchFormulario();
  }, [id]);

  const handleChange = (campoId, valor) => {
    setRespostas((prev) => ({ ...prev, [campoId]: valor }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    try {
      await enviarResposta(id, { respostas });
      setMensagem("Respostas enviadas com sucesso!");
      setTimeout(() => navigate(`/formularios/${id}/respostas`), 1500);
    } catch (error) {
      setMensagem(error?.detail || "Erro ao enviar respostas.");
    }
  };

  if (!formulario) return <p>Carregando formulário...</p>;

  return (
    <div className="form-answer-page">
      <h2>Responder Formulário</h2>
      <FormCard
        title={formulario.nome}
        description={formulario.descricao}
        onSubmit={handleSubmit}
      >
        {formulario.campos?.map((campo) => (
          <CampoInput
            key={campo.id}
            label={campo.label}
            type={campo.tipo || "text"}
            value={respostas[campo.id] || ""}
            name={campo.id}
            onChange={(e) => handleChange(campo.id, e.target.value)}
            required={campo.obrigatorio}
          />
        ))}
        <button type="submit" className="btn btn-primary">
          Enviar Respostas
        </button>
      </FormCard>
      {mensagem && <p className="mensagem">{mensagem}</p>}
    </div>
  );
};

export default FormAnswerPage;
