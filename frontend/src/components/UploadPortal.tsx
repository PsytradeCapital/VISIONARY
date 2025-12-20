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
      {/* Hero Section with Live Upload Interface Image */}
      <Fade in timeout={800}>
        <Box
          sx={{
            position: 'relative',
            borderRadius: 3,
            mb: 4,
            overflow: 'hidden',
            height: 300
          }}
        >
          {/* Background Image */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundImage: 'url(/images/upload portal.jpeg)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              filter: 'brightness(0.7)',
              transition: 'all 0.3s ease'
            }}
            className="interactive-image"
          />
          
          {/* Gradient Overlay */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%)',
              zIndex: 2
            }}
          />
          
          <Box sx={{ position: 'relative', zIndex: 3, p: 4, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Zoom in timeout={1000}>
              <Typography variant="h3" fontWeight={700} color="white" gutterBottom className="float-animation">
                🚀 AI Training Portal
              </Typography>
            </Zoom>
            <Typography variant="h6" sx={{ color: 'white', opacity: 0.95, mb: 2, maxWidth: 600 }}>
              Upload your routines, goals, and visions to create a personalized AI scheduling experience
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Chip 
                icon={<SmartToyIcon />} 
                label="AI-Powered Analysis" 
                className="sparkle-effect"
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
              <Chip 
                label="Secure Processing" 
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
              <Chip 
                label="Instant Results" 
                className="heartbeat-animation"
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
            </Box>
          </Box>
        </Box>
      </Fade>

      {/* Upload Progress */}
      {isLoading && (
        <Fade in={isLoading}>
          <Paper sx={{ p: 3, mb: 4, bgcolor: 'primary.50', border: '2px solid', borderColor: 'primary.200' }} className="glow">
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <CircularProgress size={24} sx={{ mr: 2 }} className="heartbeat-animation" />
              <Typography variant="h6" color="primary" fontWeight={700}>
                🤖 AI Processing Your Data
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={uploadProgress} 
              sx={{ 
                height: 12, 
                borderRadius: 6, 
                mb: 1,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 6,
                  background: 'linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%)'
                }
              }}
              className="live-chart"
            />
            <Typography variant="body2" color="text.secondary" fontWeight={600}>
              {uploadProgress.toFixed(0)}% Complete - Training AI Model...
            </Typography>
          </Paper>
        </Fade>
      )}

      <Grid container spacing={4}>
        {/* File Upload */}
        <Grid item xs={12} md={6}>
          <Grow in timeout={600}>
            <Card sx={{ height: '100%', position: 'relative' }} className="hover-lift">
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2, width: 56, height: 56 }} className="float-animation">
                    <CloudUploadIcon sx={{ fontSize: 32 }} />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight={700}>
                      📁 Upload Documents
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      PDF, TXT, DOCX files supported
                    </Typography>
                  </Box>
                </Box>
                
                <Paper
                  sx={{
                    p: 4,
                    border: '3px dashed',
                    borderColor: selectedFiles.length > 0 ? 'success.main' : 'grey.300',
                    textAlign: 'center',
                    cursor: 'pointer',
                    bgcolor: selectedFiles.length > 0 ? 'success.50' : 'grey.50',
                    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                    '&:hover': { 
                      borderColor: 'primary.main',
                      bgcolor: 'primary.50',
                      transform: 'scale(1.02)'
                    }
                  }}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('file-input')?.click()}
                  className="clickable-glow"
                >
                  <CloudUploadIcon 
                    sx={{ 
                      fontSize: 80, 
                      color: selectedFiles.length > 0 ? 'success.main' : 'text.secondary',
                      mb: 2 
                    }} 
                    className={selectedFiles.length > 0 ? 'heartbeat-animation' : 'float-animation'}
                  />
                  <Typography variant="h6" gutterBottom fontWeight={700}>
                    {selectedFiles.length > 0 ? '✅ Files Ready!' : '📤 Drop files here'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight={500}>
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
                  <Fade in timeout={500}>
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="subtitle2" gutterBottom fontWeight={700}>
                        📋 Selected Files ({selectedFiles.length}):
                      </Typography>
                      <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
                        {selectedFiles.map((file, index) => (
                          <Zoom in timeout={200 + index * 100} key={index}>
                            <Box 
                              sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                p: 2, 
                                mb: 1,
                                bgcolor: 'grey.50',
                                borderRadius: 2,
                                border: '2px solid',
                                borderColor: 'grey.200',
                                transition: 'all 0.3s ease',
                                '&:hover': {
                                  borderColor: 'primary.main',
                                  bgcolor: 'primary.50',
                                  transform: 'translateX(8px)'
                                }
                              }}
                            >
                              <Typography sx={{ mr: 2, fontSize: '1.5rem' }}>
                                {getFileIcon(file.name)}
                              </Typography>
                              <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                                <Typography variant="body2" fontWeight={600} noWrap>
                                  {file.name}
                                </Typography>
                                <Typography variant="caption" color="text.secondary" fontWeight={500}>
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
                                className="hover-lift"
                                sx={{ minWidth: 'auto', p: 1 }}
                              >
                                <DeleteOutlineIcon fontSize="small" />
                              </Button>
                            </Box>
                          </Zoom>
                        ))}
                      </Box>
                    </Box>
                  </Fade>
                )}
              </CardContent>
            </Card>
          </Grow>
        </Grid>

        {/* Voice & Text Input */}
        <Grid item xs={12} md={6}>
          <Grid container spacing={3} sx={{ height: '100%' }}>
            {/* Voice Input */}
            <Grid item xs={12}>
              <Grow in timeout={800}>
                <Card className="hover-lift">
                  <CardContent sx={{ p: 4, textAlign: 'center' }}>
                    <Avatar sx={{ bgcolor: 'info.main', mx: 'auto', mb: 2, width: 56, height: 56 }} className="float-animation">
                      <MicIcon sx={{ fontSize: 32 }} />
                    </Avatar>
                    <Typography variant="h6" fontWeight={700} gutterBottom>
                      🎤 Voice Input
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph fontWeight={500}>
                      Record your goals, routines, and visions
                    </Typography>
                    
                    <Button
                      variant={isRecording ? "contained" : "outlined"}
                      color={isRecording ? "error" : "info"}
                      size="large"
                      onClick={handleVoiceRecording}
                      startIcon={<MicIcon />}
                      className="flashy-button"
                      sx={{ 
                        minWidth: 180,
                        py: 2,
                        borderRadius: 3,
                        fontWeight: 700,
                        fontSize: '1.1rem',
                        borderWidth: 2,
                        '&:hover': {
                          borderWidth: 2
                        }
                      }}
                    >
                      {isRecording ? '🛑 Stop Recording' : '🎙️ Start Recording'}
                    </Button>
                    
                    {isRecording && (
                      <Fade in timeout={300}>
                        <Box sx={{ mt: 3 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, mb: 2 }}>
                            {[1, 2, 3, 4, 5].map((i) => (
                              <Box
                                key={i}
                                sx={{
                                  width: 6,
                                  height: 30,
                                  bgcolor: 'error.main',
                                  borderRadius: 3,
                                  animation: `pulse 1s ease-in-out ${i * 0.1}s infinite alternate`
                                }}
                              />
                            ))}
                          </Box>
                          <Typography variant="body2" color="error" fontWeight={700} className="neon-text">
                            🔴 Recording in progress...
                          </Typography>
                        </Box>
                      </Fade>
                    )}
                  </CardContent>
                </Card>
              </Grow>
            </Grid>

            {/* Text Input */}
            <Grid item xs={12}>
              <Grow in timeout={1000}>
                <Card sx={{ height: '100%' }} className="hover-lift">
                  <CardContent sx={{ p: 4, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'success.main', mr: 2, width: 48, height: 48 }} className="float-animation">
                        <TextFieldsIcon />
                      </Avatar>
                      <Typography variant="h6" fontWeight={700}>
                        ✍️ Text Input
                      </Typography>
                    </Box>
                    
                    <TextField
                      fullWidth
                      multiline
                      rows={6}
                      placeholder="✨ Describe your daily routines, goals, and visions here..."
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      variant="outlined"
                      sx={{ 
                        flexGrow: 1,
                        '& .MuiOutlinedInput-root': {
                          height: '100%',
                          alignItems: 'flex-start',
                          borderWidth: 2,
                          '&:hover fieldset': {
                            borderWidth: 2
                          },
                          '&.Mui-focused fieldset': {
                            borderWidth: 2
                          }
                        }
                      }}
                      className="live-chart"
                    />
                    
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                      <Typography variant="caption" color="text.secondary" fontWeight={600}>
                        {textInput.length} characters
                      </Typography>
                      <Typography variant="caption" color={textInput.length > 100 ? 'success.main' : 'text.secondary'} fontWeight={600}>
                        {textInput.length > 100 ? '✅ Good length!' : 'Keep typing...'}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grow>
            </Grid>
          </Grid>
        </Grid>

        {/* Submit Section */}
        <Grid item xs={12}>
          <Fade in timeout={1200}>
            <Paper sx={{ p: 4, textAlign: 'center', bgcolor: 'grey.50', border: '2px solid', borderColor: 'grey.200' }} className="hover-lift">
              <Button
                variant="contained"
                size="large"
                onClick={handleSubmit}
                disabled={isLoading || (selectedFiles.length === 0 && !textInput.trim())}
                startIcon={isLoading ? <CircularProgress size={24} color="inherit" /> : <SmartToyIcon />}
                className="flashy-button"
                sx={{ 
                  minWidth: 250,
                  py: 2.5,
                  px: 5,
                  borderRadius: 4,
                  fontSize: '1.2rem',
                  fontWeight: 700,
                  background: 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
                  boxShadow: '0 8px 20px rgba(139, 92, 246, 0.4)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #7C3AED 0%, #DB2777 100%)',
                    boxShadow: '0 12px 30px rgba(139, 92, 246, 0.6)',
                    transform: 'translateY(-4px) scale(1.05)'
                  },
                  '&:disabled': {
                    background: 'grey.300'
                  }
                }}
              >
                {isLoading ? '🤖 Training AI...' : '🚀 Train AI Assistant'}
              </Button>
              
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }} fontWeight={500}>
                🔒 Your data will be analyzed securely and used to personalize your scheduling experience
              </Typography>
            </Paper>
          </Fade>
          
          {uploadStatus && (
            <Fade in={!!uploadStatus}>
              <Alert 
                severity={uploadStatus.includes('❌') ? 'error' : 'success'} 
                sx={{ 
                  mt: 2, 
                  borderRadius: 2,
                  border: '2px solid',
                  borderColor: uploadStatus.includes('❌') ? 'error.main' : 'success.main',
                  fontWeight: 600,
                  fontSize: '1rem'
                }}
                icon={uploadStatus.includes('🎉') ? <CheckCircleIcon /> : undefined}
                className="hover-lift"
              >
                {uploadStatus}
              </Alert>
            </Fade>
          )}
        </Grid>

        {/* Results Section */}
        <Grid item xs={12}>
          <Collapse in={showResults && lastUploadResult && lastUploadResult.length > 0}>
            <Paper sx={{ p: 4, bgcolor: 'success.50', border: '2px solid', borderColor: 'success.200' }} className="hover-lift">
              <Typography variant="h6" fontWeight={700} gutterBottom color="success.dark">
                🎯 AI Processing Results
              </Typography>
              <Divider sx={{ mb: 3 }} />
              
              <Grid container spacing={3}>
                {lastUploadResult?.map((result: any, index: number) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Zoom in timeout={300 + index * 100}>
                      <Card sx={{ bgcolor: 'white', border: '2px solid', borderColor: 'success.200' }} className="hover-lift">
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Chip 
                              label={result.data.category} 
                              color="primary" 
                              sx={{ fontWeight: 700, fontSize: '0.9rem' }}
                              className="sparkle-effect"
                            />
                            <Box sx={{ ml: 'auto' }}>
                              <Typography variant="body2" color="success.main" fontWeight={700}>
                                ✅ {(result.data.confidence * 100).toFixed(1)}% confidence
                              </Typography>
                            </Box>
                          </Box>
                          
                          {result.data.extracted_items && (
                            <Box>
                              {Object.entries(result.data.extracted_items).map(([key, items]: [string, any]) => (
                                items.length > 0 && (
                                  <Typography key={key} variant="body2" sx={{ mb: 1 }} fontWeight={600}>
                                    <strong>📊 {key}:</strong> {items.length} item(s) extracted
                                  </Typography>
                                )
                              ))}
                            </Box>
                          )}
                        </CardContent>
                      </Card>
                    </Zoom>
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