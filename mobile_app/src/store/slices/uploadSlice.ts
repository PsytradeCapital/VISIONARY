/**
 * Upload state management with real API integration
 * Task 10.2: Mobile-optimized upload portal with multi-modal input
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { uploadAPI } from '../../services/api';

interface FileUpload {
  uri: string;
  name: string;
  type: string;
  size: number;
}

interface VoiceUpload {
  uri: string;
  duration: number;
  transcription?: string;
}

interface TextUpload {
  content: string;
  type: 'manual_input' | 'voice_transcription';
}

interface UploadResult {
  id: string;
  type: 'file' | 'voice' | 'text';
  status: 'processing' | 'completed' | 'failed';
  category?: string;
  extractedItems?: any;
  confidence?: number;
  createdAt: string;
}

interface UploadState {
  uploading: boolean;
  progress: number;
  error: string | null;
  recentUploads: UploadResult[];
  currentUpload: UploadResult | null;
}

const initialState: UploadState = {
  uploading: false,
  progress: 0,
  error: null,
  recentUploads: [],
  currentUpload: null,
};

// Async thunks for real API integration
export const uploadFile = createAsyncThunk(
  'upload/file',
  async (file: FileUpload, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: file.uri,
        name: file.name,
        type: file.type,
      } as any);

      const response = await uploadAPI.uploadDocument(formData);
      
      if (response.data?.success) {
        return {
          id: response.data.id,
          type: 'file' as const,
          status: 'completed' as const,
          category: response.data.category,
          extractedItems: response.data.extracted_items,
          confidence: response.data.confidence,
          createdAt: new Date().toISOString(),
          originalFile: file,
        };
      } else {
        throw new Error(response.data?.message || 'Upload failed');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'File upload failed');
    }
  }
);

export const uploadVoice = createAsyncThunk(
  'upload/voice',
  async (voice: VoiceUpload, { rejectWithValue }) => {
    try {
      // Create audio blob from URI
      const response = await fetch(voice.uri);
      const audioBlob = await response.blob();

      const apiResponse = await uploadAPI.uploadVoice(audioBlob);
      
      if (apiResponse.data?.success) {
        return {
          id: apiResponse.data.id,
          type: 'voice' as const,
          status: 'completed' as const,
          category: apiResponse.data.category,
          extractedItems: apiResponse.data.extracted_items,
          confidence: apiResponse.data.confidence,
          transcription: apiResponse.data.transcribed_text,
          duration: voice.duration,
          createdAt: new Date().toISOString(),
        };
      } else {
        throw new Error(apiResponse.data?.message || 'Voice upload failed');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Voice upload failed');
    }
  }
);

export const uploadText = createAsyncThunk(
  'upload/text',
  async (text: TextUpload, { rejectWithValue }) => {
    try {
      const response = await uploadAPI.uploadText(text.content);
      
      if (response.data?.success) {
        return {
          id: response.data.id,
          type: 'text' as const,
          status: 'completed' as const,
          category: response.data.category,
          extractedItems: response.data.extracted_items,
          confidence: response.data.confidence,
          content: text.content,
          inputType: text.type,
          createdAt: new Date().toISOString(),
        };
      } else {
        throw new Error(response.data?.message || 'Text upload failed');
      }
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || error.message || 'Text upload failed');
    }
  }
);

const uploadSlice = createSlice({
  name: 'upload',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setProgress: (state, action: PayloadAction<number>) => {
      state.progress = action.payload;
    },
    clearCurrentUpload: (state) => {
      state.currentUpload = null;
    },
    removeUpload: (state, action: PayloadAction<string>) => {
      state.recentUploads = state.recentUploads.filter(upload => upload.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    // File upload
    builder
      .addCase(uploadFile.pending, (state) => {
        state.uploading = true;
        state.error = null;
        state.progress = 0;
      })
      .addCase(uploadFile.fulfilled, (state, action) => {
        state.uploading = false;
        state.progress = 100;
        state.currentUpload = action.payload;
        state.recentUploads.unshift(action.payload);
        // Keep only last 20 uploads
        if (state.recentUploads.length > 20) {
          state.recentUploads = state.recentUploads.slice(0, 20);
        }
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.uploading = false;
        state.error = action.payload as string;
        state.progress = 0;
      })
      
      // Voice upload
      .addCase(uploadVoice.pending, (state) => {
        state.uploading = true;
        state.error = null;
        state.progress = 0;
      })
      .addCase(uploadVoice.fulfilled, (state, action) => {
        state.uploading = false;
        state.progress = 100;
        state.currentUpload = action.payload;
        state.recentUploads.unshift(action.payload);
        if (state.recentUploads.length > 20) {
          state.recentUploads = state.recentUploads.slice(0, 20);
        }
      })
      .addCase(uploadVoice.rejected, (state, action) => {
        state.uploading = false;
        state.error = action.payload as string;
        state.progress = 0;
      })
      
      // Text upload
      .addCase(uploadText.pending, (state) => {
        state.uploading = true;
        state.error = null;
        state.progress = 0;
      })
      .addCase(uploadText.fulfilled, (state, action) => {
        state.uploading = false;
        state.progress = 100;
        state.currentUpload = action.payload;
        state.recentUploads.unshift(action.payload);
        if (state.recentUploads.length > 20) {
          state.recentUploads = state.recentUploads.slice(0, 20);
        }
      })
      .addCase(uploadText.rejected, (state, action) => {
        state.uploading = false;
        state.error = action.payload as string;
        state.progress = 0;
      });
  },
});

export const { clearError, setProgress, clearCurrentUpload, removeUpload } = uploadSlice.actions;
export default uploadSlice.reducer;