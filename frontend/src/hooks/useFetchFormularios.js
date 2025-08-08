// frontend/src/hooks/useFetchFormularios.js

import { useEffect, useState } from "react";
import { listarFormularios } from "../api/formularioApi";

/**
 * Hook para buscar e atualizar a lista de formulários SENAI-Saúde de forma reativa.
 * Aceita parâmetro opcional de usuário para filtrar os formulários desse usuário.
 */
export default function useFetchFormularios(usuario = null) {
  const [formularios, setFormularios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  const fetch = async () => {
    setLoading(true);
    setErro(null);
    try {
      const data = await listarFormularios(usuario);
      setFormularios(data);
    } catch (e) {
      setErro(e?.detail || "Erro ao buscar formulários.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
    // eslint-disable-next-line
  }, [usuario]);

  return { formularios, loading, erro, refresh: fetch };
}
