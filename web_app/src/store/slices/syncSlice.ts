/**
 * Sync state management for PWA offline functionality
 * Task 11.2: Mobile-web synchronization with cloud backend
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface PendingAction {
  id: string;
  type: 'upload' | 'schedule_update' | 'progress_update' | 'auth_refresh';
  data: any;
  timestamp: string;
  retryCount: number;
  maxRetries: number;
}

interface SyncState {
  isOnline: boolean;
  pendingActions: PendingAction[];
  lastSyncTime: string | null;
  syncing: boolean;
  syncError: string | null;
  autoSyncEnabled: boolean;
  syncInterval: number; // in milliseconds
}

const initialState: SyncState = {
  isOnline: navigator.onLine,
  pendingActions: [],
  lastSyncTime: localStorage.getItem('lastSyncTime'),
  syncing: false,
  syncError: null,
  autoSyncEnabled: true,
  syncInterval: 30000, // 30 seconds
};

// Async thunks for background sync
export const syncPendingActions = createAsyncThunk(
  'sync/syncPending',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { sync: SyncState };
      const { pendingActions } = state.sync;

      if (pendingActions.length === 0) {
        return { syncedCount: 0, failedCount: 0, results: [] };
      }

      // Process each pending action
      const results = [];
      for (const action of pendingActions) {
        try {
          let apiResponse;
          
          switch (action.type) {
            case 'upload':
              // Simulate API call - in real implementation, use actual API
              apiResponse = await fetch('/api/v1/upload/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(action.data),
              });
              break;
              
            case 'schedule_update':
              apiResponse = await fetch(`/api/v1/schedule/${action.data.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(action.data.updates),
              });
              break;
              
            case 'progress_update':
              apiResponse = await fetch('/api/v1/analytics/progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(action.data),
              });
              break;
              
            case 'auth_refresh':
              apiResponse = await fetch('/api/v1/auth/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(action.data),
              });
              break;
          }

          if (apiResponse && apiResponse.ok) {
            results.push({ id: action.id, success: true });
          } else {
            throw new Error(`API call failed: ${apiResponse?.status}`);
          }
        } catch (error) {
          results.push({ 
            id: action.id, 
            success: false, 
            error: error instanceof Error ? error.message : 'Unknown error'
          });
        }
      }

      return {
        syncedCount: results.filter(r => r.success).length,
        failedCount: results.filter(r => !r.success).length,
        results,
      };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Sync failed');
    }
  }
);

export const performBackgroundSync = createAsyncThunk(
  'sync/backgroundSync',
  async (_, { dispatch, getState }) => {
    const state = getState() as { sync: SyncState };
    
    if (!state.sync.isOnline || state.sync.syncing) {
      return { skipped: true, reason: 'offline or already syncing' };
    }

    // Perform sync
    const result = await dispatch(syncPendingActions());
    
    return {
      skipped: false,
      result: result.payload,
      timestamp: new Date().toISOString(),
    };
  }
);

const syncSlice = createSlice({
  name: 'sync',
  initialState,
  reducers: {
    setOnlineStatus: (state, action: PayloadAction<boolean>) => {
      state.isOnline = action.payload;
      
      // If coming back online, trigger sync
      if (action.payload && state.pendingActions.length > 0 && state.autoSyncEnabled) {
        // This would trigger background sync in the component
      }
    },
    
    addPendingAction: (state, action: PayloadAction<Omit<PendingAction, 'id' | 'timestamp' | 'retryCount'>>) => {
      const pendingAction: PendingAction = {
        ...action.payload,
        id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date().toISOString(),
        retryCount: 0,
        maxRetries: action.payload.maxRetries || 3,
      };
      
      state.pendingActions.push(pendingAction);
      
      // Store in localStorage for persistence
      localStorage.setItem('pendingActions', JSON.stringify(state.pendingActions));
    },
    
    removePendingAction: (state, action: PayloadAction<string>) => {
      state.pendingActions = state.pendingActions.filter(pendingAction => pendingAction.id !== action.payload);
      localStorage.setItem('pendingActions', JSON.stringify(state.pendingActions));
    },
    
    clearPendingActions: (state) => {
      state.pendingActions = [];
      localStorage.removeItem('pendingActions');
    },
    
    incrementRetryCount: (state, action: PayloadAction<string>) => {
      const actionItem = state.pendingActions.find(a => a.id === action.payload);
      if (actionItem) {
        actionItem.retryCount += 1;
      }
    },
    
    setAutoSync: (state, action: PayloadAction<boolean>) => {
      state.autoSyncEnabled = action.payload;
      localStorage.setItem('autoSyncEnabled', action.payload.toString());
    },
    
    setSyncInterval: (state, action: PayloadAction<number>) => {
      state.syncInterval = action.payload;
      localStorage.setItem('syncInterval', action.payload.toString());
    },
    
    loadPersistedState: (state) => {
      // Load persisted pending actions
      const storedActions = localStorage.getItem('pendingActions');
      if (storedActions) {
        try {
          state.pendingActions = JSON.parse(storedActions);
        } catch (error) {
          console.error('Failed to parse stored pending actions:', error);
        }
      }
      
      // Load other persisted settings
      const autoSync = localStorage.getItem('autoSyncEnabled');
      if (autoSync !== null) {
        state.autoSyncEnabled = autoSync === 'true';
      }
      
      const syncInterval = localStorage.getItem('syncInterval');
      if (syncInterval) {
        state.syncInterval = parseInt(syncInterval, 10);
      }
    },
    
    clearSyncError: (state) => {
      state.syncError = null;
    },
  },
  
  extraReducers: (builder) => {
    // Sync pending actions
    builder
      .addCase(syncPendingActions.pending, (state) => {
        state.syncing = true;
        state.syncError = null;
      })
      .addCase(syncPendingActions.fulfilled, (state, action) => {
        state.syncing = false;
        state.lastSyncTime = new Date().toISOString();
        
        // Remove successfully synced actions
        const { results } = action.payload;
        const successfulIds = results.filter(r => r.success).map(r => r.id);
        state.pendingActions = state.pendingActions.filter(
          action => !successfulIds.includes(action.id)
        );
        
        // Increment retry count for failed actions
        const failedIds = results.filter(r => !r.success).map(r => r.id);
        state.pendingActions.forEach(action => {
          if (failedIds.includes(action.id)) {
            action.retryCount += 1;
          }
        });
        
        // Remove actions that exceeded max retries
        state.pendingActions = state.pendingActions.filter(
          action => action.retryCount < action.maxRetries
        );
        
        // Update localStorage
        localStorage.setItem('pendingActions', JSON.stringify(state.pendingActions));
        localStorage.setItem('lastSyncTime', state.lastSyncTime);
      })
      .addCase(syncPendingActions.rejected, (state, action) => {
        state.syncing = false;
        state.syncError = action.payload as string;
      })
      
      // Background sync
      .addCase(performBackgroundSync.fulfilled, (state, action) => {
        if (!action.payload.skipped) {
          state.lastSyncTime = action.payload.timestamp;
          localStorage.setItem('lastSyncTime', state.lastSyncTime);
        }
      });
  },
});

export const {
  setOnlineStatus,
  addPendingAction,
  removePendingAction,
  clearPendingActions,
  incrementRetryCount,
  setAutoSync,
  setSyncInterval,
  loadPersistedState,
  clearSyncError,
} = syncSlice.actions;

export default syncSlice.reducer;