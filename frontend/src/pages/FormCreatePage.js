// frontend/src/pages/FormCreatePage.js
import React, { useState } from "react";
import { criarFormulario } from "../api/formularioApi";
import FormCard from "../components/FormCard";
import CampoInput from "../components/CampoInput";

const FormCreatePage = () => {
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [usuario, setUsuario] = useState("thiago");
  const [campos, setCampos] = useState([]);
  const [novoCampo, setNovoCampo] = useState({ tipo: "text", label: "", obrigatorio: false, nome: "" });
  const [mensagem, setMensagem] = useState("");

  const handleAddCampo = () => {
    if (!novoCampo.label) return;
    const nomeNormalizado = (novoCampo.nome || novoCampo.label).trim().toLowerCase().replace(/\s+/g, "_");
    setCampos([...campos, { ...novoCampo, nome: nomeNormalizado }]);
    setNovoCampo({ tipo: "text", label: "", obrigatorio: false, nome: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    try {
      await criarFormulario({ nome, descricao, usuario, campos });
      setMensagem("Formulário criado com sucesso!");
      setNome(""); setDescricao(""); setUsuario("thiago"); setCampos([]);
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
            <div key={idx}>{campo.label} ({campo.tipo}) {campo.obrigatorio ? "*" : ""} — <em>{campo.nome}</em></div>
          ))}
        </div>

        <div className="novo-campo card" style={{ marginTop: 16 }}>
          <h4>Novo campo</h4>
          <CampoInput
            label="Label"
            value={novoCampo.label}
            name="novoCampoLabel"
            onChange={e => setNovoCampo({ ...novoCampo, label: e.target.value })}
            required
          />
          <CampoInput
            label="Nome (opcional)"
            value={novoCampo.nome}
            name="novoCampoNome"
            onChange={e => setNovoCampo({ ...novoCampo, nome: e.target.value })}
            placeholder="se vazio, será gerado a partir do label"
          />
          <label>Tipo</label>
          <select
            value={novoCampo.tipo}
            onChange={e => setNovoCampo({ ...novoCampo, tipo: e.target.value })}
          >
            <option value="text">Texto</option>
            <option value="number">Número</option>
            <option value="select">Select</option>
            <option value="calculated">Calculado</option>
          </select>
          <label style={{ display: "block", marginTop: 8 }}>
            <input
              type="checkbox"
              checked={novoCampo.obrigatorio}
              onChange={e => setNovoCampo({ ...novoCampo, obrigatorio: e.target.checked })}
            /> Obrigatório
          </label>
          <button type="button" className="btn btn-primary" onClick={handleAddCampo}>Adicionar campo</button>
        </div>

        <button type="submit" className="btn btn-primary">Criar Formulário</button>
        {mensagem && <p className="mensagem">{mensagem}</p>}
      </FormCard>
    </div>
  );
};

export default FormCreatePage;
