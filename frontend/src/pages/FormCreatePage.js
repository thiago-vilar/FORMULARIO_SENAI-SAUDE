// frontend/src/pages/FormCreatePage.js
import React, { useState } from "react";
import { criarFormulario } from "../api/formularioApi";
import FormCard from "../components/FormCard";
import CampoInput from "../components/CampoInput";

const FormCreatePage = () => {
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [usuario, setUsuario] = useState("");
  const [campos, setCampos] = useState([]);
  const [novoCampo, setNovoCampo] = useState({ tipo: "text", label: "", obrigatorio: false });
  const [mensagem, setMensagem] = useState("");

  const handleAddCampo = () => {
    setCampos([...campos, { ...novoCampo }]);
    setNovoCampo({ tipo: "text", label: "", obrigatorio: false });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    try {
      // mapeia "float" -> "number" (se usuário selecionou número)
      const camposNormalizados = campos.map(c => ({ ...c, tipo: c.tipo === "float" ? "number" : c.tipo }));
      await criarFormulario({
        nome,
        descricao,
        usuario,
        campos: camposNormalizados,
      });
      setMensagem("Formulário criado com sucesso!");
      setNome("");
      setDescricao("");
      setUsuario("");
      setCampos([]);
    } catch (e) {
      setMensagem(e?.detail || "Erro ao criar formulário.");
    }
  };

  return (
    <div className="form-create-page">
      <FormCard title="Criar Novo Formulário" description="Adicione os campos necessários:" onSubmit={handleSubmit}>
        <CampoInput label="Nome do formulário" value={nome} name="nome" onChange={e => setNome(e.target.value)} required />
        <CampoInput label="Descrição" value={descricao} name="descricao" onChange={e => setDescricao(e.target.value)} />
        <CampoInput label="Usuário" value={usuario} name="usuario" onChange={e => setUsuario(e.target.value)} />
        <div className="campos-lista">
          <h4>Campos do formulário</h4>
          {campos.map((campo, idx) => (
            <div key={idx}>{campo.label} ({campo.tipo}) {campo.obrigatorio ? "*" : ""}</div>
          ))}
        </div>
        <div className="novo-campo">
          <CampoInput
            label="Label"
            value={novoCampo.label}
            name="novoCampoLabel"
            onChange={e => setNovoCampo({ ...novoCampo, label: e.target.value })}
            required
          />
          <select
            value={novoCampo.tipo}
            onChange={e => setNovoCampo({ ...novoCampo, tipo: e.target.value })}
          >
            <option value="text">Texto</option>
            <option value="number">Número</option>
          </select>
          <label>
            Obrigatório
            <input
              type="checkbox"
              checked={novoCampo.obrigatorio}
              onChange={e => setNovoCampo({ ...novoCampo, obrigatorio: e.target.checked })}
            />
          </label>
          <button type="button" onClick={handleAddCampo}>Adicionar campo</button>
        </div>
        <button type="submit">Criar Formulário</button>
        {mensagem && <p className="mensagem">{mensagem}</p>}
      </FormCard>
    </div>
  );
};

export default FormCreatePage;
