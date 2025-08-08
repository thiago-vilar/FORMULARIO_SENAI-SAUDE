// frontend/src/api/respostaApi.js
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const calcularIMC = async ({ peso, altura }) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/calcular-imc`, { peso, altura });
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao calcular IMC" };
  }
};

export const enviarRespostas = async (formularioId, respostas) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/formularios/${encodeURIComponent(formularioId)}/respostas`, { respostas });
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao enviar respostas" };
  }
};

export const listarRespostas = async (formularioId, { limit = 50, offset = 0 } = {}) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/formularios/${encodeURIComponent(formularioId)}/respostas`, {
      params: { limit, offset },
    });
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao listar respostas" };
  }
};

export const removerResposta = async (formularioId, respostaId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/formularios/${encodeURIComponent(formularioId)}/respostas/${encodeURIComponent(respostaId)}`);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao remover resposta" };
  }
};
