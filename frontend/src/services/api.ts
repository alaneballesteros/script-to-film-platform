import axios from 'axios';
import type { Script, ScriptCreateRequest, ScriptGenerateRequest, ScriptResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scriptService = {
  // Generate script from prompt using AI
  async generateScript(request: ScriptGenerateRequest): Promise<Script> {
    // This will call the AI service to generate a script
    const response = await api.post('/scripts/generate', request);
    return response.data;
  },

  // Create/parse an existing script
  async createScript(request: ScriptCreateRequest): Promise<ScriptResponse> {
    const response = await api.post('/scripts', request);
    return response.data;
  },

  // Get a script by ID
  async getScript(scriptId: string): Promise<Script> {
    const response = await api.get(`/scripts/${scriptId}`);
    return response.data;
  },

  // Get all scripts
  async listScripts(): Promise<ScriptResponse[]> {
    const response = await api.get('/scripts');
    return response.data;
  },

  // Generate video prompts for scenes
  async generateVideoPrompts(scriptId: string): Promise<Script> {
    const response = await api.post(`/scripts/${scriptId}/video-prompts`);
    return response.data;
  },
};

export default api;
