import React, { useState, useRef } from 'react';
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
  Fab
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Mic as MicIcon,
  Stop as StopIcon,
  PlayArrow as PlayIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  InsertDriveFile as FileIcon,
  Image as ImageIcon,
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  Description as DocumentIcon,
  SmartToy as AIIcon,
  Add as AddIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface UploadedFile {
  id: string;
  name: string;
  size: string;
  type: string;
  uploadProgress: number;
  status: 'uploading' | 'completed' | 'processing' | 'error';
  aiAnalysis?: string;
}

const UploadPortal: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<UploadedFile[]>([
    {
      id: '1',
      name: 'project-presentation.pdf',
      size: '2.4 MB',
      type: 'pdf',
      uploadProgress: 100,
      status: 'completed',
      aiAnalysis: 'Document contains 15 slides about AI implementation strategy'
    },
    {
      id: '2',
      name: 'meeting-recording.mp3',
      size: '12.8 MB',
      type: 'audio',
      uploadProgress: 100,
      status: 'processing',
      aiAnalysis: 'Audio transcription in progress...'
    },
    {
      id: '3',
      name: 'data-analysis.xlsx',
      size: '856 KB',
      type: 'spreadsheet',
      uploadProgress: 75,
      status: 'uploading'
    }
  ]);

  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [openAIDialog, setOpenAIDialog] = useState(false);
  const [aiPrompt, setAiPrompt] = useState('');

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files;
    if (selectedFiles) {
      Array.from(selectedFiles).forEach((file) => {
        const newFile: UploadedFile = {
          id: Date.now().toString() + Math.random(),
          name: file.name,
          size: formatFileSize(file.size),
          type: getFileType(file.name),
          uploadProgress: 0,
          status: 'uploading'
        };
        
        setFiles(prev => [...prev, newFile]);
        
        // Simulate upload progress
        simulateUpload(newFile.id);
      });
    }
  };

  const simulateUpload = (fileId: string) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 20;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setFiles(prev => prev.map(file => 
          file.id === fileId 
            ? { ...file, uploadProgress: 100, status: 'completed', aiAnalysis: 'AI analysis completed successfully' }
            : file
        ));
      } else {
        setFiles(prev => prev.map(file => 
          file.id === fileId ? { ...file, uploadProgress: progress } : file
        ));
      }
    }, 500);
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

  const startRecording = () => {
    setIsRecording(true);
    setRecordingTime(0);
    
    // Simulate recording timer
    const timer = setInterval(() => {
      setRecordingTime(prev => {
        if (prev >= 300) { // 5 minutes max
          stopRecording();
          return prev;
        }
        return prev + 1;
      });
    }, 1000);
  };

  const stopRecording = () => {
    setIsRecording(false);
    
    // Add recorded file
    const recordedFile: UploadedFile = {
      id: Date.now().toString(),
      name: `voice-note-${new Date().toISOString().split('T')[0]}.mp3`,
      size: `${(recordingTime * 0.1).toFixed(1)} MB`,
      type: 'audio',
      uploadProgress: 100,
      status: 'processing',
      aiAnalysis: 'Voice transcription and analysis in progress...'
    };
    
    setFiles(prev => [...prev, recordedFile]);
    setRecordingTime(0);
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
        <DialogTitle>AI Assistant</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Ask the AI to analyze your files, extract information, or provide insights.
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="What would you like to know about your files?"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
            placeholder="e.g., Summarize the main points from my uploaded documents..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAIDialog(false)}>Cancel</Button>
          <Button 
            variant="contained" 
            startIcon={<AIIcon />}
            onClick={() => {
              // Simulate AI processing
              setOpenAIDialog(false);
              setAiPrompt('');
            }}
          >
            Ask AI
          </Button>
        </DialogActions>
      </Dialog>

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