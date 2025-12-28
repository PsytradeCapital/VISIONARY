/**
 * Authentication slice for PWA
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
}

const initialState: AuthState = {
  isAuthenticated: !!localStorage.getItem('auth_token'),
  user: localStorage.getItem('user_data') ? JSON.parse(localStorage.getItem('user_data')!) : null,
  token: localStorage.getItem('auth_token'),
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action: PayloadAction<{ user: any; token: string }>) => {
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.token = action.payload.token;
      localStorage.setItem('auth_token', action.payload.token);
      localStorage.setItem('user_data', JSON.stringify(action.payload.user));
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_data');
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;