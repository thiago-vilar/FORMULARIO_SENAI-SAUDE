// frontend/src/pages/FormListPage.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { listarFormularios, removerFormulario } from "../api/formularioApi";
import FormCard from "../components/FormCard";
import ConfirmModal from "../components/ConfirmModal";

const FormListPage = () => {
  const [formularios, setFormularios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formToDelete, setFormToDelete] = useState(null);
  const navigate = useNavigate();

  const fetchFormularios = async () => {
    setLoading(true);
    try {
      const data = await listarFormularios();
      setFormularios(data);
    } catch (e) {
      alert("Erro ao carregar formulários.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFormularios();
  }, []);

  const handleDelete = async (id) => {
    try {
      await removerFormulario(id);
      setModalOpen(false);
      setFormToDelete(null);
      fetchFormularios();
    } catch (e) {
      alert(e?.detail || "Erro ao remover formulário.");
    }
  };

  return (
    <div className="form-list-page">
      <h2>Formulários Disponíveis</h2>
      {loading && <p>Carregando...</p>}
      {!loading && formularios.length === 0 && (
        <p>Nenhum formulário cadastrado.</p>
      )}
      <div className="form-list">
        {formularios.map((form) => (
          <FormCard
            key={form.id}
            title={form.nome}
            description={form.descricao}
            onSubmit={(e) => e.preventDefault()}
          >
            <div className="form-card__actions" style={{ display: "flex", gap: "8px" }}>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => navigate(`/formularios/${form.id}/responder`)}
              >
                Responder
              </button>

              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate(`/formularios/${form.id}/respostas`)}
              >
                Ver Respostas
              </button>

              <button
                type="button"
                className="btn btn-danger"
                onClick={() => {
                  setFormToDelete(form.id);
                  setModalOpen(true);
                }}
              >
                Excluir
              </button>
            </div>
          </FormCard>
        ))}
      </div>

      <ConfirmModal
        isOpen={modalOpen}
        title="Remover Formulário"
        message="Deseja realmente remover este formulário?"
        onConfirm={() => handleDelete(formToDelete)}
        onCancel={() => setModalOpen(false)}
      />
    </div>
  );
};

export default FormListPage;
