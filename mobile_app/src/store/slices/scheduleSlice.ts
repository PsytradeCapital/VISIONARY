/**
 * Schedule state management with real API integration
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { scheduleAPI } from '../../services/api';

interface ScheduleBlock {
  id: string;
  title: string;
  description?: string;
  startTime: string;
  endTime: string;
  category: string;
  priority: number;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  location?: string;
  tags: string[];
}

interface Schedule {
  id: string;
  blocks: ScheduleBlock[];
  timeframe: 'daily' | 'weekly' | 'monthly';
  generatedAt: string;
  userId: string;
  preferences: any;
}

interface ScheduleState {
  currentSchedule: Schedule | null;
  schedules: Schedule[];
  loading: boolean;
  error: string | null;
  lastGenerated: string | null;
}

const initialState: ScheduleState = {
  currentSchedule: null,
  schedules: [],
  loading: false,
  error: null,
  lastGenerated: null,
};

// Async thunks with real API integration
export const generateSchedule = createAsyncThunk(
  'schedule/generate',
  async (request: { 
    timeframe: 'daily' | 'weekly' | 'monthly'; 
    startDate: string; 
    preferences?: any;
    goals?: string[];
  }, { rejectWithValue }) => {
    try {
      const response = await scheduleAPI.generate(request);
      
      if (response.data?.success) {
        return {
          id: response.data.schedule_id,
          blocks: response.data.blocks,
          timeframe: request.timeframe,
          generatedAt: response.data.generated_at,
          userId: response.data.user_id,
          preferences: request.preferences,
        };
      } else {
        throw new Error(response.data?.message || 'Schedule generation failed');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Schedule generation failed');
    }
  }
);

export const getSchedule = createAsyncThunk(
  'schedule/get',
  async (scheduleId: string, { rejectWithValue }) => {
    try {
      const response = await scheduleAPI.get(scheduleId);
      
      if (response.data?.success) {
        return response.data.schedule;
      } else {
        throw new Error(response.data?.message || 'Failed to fetch schedule');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Failed to fetch schedule');
    }
  }
);

export const updateSchedule = createAsyncThunk(
  'schedule/update',
  async (params: { scheduleId: string; updates: any }, { rejectWithValue }) => {
    try {
      const response = await scheduleAPI.update(params.scheduleId, params.updates);
      
      if (response.data?.success) {
        return {
          scheduleId: params.scheduleId,
          updates: params.updates,
          updatedAt: new Date().toISOString(),
        };
      } else {
        throw new Error(response.data?.message || 'Failed to update schedule');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Failed to update schedule');
    }
  }
);

export const updateScheduleBlock = createAsyncThunk(
  'schedule/updateBlock',
  async (params: { 
    scheduleId: string; 
    blockId: string; 
    updates: Partial<ScheduleBlock> 
  }, { rejectWithValue }) => {
    try {
      const response = await scheduleAPI.update(params.scheduleId, {
        block_id: params.blockId,
        block_updates: params.updates,
      });
      
      if (response.data?.success) {
        return {
          scheduleId: params.scheduleId,
          blockId: params.blockId,
          updates: params.updates,
        };
      } else {
        throw new Error(response.data?.message || 'Failed to update schedule block');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Failed to update schedule block');
    }
  }
);

const scheduleSlice = createSlice({
  name: 'schedule',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentSchedule: (state, action: PayloadAction<Schedule>) => {
      state.currentSchedule = action.payload;
    },
    updateBlockStatus: (state, action: PayloadAction<{ blockId: string; status: ScheduleBlock['status'] }>) => {
      if (state.currentSchedule) {
        const block = state.currentSchedule.blocks.find(b => b.id === action.payload.blockId);
        if (block) {
          block.status = action.payload.status;
        }
      }
    },
    addScheduleToHistory: (state, action: PayloadAction<Schedule>) => {
      state.schedules.unshift(action.payload);
      // Keep only last 10 schedules
      if (state.schedules.length > 10) {
        state.schedules = state.schedules.slice(0, 10);
      }
    },
  },
  extraReducers: (builder) => {
    // Generate schedule
    builder
      .addCase(generateSchedule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(generateSchedule.fulfilled, (state, action) => {
        state.loading = false;
        state.currentSchedule = action.payload;
        state.lastGenerated = new Date().toISOString();
        state.schedules.unshift(action.payload);
        if (state.schedules.length > 10) {
          state.schedules = state.schedules.slice(0, 10);
        }
        state.error = null;
      })
      .addCase(generateSchedule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      
      // Get schedule
      .addCase(getSchedule.pending, (state) => {
        state.loading = true;
      })
      .addCase(getSchedule.fulfilled, (state, action) => {
        state.loading = false;
        state.currentSchedule = action.payload;
      })
      .addCase(getSchedule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      
      // Update schedule
      .addCase(updateSchedule.fulfilled, (state, action) => {
        if (state.currentSchedule && state.currentSchedule.id === action.payload.scheduleId) {
          // Apply updates to current schedule
          state.currentSchedule = { ...state.currentSchedule, ...action.payload.updates };
        }
      })
      
      // Update schedule block
      .addCase(updateScheduleBlock.fulfilled, (state, action) => {
        if (state.currentSchedule && state.currentSchedule.id === action.payload.scheduleId) {
          const block = state.currentSchedule.blocks.find(b => b.id === action.payload.blockId);
          if (block) {
            Object.assign(block, action.payload.updates);
          }
        }
      });
  },
});

export const { 
  clearError, 
  setCurrentSchedule, 
  updateBlockStatus, 
  addScheduleToHistory 
} = scheduleSlice.actions;

export default scheduleSlice.reducer;