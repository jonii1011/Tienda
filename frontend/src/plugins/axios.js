// src/axios.js
import axios from 'axios';

// Crea una instancia de Axios
const instance = axios.create({
  baseURL: 'http://localhost:8080', // URL de tu backend
});

// Configura el interceptor de solicitud
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default instance;
