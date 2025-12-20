import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  TextField,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import MicIcon from '@mui/icons-material/Mic';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import { uploadAPI } from '../services/api';

const UploadPortal: React.FC = () => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [textInput, setTextInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [lastUploadResult, setLastUploadResult] = useState<any>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleVoiceRecording = () => {
    setIsRecording(!isRecording);
    // TODO: Implement voice recording functionality
    if (!isRecording) {
      setUploadStatus('Voice recording started...');
    } else {
      setUploadStatus('Voice recording stopped');
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setUploadStatus('Processing uploads...');
    
    try {
      const results = [];
      
      // Upload files
      for (const file of selectedFiles) {
        const result = await uploadAPI.uploadDocument(file);
        results.push(result);
      }
      
      // Upload text if provided
      if (textInput.trim()) {
        const result = await uploadAPI.uploadText(textInput.trim());
        results.push(result);
      }
      
      setLastUploadResult(results);
      setUploadStatus(`Successfully processed ${results.length} item(s)!`);
      setSelectedFiles([]);
      setTextInput('');
      
    } catch (error: any) {
      console.error('Upload error:', error);
      setUploadStatus(`Error: ${error.response?.data?.detail || 'Upload failed'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Upload Your Data
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Share your routines, goals, and visions to personalize your AI assistant
      </Typography>

      <Grid container spacing={3}>
        {/* File Upload */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <CloudUploadIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Upload Documents
              </Typography>
              
              <Paper
                sx={{
                  p: 3,
                  border: '2px dashed #ccc',
                  textAlign: 'center',
                  cursor: 'pointer',
                  '&:hover': { borderColor: 'primary.main' }
                }}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <CloudUploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="body1" gutterBottom>
                  Drag and drop files here or click to browse
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Supports PDF, TXT, DOCX files
                </Typography>
              </Paper>
              
              <input
                id="file-input"
                type="file"
                multiple
                accept=".pdf,.txt,.docx"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
              />

              {selectedFiles.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Selected Files:
                  </Typography>
                  {selectedFiles.map((file, index) => (
                    <Chip
                      key={index}
                      label={file.name}
                      onDelete={() => removeFile(index)}
                      sx={{ mr: 1, mb: 1 }}
                    />
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Voice Input */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <MicIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Voice Input
              </Typography>
              
              <Box textAlign="center" py={3}>
                <Button
                  variant={isRecording ? "contained" : "outlined"}
                  color={isRecording ? "error" : "primary"}
                  size="large"
                  onClick={handleVoiceRecording}
                  startIcon={<MicIcon />}
                >
                  {isRecording ? 'Stop Recording' : 'Start Recording'}
                </Button>
                <Typography variant="body2" color="text.secondary" mt={2}>
                  Record your goals, routines, and visions
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Text Input */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TextFieldsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Text Input
              </Typography>
              
              <TextField
                fullWidth
                multiline
                rows={6}
                placeholder="Describe your daily routines, goals, and visions here..."
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                variant="outlined"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Submit */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="center" gap={2}>
            <Button
              variant="contained"
              size="large"
              onClick={handleSubmit}
              disabled={isLoading || (selectedFiles.length === 0 && !textInput.trim())}
              startIcon={isLoading ? <CircularProgress size={20} /> : undefined}
            >
              {isLoading ? 'Processing...' : 'Process Data'}
            </Button>
          </Box>
          
          {uploadStatus && (
            <Alert 
              severity={uploadStatus.includes('Error') ? 'error' : 'info'} 
              sx={{ mt: 2 }}
            >
              {uploadStatus}
            </Alert>
          )}
          
          {lastUploadResult && lastUploadResult.length > 0 && (
            <Paper sx={{ mt: 2, p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Processing Results:
              </Typography>
              {lastUploadResult.map((result: any, index: number) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="subtitle2">
                    Category: <Chip label={result.data.category} size="small" />
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Confidence: {(result.data.confidence * 100).toFixed(1)}%
                  </Typography>
                  {result.data.extracted_items && (
                    <Box sx={{ mt: 1 }}>
                      {Object.entries(result.data.extracted_items).map(([key, items]: [string, any]) => (
                        items.length > 0 && (
                          <Typography key={key} variant="body2">
                            {key}: {items.length} item(s)
                          </Typography>
                        )
                      ))}
                    </Box>
                  )}
                </Box>
              ))}
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default UploadPortal;