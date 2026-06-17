/**
 * API service using native fetch (no axios, no Node.js dependencies)
 */

import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIService {
  private async getHeaders(): Promise<HeadersInit> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    const token = await SecureStore.getItemAsync('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = await this.getHeaders();
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    });

    if (response.status === 401) {
      await SecureStore.deleteItemAsync('auth_token');
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response;
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    return { data: await response.json() };
  }

  async register(userData: { email: string; password: string; fullName: string }) {
    const response = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    return { data: await response.json() };
  }

  async getCurrentUser() {
    const response = await this.request('/auth/me');
    return { data: await response.json() };
  }

  // Upload endpoints
  async uploadDocument(file: any) {
    const formData = new FormData();
    formData.append('file', file);
    
    const headers = await this.getHeaders();
    delete headers['Content-Type']; // Let browser set it for FormData
    
    const response = await fetch(`${API_BASE_URL}/upload/document`, {
      method: 'POST',
      headers,
      body: formData,
    });
    
    return { data: await response.json() };
  }

  async uploadVoice(audioBlob: Blob) {
    const formData = new FormData();
    formData.append('audio_file', audioBlob);
    
    const headers = await this.getHeaders();
    delete headers['Content-Type'];
    
    const response = await fetch(`${API_BASE_URL}/upload/voice`, {
      method: 'POST',
      headers,
      body: formData,
    });
    
    return { data: await response.json() };
  }

  async uploadText(text: string) {
    const formData = new FormData();
    formData.append('text', text);
    
    const response = await this.request('/upload/text', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
    return { data: await response.json() };
  }

  // Schedule endpoints
  async generateSchedule(request: any) {
    const response = await this.request('/schedule/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    return { data: await response.json() };
  }

  async getSchedule(scheduleId: string) {
    const response = await this.request(`/schedule/${scheduleId}`);
    return { data: await response.json() };
  }

  async updateSchedule(scheduleId: string, updates: any) {
    const response = await this.request(`/schedule/${scheduleId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
    return { data: await response.json() };
  }

  // Analytics endpoints
  async getProgressAnalytics(timeframe: string = 'weekly') {
    const response = await this.request(`/analytics/progress?timeframe=${timeframe}`);
    return { data: await response.json() };
  }

  async getProgressCharts(chartType: string = 'progress') {
    const response = await this.request(`/analytics/charts?chart_type=${chartType}`);
    return { data: await response.json() };
  }

  async generateReport(reportType: string = 'weekly') {
    const response = await this.request(`/analytics/report?report_type=${reportType}`);
    return { data: await response.json() };
  }

  // Reminder endpoints
  async createReminder(request: any) {
    const response = await this.request('/reminder/create', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    return { data: await response.json() };
  }

  async listReminders() {
    const response = await this.request('/reminder/list');
    return { data: await response.json() };
  }

  async deleteReminder(reminderId: string) {
    const response = await this.request(`/reminder/${reminderId}`, {
      method: 'DELETE',
    });
    return { data: await response.json() };
  }
}

// Export individual API modules
export const authAPI = {
  login: (credentials: { email: string; password: string }) => new APIService().login(credentials),
  register: (userData: { email: string; password: string; fullName: string }) => new APIService().register(userData),
  getCurrentUser: () => new APIService().getCurrentUser(),
};

export const uploadAPI = {
  uploadDocument: (file: any) => new APIService().uploadDocument(file),
  uploadVoice: (audioBlob: Blob) => new APIService().uploadVoice(audioBlob),
  uploadText: (text: string) => new APIService().uploadText(text),
};

export const scheduleAPI = {
  generate: (request: any) => new APIService().generateSchedule(request),
  get: (scheduleId: string) => new APIService().getSchedule(scheduleId),
  update: (scheduleId: string, updates: any) => new APIService().updateSchedule(scheduleId, updates),
};

export const analyticsAPI = {
  getProgress: (timeframe?: string) => new APIService().getProgressAnalytics(timeframe),
  getCharts: (chartType?: string) => new APIService().getProgressCharts(chartType),
  generateReport: (reportType?: string) => new APIService().generateReport(reportType),
};

export const reminderAPI = {
  create: (request: any) => new APIService().createReminder(request),
  list: () => new APIService().listReminders(),
  delete: (reminderId: string) => new APIService().deleteReminder(reminderId),
};

export default APIService;
