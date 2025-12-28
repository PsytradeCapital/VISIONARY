/**
 * API service for mobile app
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async (config) => {
        const token = await SecureStore.getItemAsync('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired, clear stored token
          await SecureStore.deleteItemAsync('auth_token');
          // TODO: Redirect to login
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }): Promise<AxiosResponse> {
    return this.client.post('/auth/login', credentials);
  }

  async register(userData: { email: string; password: string; fullName: string }): Promise<AxiosResponse> {
    return this.client.post('/auth/register', userData);
  }

  async getCurrentUser(): Promise<AxiosResponse> {
    return this.client.get('/auth/me');
  }

  // Upload endpoints
  async uploadDocument(file: any): Promise<AxiosResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.client.post('/upload/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async uploadVoice(audioBlob: Blob): Promise<AxiosResponse> {
    const formData = new FormData();
    formData.append('audio_file', audioBlob);
    
    return this.client.post('/upload/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async uploadText(text: string): Promise<AxiosResponse> {
    const formData = new FormData();
    formData.append('text', text);
    
    return this.client.post('/upload/text', formData);
  }

  // Schedule endpoints
  async generateSchedule(request: any): Promise<AxiosResponse> {
    return this.client.post('/schedule/generate', request);
  }

  async getSchedule(scheduleId: string): Promise<AxiosResponse> {
    return this.client.get(`/schedule/${scheduleId}`);
  }

  async updateSchedule(scheduleId: string, updates: any): Promise<AxiosResponse> {
    return this.client.put(`/schedule/${scheduleId}`, updates);
  }

  // Analytics endpoints
  async getProgressAnalytics(timeframe: string = 'weekly'): Promise<AxiosResponse> {
    return this.client.get('/analytics/progress', { params: { timeframe } });
  }

  async getProgressCharts(chartType: string = 'progress'): Promise<AxiosResponse> {
    return this.client.get('/analytics/charts', { params: { chart_type: chartType } });
  }

  async generateReport(reportType: string = 'weekly'): Promise<AxiosResponse> {
    return this.client.get('/analytics/report', { params: { report_type: reportType } });
  }

  // Reminder endpoints
  async createReminder(request: any): Promise<AxiosResponse> {
    return this.client.post('/reminder/create', request);
  }

  async listReminders(): Promise<AxiosResponse> {
    return this.client.get('/reminder/list');
  }

  async deleteReminder(reminderId: string): Promise<AxiosResponse> {
    return this.client.delete(`/reminder/${reminderId}`);
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