// src/axios.ts
import axios from 'axios';

const instance = axios.create({
  baseURL: '/api', // Proxy will forward to http://localhost:5000
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auto attach token if available
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default instance;