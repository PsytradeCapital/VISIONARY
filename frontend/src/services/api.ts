import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    id: string;
    category: string;
    extracted_items: {
      routines: string[];
      goals: string[];
      preferences: string[];
      constraints: string[];
    };
    confidence: number;
  };
}

export const uploadAPI = {
  uploadDocument: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/upload/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  uploadText: async (text: string): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('text', text);
    
    const response = await api.post('/api/upload/text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  uploadVoice: async (audioBlob: Blob): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'voice_input.wav');
    
    const response = await api.post('/api/upload/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getUploadHistory: async () => {
    const response = await api.get('/api/upload/history');
    return response.data;
  },
};

export const progressAPI = {
  getOverview: async () => {
    const response = await api.get('/api/progress/overview');
    return response.data;
  },

  getVisionProgress: async (visionId: string) => {
    const response = await api.get(`/api/progress/vision/${visionId}`);
    return response.data;
  },

  updateVisionMetric: async (visionId: string, metricName: string, newValue: number) => {
    const response = await api.put(`/api/progress/vision/${visionId}/metric`, null, {
      params: { metric_name: metricName, new_value: newValue }
    });
    return response.data;
  },

  generateReport: async (period: 'weekly' | 'monthly' = 'weekly') => {
    const response = await api.get('/api/progress/report', {
      params: { period }
    });
    return response.data;
  },

  getAchievements: async (days: number = 7) => {
    const response = await api.get('/api/progress/achievements', {
      params: { days }
    });
    return response.data;
  },
};

export const scheduleAPI = {
  getSchedules: async (timeframe?: string) => {
    const response = await api.get('/api/schedule/', {
      params: timeframe ? { timeframe } : {}
    });
    return response.data;
  },

  createSchedule: async (scheduleData: any) => {
    const response = await api.post('/api/schedule/', scheduleData);
    return response.data;
  },

  updateSchedule: async (scheduleId: string, updates: any) => {
    const response = await api.put(`/api/schedule/${scheduleId}`, updates);
    return response.data;
  },

  generateSchedule: async (timeframe: string, preferences: any = {}) => {
    const response = await api.post('/api/schedule/generate', {
      timeframe,
      preferences
    });
    return response.data;
  },

  getAlternatives: async (scheduleId: string) => {
    const response = await api.get(`/api/schedule/${scheduleId}/alternatives`);
    return response.data;
  },

  getUserSchedules: async () => {
    const response = await api.get('/api/schedule/');
    return response.data;
  },

  getSchedule: async (scheduleId: string) => {
    const response = await api.get(`/api/schedule/${scheduleId}`);
    return response.data;
  },
};

export const reminderAPI = {
  getReminders: async () => {
    const response = await api.get('/api/reminders/');
    return response.data;
  },

  createReminder: async (reminderData: any) => {
    const response = await api.post('/api/reminders/', reminderData);
    return response.data;
  },

  updateReminder: async (reminderId: string, updates: any) => {
    const response = await api.put(`/api/reminders/${reminderId}`, updates);
    return response.data;
  },

  scheduleReminder: async (reminderData: any) => {
    const response = await api.post('/api/reminders/schedule', reminderData);
    return response.data;
  },
};

// WebSocket connection management
export class WebSocketService {
  private ws: WebSocket | null = null;
  private userId: string | null = null;
  private token: string | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(userId: string, token: string) {
    this.userId = userId;
    this.token = token;
    this.createConnection();
  }

  private createConnection() {
    if (!this.userId || !this.token) return;

    const wsUrl = `ws://localhost:8000/ws/${this.userId}?token=${this.token}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private handleMessage(message: any) {
    // Dispatch custom events for different message types
    const event = new CustomEvent('websocket-message', { detail: message });
    window.dispatchEvent(event);

    // Handle specific message types
    switch (message.type) {
      case 'schedule_update':
        window.dispatchEvent(new CustomEvent('schedule-updated', { detail: message.data }));
        break;
      case 'progress_update':
        window.dispatchEvent(new CustomEvent('progress-updated', { detail: message.data }));
        break;
      case 'reminder':
        window.dispatchEvent(new CustomEvent('reminder-received', { detail: message.data }));
        break;
      case 'achievement':
        window.dispatchEvent(new CustomEvent('achievement-unlocked', { detail: message.data }));
        break;
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.createConnection();
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  requestUpdate(updateType: string) {
    this.send({
      type: 'request_update',
      update_type: updateType,
      timestamp: new Date().toISOString()
    });
  }
}

export const webSocketService = new WebSocketService();

export default api;