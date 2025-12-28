/**
 * Schedule slice for PWA
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ScheduleState {
  events: any[];
  loading: boolean;
  error: string | null;
}

const initialState: ScheduleState = {
  events: [],
  loading: false,
  error: null,
};

const scheduleSlice = createSlice({
  name: 'schedule',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setEvents: (state, action: PayloadAction<any[]>) => {
      state.events = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setLoading, setEvents, setError } = scheduleSlice.actions;
export default scheduleSlice.reducer;