import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // URL Backend

export const registerUser = async (email, password) => {
  return axios.post(`${API_URL}/register`, { email, password });
};

export const loginUser = async (email, password) => {
  return axios.post(`${API_URL}/login`, { email, password });
};

export const getMe = async (token) => {
  return axios.get(`${API_URL}/me`, { params: { token } });
};

export const getPrompts = async () => {
  return axios.get(`${API_URL}/prompts`);
};

export const addPrompt = async (text, user_email) => {
  return axios.post(`${API_URL}/prompts`, { text, user_email });
};

export const sendFeedback = async (prompt_id, user_email, feedback) => {
  return axios.post(`${API_URL}/feedback`, { prompt_id, user_email, feedback });
};

export const askAI = async (text, user_email) => {
  return axios.post(`${API_URL}/ai`, { text, user_email });
};
