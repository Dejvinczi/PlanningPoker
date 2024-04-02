import axios from 'axios';

const BASE_URL = `http://${process.env.NEXT_PUBLIC_API_HOST}:${process.env.NEXT_PUBLIC_API_PORT}`;

const api = axios.create({
  baseURL: `${BASE_URL}/api/`,
});

export default api;
