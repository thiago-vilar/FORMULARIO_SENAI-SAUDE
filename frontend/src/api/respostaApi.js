// frontend/src/api/respostaApi.js
import axios from "axios";

// URL base da API (usa variável de ambiente ou localhost)
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Calcula o IMC com base em peso (kg) e altura (cm)
 * @param {Object} params - { peso: Number, altura: Number }
 * @returns {Promise<Object>} - { imc: Number, classificacao: String }
 */
export const calcularIMC = async ({ peso, altura }) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/calcular-imc`, { peso, altura });
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao calcular IMC" };
  }
};

/**
 * Envia respostas para um formulário específico
 * @param {number|string} formularioId - ID do formulário
 * @param {Object|Array} payload - Dados das respostas
 * @returns {Promise<Object>} - Dados retornados pela API
 */
export const enviarResposta = async (formularioId, payload) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/formularios/${formularioId}/respostas`,
      payload
    );
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao enviar resposta" };
  }
};

/**
 * Lista respostas de um formulário
 * @param {number|string} formularioId - ID do formulário
 * @returns {Promise<Array>} - Lista de respostas
 */
export const listarRespostas = async (formularioId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/formularios/${formularioId}/respostas`
    );
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao listar respostas" };
  }
};

/**
 * Obtém detalhes de uma resposta específica
 * @param {number|string} formularioId - ID do formulário
 * @param {number|string} respostaId - ID da resposta
 * @returns {Promise<Object>} - Dados da resposta
 */
export const buscarRespostaPorId = async (formularioId, respostaId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/formularios/${formularioId}/respostas/${respostaId}`
    );
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao buscar resposta" };
  }
};

/**
 * Remove uma resposta de um formulário
 * @param {number|string} formularioId - ID do formulário
 * @param {number|string} respostaId - ID da resposta
 * @returns {Promise<Object>} - Confirmação da exclusão
 */
export const removerResposta = async (formularioId, respostaId) => {
  try {
    const response = await axios.delete(
      `${API_BASE_URL}/formularios/${formularioId}/respostas/${respostaId}`
    );
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao remover resposta" };
  }
};
