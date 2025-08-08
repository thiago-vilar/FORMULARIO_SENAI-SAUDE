// frontend/src/pages/FormResponsesPage.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { listarRespostas, removerResposta } from "../api/respostaApi";

const FormResponsesPage = () => {
  const { formularioId } = useParams();
  const [respostas, setRespostas] = useState([]);
  const [mensagem, setMensagem] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchRespostas = async () => {
    setLoading(true);
    try {
      const data = await listarRespostas(formularioId);
      setRespostas(data);
    } catch {
      setMensagem("Erro ao carregar respostas.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRespostas();
  }, [formularioId]);

  const handleDelete = async (respostaId) => {
    try {
      await removerResposta(formularioId, respostaId);
      fetchRespostas();
    } catch {
      setMensagem("Erro ao remover resposta.");
    }
  };

  if (loading) return <p>Carregando respostas...</p>;

  return (
    <div className="form-responses-page">
      <h2>Respostas do Formulário</h2>
      {mensagem && <p>{mensagem}</p>}
      {respostas.length === 0 ? (
        <p>Nenhuma resposta encontrada.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Data</th>
              <th>Respostas</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {respostas.map((resposta) => (
              <tr key={resposta.id}>
                <td>{resposta.id}</td>
                <td>{new Date(resposta.criado_em).toLocaleString()}</td>
                <td>
                  <ul>
                    {Object.entries(resposta.valores || {}).map(([campo, valor]) => (
                      <li key={campo}>
                        <strong>{campo}:</strong> {valor}
                      </li>
                    ))}
                  </ul>
                </td>
                <td>
                  <button
                    className="btn btn-danger btn-sm"
                    onClick={() => handleDelete(resposta.id)}
                  >
                    Excluir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FormResponsesPage;
