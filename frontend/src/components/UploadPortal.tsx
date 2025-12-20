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
  CircularProgress,
  Avatar,
  Divider,
  LinearProgress,
  Fade,
  Collapse
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import MicIcon from '@mui/icons-material/Mic';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { uploadAPI } from '../services/api';

const UploadPortal: React.FC = () => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [textInput, setTextInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [lastUploadResult, setLastUploadResult] = useState<any>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showResults, setShowResults] = useState(false);

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
    if (!isRecording) {
      setUploadStatus('🎤 Voice recording started...');
    } else {
      setUploadStatus('✅ Voice recording stopped');
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setUploadProgress(0);
    setUploadStatus('🚀 Processing your data...');
    
    try {
      const results = [];
      const totalItems = selectedFiles.length + (textInput.trim() ? 1 : 0);
      let completed = 0;
      
      // Upload files
      for (const file of selectedFiles) {
        const result = await uploadAPI.uploadDocument(file);
        results.push(result);
        completed++;
        setUploadProgress((completed / totalItems) * 100);
      }
      
      // Upload text if provided
      if (textInput.trim()) {
        const result = await uploadAPI.uploadText(textInput.trim());
        results.push(result);
        completed++;
        setUploadProgress(100);
      }
      
      setLastUploadResult(results);
      setUploadStatus(`🎉 Successfully processed ${results.length} item(s)!`);
      setShowResults(true);
      setSelectedFiles([]);
      setTextInput('');
      
    } catch (error: any) {
      console.error('Upload error:', error);
      setUploadStatus(`❌ Error: ${error.response?.data?.detail || 'Upload failed'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf': return '📄';
      case 'txt': return '📝';
      case 'docx': return '📘';
      default: return '📎';
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          p: 4,
          borderRadius: 3,
          mb: 4,
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Box sx={{ position: 'relative', zIndex: 2 }}>
          <Typography variant="h3" fontWeight={700} gutterBottom>
            Train Your AI Assistant
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9, mb: 2, maxWidth: 600 }}>
            Upload your routines, goals, and visions to create a personalized scheduling experience
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip 
              icon={<SmartToyIcon />} 
              label="AI-Powered Analysis" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
            <Chip 
              label="Secure Processing" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
            <Chip 
              label="Instant Results" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
          </Box>
        </Box>
      </Box>

      {/* Upload Progress */}
      {isLoading && (
        <Fade in={isLoading}>
          <Paper sx={{ p: 3, mb: 4, bgcolor: 'primary.50' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <CircularProgress size={24} sx={{ mr: 2 }} />
              <Typography variant="h6" color="primary">
                Processing Your Data
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={uploadProgress} 
              sx={{ height: 8, borderRadius: 4, mb: 1 }}
            />
            <Typography variant="body2" color="text.secondary">
              {uploadProgress.toFixed(0)}% Complete
            </Typography>
          </Paper>
        </Fade>
      )}

      <Grid container spacing={4}>
        {/* File Upload */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', position: 'relative' }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2, width: 48, height: 48 }}>
                  <CloudUploadIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Upload Documents
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    PDF, TXT, DOCX files supported
                  </Typography>
                </Box>
              </Box>
              
              <Paper
                sx={{
                  p: 4,
                  border: '2px dashed',
                  borderColor: selectedFiles.length > 0 ? 'success.main' : 'grey.300',
                  textAlign: 'center',
                  cursor: 'pointer',
                  bgcolor: selectedFiles.length > 0 ? 'success.50' : 'grey.50',
                  transition: 'all 0.3s ease',
                  '&:hover': { 
                    borderColor: 'primary.main',
                    bgcolor: 'primary.50'
                  }
                }}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <CloudUploadIcon 
                  sx={{ 
                    fontSize: 64, 
                    color: selectedFiles.length > 0 ? 'success.main' : 'text.secondary',
                    mb: 2 
                  }} 
                />
                <Typography variant="h6" gutterBottom>
                  {selectedFiles.length > 0 ? 'Files Ready!' : 'Drop files here'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  or click to browse your computer
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
                <Box sx={{ mt: 3 }}>
                  <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                    Selected Files ({selectedFiles.length}):
                  </Typography>
                  <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
                    {selectedFiles.map((file, index) => (
                      <Box 
                        key={index}
                        sx={{ 
                          display: 'flex', 
                          alignItems: 'center', 
                          p: 2, 
                          mb: 1,
                          bgcolor: 'grey.50',
                          borderRadius: 2,
                          border: '1px solid',
                          borderColor: 'grey.200'
                        }}
                      >
                        <Typography sx={{ mr: 1, fontSize: '1.2rem' }}>
                          {getFileIcon(file.name)}
                        </Typography>
                        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                          <Typography variant="body2" fontWeight={500} noWrap>
                            {file.name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {(file.size / 1024).toFixed(1)} KB
                          </Typography>
                        </Box>
                        <Button
                          size="small"
                          color="error"
                          onClick={(e) => {
                            e.stopPropagation();
                            removeFile(index);
                          }}
                        >
                          <DeleteOutlineIcon fontSize="small" />
                        </Button>
                      </Box>
                    ))}
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Voice & Text Input */}
        <Grid item xs={12} md={6}>
          <Grid container spacing={3} sx={{ height: '100%' }}>
            {/* Voice Input */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 4, textAlign: 'center' }}>
                  <Avatar sx={{ bgcolor: 'info.main', mx: 'auto', mb: 2, width: 48, height: 48 }}>
                    <MicIcon />
                  </Avatar>
                  <Typography variant="h6" fontWeight={600} gutterBottom>
                    Voice Input
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Record your goals, routines, and visions
                  </Typography>
                  
                  <Button
                    variant={isRecording ? "contained" : "outlined"}
                    color={isRecording ? "error" : "info"}
                    size="large"
                    onClick={handleVoiceRecording}
                    startIcon={<MicIcon />}
                    sx={{ 
                      minWidth: 160,
                      py: 1.5,
                      borderRadius: 3,
                      fontWeight: 600
                    }}
                  >
                    {isRecording ? 'Stop Recording' : 'Start Recording'}
                  </Button>
                  
                  {isRecording && (
                    <Box sx={{ mt: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, mb: 1 }}>
                        {[1, 2, 3, 4].map((i) => (
                          <Box
                            key={i}
                            sx={{
                              width: 4,
                              height: 20,
                              bgcolor: 'error.main',
                              borderRadius: 2,
                              animation: `pulse 1s ease-in-out ${i * 0.1}s infinite alternate`
                            }}
                          />
                        ))}
                      </Box>
                      <Typography variant="caption" color="error">
                        Recording in progress...
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Text Input */}
            <Grid item xs={12}>
              <Card sx={{ height: '100%' }}>
                <CardContent sx={{ p: 4, height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'success.main', mr: 2, width: 40, height: 40 }}>
                      <TextFieldsIcon />
                    </Avatar>
                    <Typography variant="h6" fontWeight={600}>
                      Text Input
                    </Typography>
                  </Box>
                  
                  <TextField
                    fullWidth
                    multiline
                    rows={6}
                    placeholder="Describe your daily routines, goals, and visions here..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    variant="outlined"
                    sx={{ 
                      flexGrow: 1,
                      '& .MuiOutlinedInput-root': {
                        height: '100%',
                        alignItems: 'flex-start'
                      }
                    }}
                  />
                  
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                    {textInput.length} characters
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>

        {/* Submit Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 4, textAlign: 'center', bgcolor: 'grey.50' }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleSubmit}
              disabled={isLoading || (selectedFiles.length === 0 && !textInput.trim())}
              startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <SmartToyIcon />}
              sx={{ 
                minWidth: 200,
                py: 2,
                px: 4,
                borderRadius: 3,
                fontSize: '1.1rem',
                fontWeight: 600,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)'
                }
              }}
            >
              {isLoading ? 'Processing...' : 'Train AI Assistant'}
            </Button>
            
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              Your data will be analyzed and used to personalize your scheduling experience
            </Typography>
          </Paper>
          
          {uploadStatus && (
            <Fade in={!!uploadStatus}>
              <Alert 
                severity={uploadStatus.includes('❌') ? 'error' : 'success'} 
                sx={{ mt: 2, borderRadius: 2 }}
                icon={uploadStatus.includes('🎉') ? <CheckCircleIcon /> : undefined}
              >
                {uploadStatus}
              </Alert>
            </Fade>
          )}
        </Grid>

        {/* Results Section */}
        <Grid item xs={12}>
          <Collapse in={showResults && lastUploadResult && lastUploadResult.length > 0}>
            <Paper sx={{ p: 4, bgcolor: 'success.50', border: '1px solid', borderColor: 'success.200' }}>
              <Typography variant="h6" fontWeight={600} gutterBottom color="success.dark">
                🎯 Processing Results
              </Typography>
              <Divider sx={{ mb: 3 }} />
              
              <Grid container spacing={2}>
                {lastUploadResult?.map((result: any, index: number) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Card sx={{ bgcolor: 'white' }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Chip 
                            label={result.data.category} 
                            color="primary" 
                            sx={{ fontWeight: 600 }}
                          />
                          <Box sx={{ ml: 'auto' }}>
                            <Typography variant="body2" color="success.main" fontWeight={600}>
                              {(result.data.confidence * 100).toFixed(1)}% confidence
                            </Typography>
                          </Box>
                        </Box>
                        
                        {result.data.extracted_items && (
                          <Box>
                            {Object.entries(result.data.extracted_items).map(([key, items]: [string, any]) => (
                              items.length > 0 && (
                                <Typography key={key} variant="body2" sx={{ mb: 1 }}>
                                  <strong>{key}:</strong> {items.length} item(s) extracted
                                </Typography>
                              )
                            ))}
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Collapse>
        </Grid>
      </Grid>
    </Box>
  );
};

export default UploadPortal;