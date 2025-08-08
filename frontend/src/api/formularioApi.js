// frontend/src/api/formularioApi.js
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const criarFormulario = async (formulario) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/formularios`, formulario);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao criar formulário" };
  }
};

export const listarFormularios = async (usuario) => {
  try {
    let url = `${API_BASE_URL}/formularios`;
    if (usuario) {
      url += `?usuario=${encodeURIComponent(usuario)}`;
    }
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao listar formulários" };
  }
};

export const buscarFormularioPorId = async (id) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/formularios/${id}`);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Formulário não encontrado" };
  }
};

export const atualizarFormulario = async (id, formulario) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/formularios/${id}`, formulario);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao atualizar formulário" };
  }
};

export const removerFormulario = async (id) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/formularios/${id}`);
    return response.data;
  } catch (error) {
    throw error?.response?.data || { detail: "Erro ao remover formulário" };
  }
};
