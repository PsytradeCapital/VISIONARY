import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { 
  Container, 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Button,
  Tabs,
  Tab
} from '@mui/material';
import Dashboard from './components/Dashboard';
import UploadPortal from './components/UploadPortal';
import ScheduleView from './components/ScheduleView';
import ProgressView from './components/ProgressView';
import ImageGallery from './components/ImageGallery';
import ImageSelector from './components/ImageSelector';
import Login from './components/Login';
import { webSocketService } from './services/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const navigationTabs = [
    { label: 'Dashboard', path: '/' },
    { label: 'Upload', path: '/upload' },
    { label: 'Schedule', path: '/schedule' },
    { label: 'Progress', path: '/progress' },
    { label: 'Gallery', path: '/gallery' },
    { label: 'Selector', path: '/selector' }
  ];

  const currentTab = navigationTabs.findIndex(tab => tab.path === location.pathname);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    navigate(navigationTabs[newValue].path);
  };

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('auth_token');
    const storedUserId = localStorage.getItem('user_id');
    
    if (token && storedUserId) {
      setIsAuthenticated(true);
      setUserId(storedUserId);
      
      // Connect to WebSocket
      webSocketService.connect(storedUserId, token);
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (token: string, newUserId: string) => {
    setIsAuthenticated(true);
    setUserId(newUserId);
    
    // Connect to WebSocket
    webSocketService.connect(newUserId, token);
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    webSocketService.disconnect();
    setIsAuthenticated(false);
    setUserId('');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        Loading...
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Visionary - AI Personal Scheduler
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'primary.dark' }}>
          <Tabs 
            value={currentTab >= 0 ? currentTab : 0} 
            onChange={handleTabChange}
            textColor="inherit"
            indicatorColor="secondary"
            variant="scrollable"
            scrollButtons="auto"
          >
            {navigationTabs.map((tab, index) => (
              <Tab key={index} label={tab.label} />
            ))}
          </Tabs>
        </Box>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadPortal />} />
          <Route path="/schedule" element={<ScheduleView />} />
          <Route path="/progress" element={<ProgressView />} />
          <Route path="/gallery" element={<ImageGallery />} />
          <Route path="/selector" element={<ImageSelector />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;