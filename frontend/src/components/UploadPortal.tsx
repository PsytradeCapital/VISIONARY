import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Fab,
  Alert,
  Snackbar
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Mic as MicIcon,
  Stop as StopIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  InsertDriveFile as FileIcon,
  Image as ImageIcon,
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  Description as DocumentIcon,
  SmartToy as AIIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api, { uploadAPI } from '../services/api';

interface UploadedFile {
  id: string;
  name: string;
  size: string;
  type: string;
  uploadProgress: number;
  status: 'uploading' | 'completed' | 'processing' | 'error';
  aiAnalysis?: string;
  category?: string;
  confidence?: number;
}

const UploadPortal: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [openAIDialog, setOpenAIDialog] = useState(false);
  const [aiPrompt, setAiPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Load existing files on component mount
  useEffect(() => {
    loadKnowledgeEntries();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const loadKnowledgeEntries = async () => {
    try {
      const response = await api.get('/api/upload/knowledge');
      if (response.data.success) {
        const entries = response.data.data.map((entry: any) => ({
          id: entry.id,
          name: entry.metadata?.filename || `${entry.source_type}-${entry.id.slice(0, 8)}`,
          size: entry.metadata?.file_size ? formatFileSize(entry.metadata.file_size) : 'Unknown',
          type: entry.source_type,
          uploadProgress: 100,
          status: 'completed' as const,
          aiAnalysis: `Category: ${entry.category} (${Math.round(entry.confidence * 100)}% confidence)`,
          category: entry.category,
          confidence: entry.confidence
        }));
        setFiles(entries);
      }
    } catch (error) {
      console.error('Error loading knowledge entries:', error);
      setError('Failed to load existing files');
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files;
    if (!selectedFiles) return;

    for (const file of Array.from(selectedFiles)) {
      const newFile: UploadedFile = {
        id: Date.now().toString() + Math.random(),
        name: file.name,
        size: formatFileSize(file.size),
        type: getFileType(file.name),
        uploadProgress: 0,
        status: 'uploading'
      };
      
      setFiles(prev => [...prev, newFile]);
      
      try {
        // Upload the file using uploadAPI
        const response = await uploadAPI.uploadDocument(file);

        if (response.success) {
          setFiles(prev => prev.map(f => 
            f.id === newFile.id 
              ? { 
                  ...f, 
                  uploadProgress: 100, 
                  status: 'completed',
                  aiAnalysis: `Category: ${response.data.category} (${Math.round(response.data.confidence * 100)}% confidence)`,
                  category: response.data.category,
                  confidence: response.data.confidence
                }
              : f
          ));
          setSuccess('File uploaded and processed successfully!');
        }
      } catch (error: any) {
        console.error('Upload error:', error);
        setFiles(prev => prev.map(f => 
          f.id === newFile.id ? { ...f, status: 'error', aiAnalysis: 'Upload failed' } : f
        ));
        setError(error.response?.data?.detail || 'Upload failed');
      }
    }
  };

  const handleTextUpload = async (text: string) => {
    if (!text.trim()) return;

    const newFile: UploadedFile = {
      id: Date.now().toString(),
      name: `text-input-${new Date().toISOString().split('T')[0]}`,
      size: `${text.length} chars`,
      type: 'text',
      uploadProgress: 0,
      status: 'uploading'
    };
    
    setFiles(prev => [...prev, newFile]);
    setLoading(true);

    try {
      const response = await uploadAPI.uploadText(text);

      if (response.success) {
        setFiles(prev => prev.map(f => 
          f.id === newFile.id 
            ? { 
                ...f, 
                uploadProgress: 100, 
                status: 'completed',
                aiAnalysis: `Category: ${response.data.category} (${Math.round(response.data.confidence * 100)}% confidence)`,
                category: response.data.category,
                confidence: response.data.confidence
              }
            : f
        ));
        setSuccess('Text processed successfully!');
        setAiPrompt('');
        setOpenAIDialog(false);
      }
    } catch (error: any) {
      console.error('Text upload error:', error);
      setFiles(prev => prev.map(f => 
        f.id === newFile.id ? { ...f, status: 'error', aiAnalysis: 'Processing failed' } : f
      ));
      setError(error.response?.data?.detail || 'Text processing failed');
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileType = (filename: string): string => {
    const extension = filename.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf': return 'pdf';
      case 'doc':
      case 'docx': return 'document';
      case 'xls':
      case 'xlsx': return 'spreadsheet';
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif': return 'image';
      case 'mp4':
      case 'avi':
      case 'mov': return 'video';
      case 'mp3':
      case 'wav':
      case 'aac': return 'audio';
      default: return 'file';
    }
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf':
      case 'document': return <DocumentIcon />;
      case 'image': return <ImageIcon />;
      case 'video': return <VideoIcon />;
      case 'audio': return <AudioIcon />;
      default: return <FileIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return '#4caf50';
      case 'uploading': return '#2196f3';
      case 'processing': return '#ff9800';
      case 'error': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const startRecording = async () => {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Create MediaRecorder
      const recorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];
      
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };
      
      recorder.onstop = async () => {
        // Create audio blob
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        
        // Upload the recording
        await handleVoiceUpload(audioBlob);
      };
      
      recorder.start();
      setMediaRecorder(recorder);
      setAudioChunks(chunks);
      setIsRecording(true);
      setRecordingTime(0);
      
      // Start timer
      const recordingTimer = setInterval(() => {
        setRecordingTime(prev => {
          if (prev >= 300) { // 5 minutes max
            stopRecording();
            clearInterval(recordingTimer);
            return prev;
          }
          return prev + 1;
        });
      }, 1000);
      
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Failed to access microphone. Please grant permission.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
    setIsRecording(false);
    setRecordingTime(0);
  };

  const handleVoiceUpload = async (audioBlob: Blob) => {
    const newFile: UploadedFile = {
      id: Date.now().toString(),
      name: `voice-note-${new Date().toISOString().split('T')[0]}.wav`,
      size: formatFileSize(audioBlob.size),
      type: 'audio',
      uploadProgress: 0,
      status: 'uploading'
    };
    
    setFiles(prev => [...prev, newFile]);
    setLoading(true);

    try {
      const response = await uploadAPI.uploadVoice(audioBlob);

      if (response.success) {
        setFiles(prev => prev.map(f => 
          f.id === newFile.id 
            ? { 
                ...f, 
                uploadProgress: 100, 
                status: 'completed',
                aiAnalysis: `Transcribed: ${response.data.category} (${Math.round(response.data.confidence * 100)}% confidence)`,
                category: response.data.category,
                confidence: response.data.confidence
              }
            : f
        ));
        setSuccess('Voice recording processed successfully!');
      }
    } catch (error: any) {
      console.error('Voice upload error:', error);
      setFiles(prev => prev.map(f => 
        f.id === newFile.id ? { ...f, status: 'error', aiAnalysis: 'Processing failed' } : f
      ));
      setError(error.response?.data?.detail || 'Voice processing failed');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const deleteFile = (fileId: string) => {
    setFiles(prev => prev.filter(file => file.id !== fileId));
  };

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: 3
    }}>
      {/* Header */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        mb: 4,
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)',
        borderRadius: 3,
        padding: 2
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ 
            background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
            width: 56, 
            height: 56 
          }}>
            <UploadIcon sx={{ fontSize: 32 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
              Smart Upload Portal
            </Typography>
            <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              AI-powered file processing and analysis
            </Typography>
          </Box>
        </Box>
        
        <Button
          variant="contained"
          startIcon={<AIIcon />}
          onClick={() => setOpenAIDialog(true)}
          sx={{
            background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
            boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
            px: 3,
            py: 1.5
          }}
        >
          AI Assistant
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Upload Area */}
        <Grid item xs={12} md={8}>
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Typography variant="h5" fontWeight="bold" color="primary" gutterBottom>
                Upload Files
              </Typography>
              
              {/* Drag & Drop Area */}
              <Box
                sx={{
                  border: '2px dashed #2196f3',
                  borderRadius: 3,
                  padding: 4,
                  textAlign: 'center',
                  background: 'linear-gradient(45deg, #2196f315 30%, #21cbf315 90%)',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #2196f325 30%, #21cbf325 90%)',
                    transform: 'scale(1.02)'
                  }
                }}
                onClick={() => fileInputRef.current?.click()}
              >
                <UploadIcon sx={{ fontSize: 64, color: '#2196f3', mb: 2 }} />
                <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                  Drop files here or click to browse
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Supports PDF, DOC, XLS, Images, Audio, Video files
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Maximum file size: 100MB
                </Typography>
              </Box>
              
              <input
                ref={fileInputRef}
                type="file"
                multiple
                style={{ display: 'none' }}
                onChange={handleFileUpload}
                accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif,.mp4,.avi,.mov,.mp3,.wav,.aac"
              />
            </CardContent>
          </Card>

          {/* File List */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            height: '400px',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Typography variant="h5" fontWeight="bold" color="primary" gutterBottom>
                Uploaded Files
              </Typography>
              
              <List sx={{ maxHeight: '320px', overflow: 'auto' }}>
                {files.map((file) => (
                  <ListItem
                    key={file.id}
                    sx={{
                      mb: 2,
                      borderRadius: 2,
                      background: 'rgba(0,0,0,0.02)',
                      border: `2px solid ${getStatusColor(file.status)}20`,
                      '&:hover': { 
                        background: 'rgba(0,0,0,0.05)',
                        transform: 'translateX(5px)',
                        transition: 'all 0.3s ease'
                      }
                    }}
                  >
                    <ListItemIcon>
                      <Avatar sx={{ 
                        background: getStatusColor(file.status),
                        width: 48,
                        height: 48
                      }}>
                        {getFileIcon(file.type)}
                      </Avatar>
                    </ListItemIcon>
                    
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                          <Typography variant="h6" fontWeight="bold">
                            {file.name}
                          </Typography>
                          <Chip 
                            label={file.status} 
                            size="small" 
                            sx={{ 
                              background: getStatusColor(file.status),
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            Size: {file.size}
                          </Typography>
                          {file.status === 'uploading' && (
                            <LinearProgress 
                              variant="determinate" 
                              value={file.uploadProgress} 
                              sx={{ mt: 1, borderRadius: 1 }}
                            />
                          )}
                          {file.aiAnalysis && (
                            <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic', color: '#2196f3' }}>
                              🤖 {file.aiAnalysis}
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                    
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      <IconButton size="small" sx={{ color: '#2196f3' }}>
                        <DownloadIcon />
                      </IconButton>
                      <IconButton 
                        size="small" 
                        sx={{ color: '#f44336' }}
                        onClick={() => deleteFile(file.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Voice Recording & AI Tools */}
        <Grid item xs={12} md={4}>
          {/* Voice Recording */}
          <Card sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <MicIcon sx={{ fontSize: 32 }} />
                <Typography variant="h6" fontWeight="bold">
                  Voice Recording
                </Typography>
              </Box>
              
              <Box sx={{ textAlign: 'center', mb: 3 }}>
                {isRecording ? (
                  <Box>
                    <Typography variant="h4" fontWeight="bold" sx={{ mb: 2 }}>
                      {formatTime(recordingTime)}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                      <Button
                        variant="contained"
                        startIcon={<StopIcon />}
                        onClick={stopRecording}
                        sx={{
                          background: '#f44336',
                          '&:hover': { background: '#d32f2f' }
                        }}
                      >
                        Stop Recording
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  <Button
                    variant="contained"
                    startIcon={<MicIcon />}
                    onClick={startRecording}
                    sx={{
                      background: 'rgba(255,255,255,0.2)',
                      color: 'white',
                      py: 2,
                      px: 4,
                      fontSize: '1.1rem',
                      '&:hover': { background: 'rgba(255,255,255,0.3)' }
                    }}
                  >
                    Start Recording
                  </Button>
                )}
              </Box>
              
              <Typography variant="body2" sx={{ opacity: 0.9, textAlign: 'center' }}>
                Record voice notes, meetings, or ideas. AI will automatically transcribe and analyze.
              </Typography>
            </CardContent>
          </Card>

          {/* AI Processing Stats */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                AI Processing Stats
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  📄 {files.filter(f => f.status === 'completed').length} Files Processed
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  🔄 {files.filter(f => f.status === 'processing').length} Currently Processing
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  📊 {files.filter(f => f.aiAnalysis).length} AI Analyses Complete
                </Typography>
                <Typography variant="body2">
                  ⚡ Average processing time: 2.3 minutes
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                Quick Actions
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<AIIcon />}
                    onClick={() => navigate('/progress')}
                    sx={{
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      py: 2
                    }}
                  >
                    View AI Insights
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<DownloadIcon />}
                    sx={{ py: 2 }}
                  >
                    Export All Files
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Assistant Dialog */}
      <Dialog open={openAIDialog} onClose={() => setOpenAIDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Process Text Input</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Enter text to be processed by AI for schedule generation and insights.
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Enter your text, goals, or notes"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
            placeholder="e.g., I want to exercise 3 times a week, learn Spanish for 30 minutes daily, and save $500 monthly..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAIDialog(false)}>Cancel</Button>
          <Button 
            variant="contained" 
            startIcon={<AIIcon />}
            onClick={() => handleTextUpload(aiPrompt)}
            disabled={loading || !aiPrompt.trim()}
          >
            {loading ? 'Processing...' : 'Process Text'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Error/Success Snackbars */}
      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setError(null)} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar 
        open={!!success} 
        autoHideDuration={4000} 
        onClose={() => setSuccess(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={() => setSuccess(null)} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)'
        }}
        onClick={() => fileInputRef.current?.click()}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
};

export default UploadPortal;