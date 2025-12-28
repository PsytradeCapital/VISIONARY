/**
 * Analytics state management with real API integration
 * Task 10.4: Photorealistic progress visualization with interactive charts
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { analyticsAPI } from '../../services/api';

interface ProgressMetrics {
  healthProgress: number;
  nutritionProgress: number;
  financialProgress: number;
  productivityScore: number;
  goalCompletionRate: number;
  habitStrength: Record<string, number>;
  weeklyTrends: Record<string, number[]>;
  monthlyTrends: Record<string, number[]>;
}

interface ChartData {
  id: string;
  type: 'line' | 'bar' | 'pie' | 'progress';
  title: string;
  data: any;
  backgroundImage?: string;
  category: 'health' | 'nutrition' | 'financial' | 'productivity';
  timeframe: 'daily' | 'weekly' | 'monthly' | 'yearly';
}

interface AIInsight {
  id: string;
  type: 'pattern' | 'recommendation' | 'achievement' | 'warning';
  title: string;
  description: string;
  confidence: number;
  category: string;
  actionable: boolean;
  createdAt: string;
}

interface AnalyticsState {
  metrics: ProgressMetrics | null;
  charts: ChartData[];
  insights: AIInsight[];
  achievements: any[];
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

const initialState: AnalyticsState = {
  metrics: null,
  charts: [],
  insights: [],
  achievements: [],
  loading: false,
  error: null,
  lastUpdated: null,
};

// Async thunks for real API integration
export const fetchAnalytics = createAsyncThunk(
  'analytics/fetchAnalytics',
  async (params: { period: 'week' | 'month' | 'year' }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getProgress(params.period);
      
      if (response.data?.success) {
        return {
          metrics: response.data.metrics,
          insights: response.data.insights,
          achievements: response.data.achievements,
          lastUpdated: new Date().toISOString(),
        };
      } else {
        throw new Error(response.data?.message || 'Failed to fetch analytics');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Analytics fetch failed');
    }
  }
);

export const fetchProgressCharts = createAsyncThunk(
  'analytics/fetchCharts',
  async (params: { chartType?: string; timeframe?: string }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getCharts(params.chartType);
      
      if (response.data?.success) {
        return response.data.charts;
      } else {
        throw new Error(response.data?.message || 'Failed to fetch charts');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Charts fetch failed');
    }
  }
);

export const generateProgressReport = createAsyncThunk(
  'analytics/generateReport',
  async (params: { reportType: 'daily' | 'weekly' | 'monthly' }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.generateReport(params.reportType);
      
      if (response.data?.success) {
        return {
          report: response.data.report,
          insights: response.data.insights,
          recommendations: response.data.recommendations,
        };
      } else {
        throw new Error(response.data?.message || 'Failed to generate report');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Report generation failed');
    }
  }
);

export const updateProgressMetric = createAsyncThunk(
  'analytics/updateMetric',
  async (params: { category: string; metric: string; value: number }, { rejectWithValue }) => {
    try {
      // This would call a backend endpoint to update a specific metric
      const response = await analyticsAPI.getProgress(); // Placeholder - would be updateMetric API
      
      if (response.data?.success) {
        return {
          category: params.category,
          metric: params.metric,
          value: params.value,
          updatedAt: new Date().toISOString(),
        };
      } else {
        throw new Error('Failed to update metric');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Metric update failed');
    }
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCharts: (state, action: PayloadAction<ChartData[]>) => {
      state.charts = action.payload;
    },
    addInsight: (state, action: PayloadAction<AIInsight>) => {
      state.insights.unshift(action.payload);
      // Keep only last 50 insights
      if (state.insights.length > 50) {
        state.insights = state.insights.slice(0, 50);
      }
    },
    removeInsight: (state, action: PayloadAction<string>) => {
      state.insights = state.insights.filter(insight => insight.id !== action.payload);
    },
    updateMetricLocally: (state, action: PayloadAction<{ category: string; value: number }>) => {
      if (state.metrics) {
        const { category, value } = action.payload;
        switch (category) {
          case 'health':
            state.metrics.healthProgress = value;
            break;
          case 'nutrition':
            state.metrics.nutritionProgress = value;
            break;
          case 'financial':
            state.metrics.financialProgress = value;
            break;
          case 'productivity':
            state.metrics.productivityScore = value;
            break;
        }
      }
    },
  },
  extraReducers: (builder) => {
    // Fetch analytics
    builder
      .addCase(fetchAnalytics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnalytics.fulfilled, (state, action) => {
        state.loading = false;
        state.metrics = action.payload.metrics;
        state.insights = action.payload.insights;
        state.achievements = action.payload.achievements;
        state.lastUpdated = action.payload.lastUpdated;
        state.error = null;
      })
      .addCase(fetchAnalytics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      
      // Fetch charts
      .addCase(fetchProgressCharts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchProgressCharts.fulfilled, (state, action) => {
        state.loading = false;
        state.charts = action.payload;
      })
      .addCase(fetchProgressCharts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      
      // Generate report
      .addCase(generateProgressReport.pending, (state) => {
        state.loading = true;
      })
      .addCase(generateProgressReport.fulfilled, (state, action) => {
        state.loading = false;
        // Add report insights to existing insights
        if (action.payload.insights) {
          state.insights = [...action.payload.insights, ...state.insights].slice(0, 50);
        }
      })
      .addCase(generateProgressReport.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      
      // Update metric
      .addCase(updateProgressMetric.fulfilled, (state, action) => {
        const { category, value } = action.payload;
        if (state.metrics) {
          switch (category) {
            case 'health':
              state.metrics.healthProgress = value;
              break;
            case 'nutrition':
              state.metrics.nutritionProgress = value;
              break;
            case 'financial':
              state.metrics.financialProgress = value;
              break;
            case 'productivity':
              state.metrics.productivityScore = value;
              break;
          }
        }
      });
  },
});

export const { 
  clearError, 
  setCharts, 
  addInsight, 
  removeInsight, 
  updateMetricLocally 
} = analyticsSlice.actions;

export default analyticsSlice.reducer;