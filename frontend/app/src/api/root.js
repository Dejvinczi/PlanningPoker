import axios from 'axios';

const API_URL = `http://${process.env.NEXT_PUBLIC_API_HOST}:${process.env.NEXT_PUBLIC_API_PORT}/api`;

const api = axios.create({
  baseURL: `${API_URL}/`,
});

export default api;
