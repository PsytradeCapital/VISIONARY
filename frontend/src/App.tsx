import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { 
  Box, 
  ThemeProvider,
  createTheme,
  CssBaseline,
  Snackbar,
  Alert
} from '@mui/material';
import Dashboard from './components/Dashboard';
import UploadPortal from './components/UploadPortal';
import ScheduleView from './components/ScheduleView';
import ProgressView from './components/ProgressView';
import Navigation from './components/Navigation';
import Login from './components/Login';
import { webSocketService } from './services/api';

// Professional theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2563EB',
      dark: '#1D4ED8',
      light: '#60A5FA',
      contrastText: '#FFFFFF'
    },
    secondary: {
      main: '#10B981',
      dark: '#059669',
      light: '#34D399'
    },
    background: {
      default: '#FAFBFC',
      paper: '#FFFFFF'
    },
    text: {
      primary: '#111827',
      secondary: '#6B7280'
    }
  },
  typography: {
    fontFamily: '"Inter", "SF Pro Display", "Segoe UI", "Roboto", "Helvetica", "Arial", sans-serif'
  },
  shape: {
    borderRadius: 12
  }
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [notification, setNotification] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'info' | 'warning' | 'error';
  }>({
    open: false,
    message: '',
    severity: 'info'
  });

  useEffect(() => {
    // Check for existing authentication
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
        setIsAuthenticated(true);
        
        // Connect to WebSocket
        webSocketService.connect(parsedUser.id, token);
        
        setNotification({
          open: true,
          message: `🚀 Welcome back, ${parsedUser.email}!`,
          severity: 'success'
        });
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
      }
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (token: string, userData: any) => {
    setUser(userData);
    setIsAuthenticated(true);
    
    // Connect to WebSocket
    webSocketService.connect(userData.id, token);
    
    setNotification({
      open: true,
      message: `🎉 Welcome to Visionary AI, ${userData.email}!`,
      severity: 'success'
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
    webSocketService.disconnect();
    
    setNotification({
      open: true,
      message: '👋 Logged out successfully!',
      severity: 'info'
    });
  };

  const handleQuickAction = (action: string) => {
    let message = '';
    switch (action) {
      case 'add-task':
        message = '📝 Quick task creation opened!';
        break;
      case 'add-event':
        message = '📅 Event scheduler opened!';
        break;
      case 'voice-note':
        message = '🎤 Voice recording started!';
        break;
      case 'camera':
        message = '📸 Camera capture ready!';
        break;
      case 'ai-assistant':
        message = '🤖 AI Assistant activated!';
        break;
      default:
        message = '✨ Action triggered!';
    }
    
    setNotification({
      open: true,
      message,
      severity: 'info'
    });
  };

  const handleCloseNotification = () => {
    setNotification(prev => ({ ...prev, open: false }));
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box 
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          minHeight="100vh"
          sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white'
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <Box
              sx={{
                width: 80,
                height: 80,
                borderRadius: '50%',
                border: '4px solid rgba(255,255,255,0.3)',
                borderTop: '4px solid white',
                animation: 'spin 1s linear infinite',
                margin: '0 auto 20px'
              }}
            />
            Loading Visionary AI...
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login onLogin={handleLogin} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        width: '100vw', 
        minHeight: '100vh', 
        paddingBottom: '100px', // Space for navigation
        overflow: 'hidden' 
      }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadPortal />} />
          <Route path="/schedule" element={<ScheduleView />} />
          <Route path="/progress" element={<ProgressView />} />
        </Routes>
        
        <Navigation onQuickAction={handleQuickAction} />
        
        {/* Notification Snackbar */}
        <Snackbar
          open={notification.open}
          autoHideDuration={3000}
          onClose={handleCloseNotification}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert
            onClose={handleCloseNotification}
            severity={notification.severity}
            sx={{
              background: 'rgba(255,255,255,0.95)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '12px',
              fontWeight: '600'
            }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      </Box>
      
      {/* Global CSS Animations */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </ThemeProvider>
  );
}

export default App;