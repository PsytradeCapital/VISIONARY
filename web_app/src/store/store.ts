/**
 * Redux store configuration for PWA
 * Task 11.2: Mobile-web synchronization with cloud backend
 */

import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import uploadSlice from './slices/uploadSlice';
import scheduleSlice from './slices/scheduleSlice';
import analyticsSlice from './slices/analyticsSlice';
import syncSlice from './slices/syncSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    upload: uploadSlice,
    schedule: scheduleSlice,
    analytics: analyticsSlice,
    sync: syncSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'sync/queueAction'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;