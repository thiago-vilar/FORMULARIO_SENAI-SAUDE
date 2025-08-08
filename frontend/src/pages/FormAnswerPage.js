// frontend/src/pages/FormAnswerPage.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { buscarFormularioPorId } from "../api/formularioApi";
import { enviarRespostas } from "../api/respostaApi";
import FormCard from "../components/FormCard";
import CampoInput from "../components/CampoInput";

export default function FormAnswerPage() {
  const { id } = useParams();
  const [form, setForm] = useState(null);
  const [valores, setValores] = useState({});
  const [resultado, setResultado] = useState(null);
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const f = await buscarFormularioPorId(id);
        setForm(f);
        const init = {};
        (f.campos || [])
          .filter((c) => c.tipo !== "calculated")
          .forEach((c) => {
            const nome = c.nome || (c.label || "").trim().replace(/\s+/g, "_").toLowerCase();
            init[nome] = "";
          });
        setValores(init);
      } catch (e) {
        setMensagem(e.detail || "Falha ao carregar formulário");
      }
    })();
  }, [id]);

  const onChange = (nome, v) => setValores((prev) => ({ ...prev, [nome]: v }));

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {};
      // envia apenas campos não calculados
      (form.campos || [])
        .filter((c) => c.tipo !== "calculated")
        .forEach((c) => {
          const nome = c.nome || (c.label || "").trim().replace(/\s+/g, "_").toLowerCase();
          const raw = valores[nome];
          payload[nome] = c.tipo === "number" ? Number(raw) : raw;
        });

      const r = await enviarRespostas(id, payload);
      setResultado(r);
      setMensagem("");
    } catch (e) {
      setMensagem(e.detail || "Falha ao enviar respostas");
    }
  };

  if (!form) return <p>Carregando...</p>;

  return (
    <div className="form-answer-page">
      <FormCard title={form.nome} description={form.descricao} onSubmit={onSubmit}>
        {(form.campos || []).filter(c => c.tipo !== "calculated").map((c) => {
          const nome = c.nome || (c.label || "").trim().replace(/\s+/g, "_").toLowerCase();
          const type = c.tipo === "number" ? "number" : c.tipo === "select" ? "select" : "text";
          return (
            <div key={c.id || nome}>
              {type === "select" ? (
                <>
                  <label>{c.label}</label>
                  <select
                    value={valores[nome]}
                    onChange={(e) => onChange(nome, e.target.value)}
                    required={!!c.obrigatorio}
                  >
                    <option value="">Selecione</option>
                    {(c.opcoes || []).map((op) =>
                      typeof op === "string" ? (
                        <option key={op} value={op}>{op}</option>
                      ) : (
                        <option key={op.value} value={op.value}>{op.label}</option>
                      )
                    )}
                  </select>
                </>
              ) : (
                <CampoInput
                  label={c.label}
                  type={type}
                  name={nome}
                  value={valores[nome]}
                  onChange={(e) => onChange(nome, e.target.value)}
                  step={type === "number" ? "0.01" : undefined}
                  required={!!c.obrigatorio}
                />
              )}
            </div>
          );
        })}
        <button type="submit">Enviar</button>
      </FormCard>

      {mensagem && <p className="mensagem">{mensagem}</p>}
      {resultado && (
        <div className="resultado-imc">
          <h4>Resposta gravada</h4>
          <pre style={{ background: "#f6f6f6", padding: 12 }}>{JSON.stringify(resultado, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
