// frontend/src/api/http.js
import axios from "axios";

const http = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
  timeout: 15000,
});

http.interceptors.response.use(
  (res) => res,
  (error) => {
    const detail = error?.response?.data?.detail || "Erro na comunicação com a API";
    return Promise.reject({ ...error, detail });
  }
);

export default http;
