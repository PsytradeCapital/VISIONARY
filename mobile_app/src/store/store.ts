/**
 * Redux store configuration for mobile app
 */

import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import scheduleSlice from './slices/scheduleSlice';
import uploadSlice from './slices/uploadSlice';
import analyticsSlice from './slices/analyticsSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    schedule: scheduleSlice,
    upload: uploadSlice,
    analytics: analyticsSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;