// frontend/src/pages/FormListPage.js
import React, { useEffect, useState } from "react";
import { listarFormularios, removerFormulario } from "../api/formularioApi";
import { useNavigate } from "react-router-dom";
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
      {!loading && formularios.length === 0 && <p>Nenhum formulário cadastrado.</p>}
      <div className="form-list">
        {formularios.map((form) => (
          <FormCard
            key={form.id}
            title={form.nome}
            description={form.descricao}
            onSubmit={(e) => e.preventDefault()}
          >
            <button type="button" onClick={() => navigate(`/formularios/${form.id}/responder`)}>
              Responder
            </button>
            <button
              type="button"
              onClick={() => {
                setFormToDelete(form.id);
                setModalOpen(true);
              }}
              style={{ marginLeft: 8 }}
            >
              Excluir
            </button>
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
