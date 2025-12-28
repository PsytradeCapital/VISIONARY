/**
 * Upload slice for PWA
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UploadState {
  uploading: boolean;
  progress: number;
  error: string | null;
}

const initialState: UploadState = {
  uploading: false,
  progress: 0,
  error: null,
};

const uploadSlice = createSlice({
  name: 'upload',
  initialState,
  reducers: {
    startUpload: (state) => {
      state.uploading = true;
      state.progress = 0;
      state.error = null;
    },
    updateProgress: (state, action: PayloadAction<number>) => {
      state.progress = action.payload;
    },
    uploadSuccess: (state) => {
      state.uploading = false;
      state.progress = 100;
      state.error = null;
    },
    uploadError: (state, action: PayloadAction<string>) => {
      state.uploading = false;
      state.error = action.payload;
    },
  },
});

export const { startUpload, updateProgress, uploadSuccess, uploadError } = uploadSlice.actions;
export default uploadSlice.reducer;