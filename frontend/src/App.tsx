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
  Tab,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Avatar,
  IconButton,
  Menu,
  MenuItem,
  Chip
} from '@mui/material';
import { 
  Dashboard as DashboardIcon,
  CloudUpload as UploadIcon,
  Schedule as ScheduleIcon,
  TrendingUp as ProgressIcon,
  AccountCircle,
  Notifications
} from '@mui/icons-material';
import Dashboard from './components/Dashboard';
import UploadPortal from './components/UploadPortal';
import ScheduleView from './components/ScheduleView';
import ProgressView from './components/ProgressView';
import Login from './components/Login';
import { webSocketService } from './services/api';

// Professional theme based on top-rated reference images (4.65/5.0 avg rating)
// Inspired by image2.jpeg (4.8★), image4.jpeg (4.7★), image3.jpeg (4.6★)
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2563EB', // Modern blue from top-rated scheduling interfaces
      dark: '#1D4ED8',
      light: '#60A5FA',
      contrastText: '#FFFFFF'
    },
    secondary: {
      main: '#10B981', // Success green from scheduling interfaces
      dark: '#059669',
      light: '#34D399'
    },
    info: {
      main: '#8B5CF6', // Purple from AI assistant designs (image4.jpeg)
      light: '#A78BFA',
      dark: '#7C3AED'
    },
    warning: {
      main: '#F59E0B', // Orange from analytics (image3.jpeg)
      light: '#FBBF24',
      dark: '#D97706'
    },
    error: {
      main: '#EF4444',
      light: '#F87171',
      dark: '#DC2626'
    },
    success: {
      main: '#10B981',
      light: '#34D399',
      dark: '#059669'
    },
    background: {
      default: '#FAFBFC', // Ultra-clean background
      paper: '#FFFFFF'
    },
    text: {
      primary: '#111827', // Rich dark text for readability
      secondary: '#6B7280' // Sophisticated gray
    },
    grey: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      200: '#E5E7EB',
      300: '#D1D5DB',
      400: '#9CA3AF',
      500: '#6B7280',
      600: '#4B5563',
      700: '#374151',
      800: '#1F2937',
      900: '#111827'
    },
    divider: '#E5E7EB'
  },
  typography: {
    fontFamily: '"Inter", "SF Pro Display", "Segoe UI", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 800,
      fontSize: '3.5rem',
      lineHeight: 1.1,
      letterSpacing: '-0.025em'
    },
    h2: {
      fontWeight: 700,
      fontSize: '2.75rem',
      lineHeight: 1.2,
      letterSpacing: '-0.02em'
    },
    h3: {
      fontWeight: 700,
      fontSize: '2.25rem',
      lineHeight: 1.2,
      letterSpacing: '-0.015em'
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.875rem',
      lineHeight: 1.3,
      letterSpacing: '-0.01em'
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.4,
      letterSpacing: '-0.005em'
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.4
    },
    subtitle1: {
      fontSize: '1.125rem',
      fontWeight: 500,
      lineHeight: 1.5,
      color: '#6B7280'
    },
    subtitle2: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.5,
      color: '#9CA3AF'
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      color: '#374151'
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
      color: '#6B7280'
    },
    button: {
      fontWeight: 600,
      textTransform: 'none',
      letterSpacing: '0.025em'
    }
  },
  shape: {
    borderRadius: 12
  },
  shadows: [
    'none',
    '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
  ],
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#FAFBFC',
          fontFamily: '"Inter", "SF Pro Display", "Segoe UI", "Roboto", "Helvetica", "Arial", sans-serif'
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
          borderRadius: 16,
          border: '1px solid #F3F4F6',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            transform: 'translateY(-4px)',
            borderColor: '#E5E7EB'
          }
        }
      }
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 10,
          padding: '10px 20px',
          fontSize: '0.95rem',
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          boxShadow: 'none'
        },
        contained: {
          boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
          '&:hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            transform: 'translateY(-1px)'
          }
        },
        outlined: {
          borderWidth: '1.5px',
          '&:hover': {
            borderWidth: '1.5px',
            transform: 'translateY(-1px)',
            boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
          }
        }
      }
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
          backdropFilter: 'blur(12px)',
          backgroundColor: 'rgba(37, 99, 235, 0.95)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none'
        }
      }
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
          fontSize: '0.875rem'
        }
      }
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 10,
            '& fieldset': {
              borderColor: '#E5E7EB'
            },
            '&:hover fieldset': {
              borderColor: '#D1D5DB'
            },
            '&.Mui-focused fieldset': {
              borderColor: '#2563EB',
              borderWidth: '2px'
            }
          }
        }
      }
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '0.95rem',
          minHeight: 48,
          '&.Mui-selected': {
            fontWeight: 600
          }
        }
      }
    }
  }
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const location = useLocation();

  const navigationTabs = [
    { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { label: 'Upload', path: '/upload', icon: <UploadIcon /> },
    { label: 'Schedule', path: '/schedule', icon: <ScheduleIcon /> },
    { label: 'Progress', path: '/progress', icon: <ProgressIcon /> }
  ];

  const currentTab = navigationTabs.findIndex(tab => tab.path === location.pathname);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    navigate(navigationTabs[newValue].path);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
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
    handleMenuClose();
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
          <Typography variant="h6">Loading Visionary...</Typography>
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
      <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar sx={{ px: { xs: 2, sm: 3 } }}>
            <Box display="flex" alignItems="center" sx={{ flexGrow: 1 }}>
              <Avatar 
                sx={{ 
                  width: 40, 
                  height: 40, 
                  mr: 2,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  fontWeight: 700
                }}
              >
                V
              </Avatar>
              <Box>
                <Typography variant="h6" component="div" sx={{ fontWeight: 700, fontSize: '1.25rem' }}>
                  Visionary
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.75rem' }}>
                  AI Personal Scheduler
                </Typography>
              </Box>
            </Box>
            
            <Box display="flex" alignItems="center" gap={1}>
              <Chip 
                label="Pro" 
                size="small" 
                sx={{ 
                  bgcolor: 'rgba(255, 255, 255, 0.2)', 
                  color: 'white',
                  fontWeight: 600
                }} 
              />
              <IconButton color="inherit" sx={{ ml: 1 }}>
                <Notifications />
              </IconButton>
              <IconButton 
                color="inherit" 
                onClick={handleMenuOpen}
                sx={{ ml: 1 }}
              >
                <AccountCircle />
              </IconButton>
            </Box>
          </Toolbar>
          
          <Box sx={{ 
            borderBottom: 1, 
            borderColor: 'rgba(255, 255, 255, 0.1)', 
            bgcolor: 'rgba(29, 78, 216, 0.8)',
            px: { xs: 2, sm: 3 }
          }}>
            <Tabs 
              value={currentTab >= 0 ? currentTab : 0} 
              onChange={handleTabChange}
              textColor="inherit"
              indicatorColor="secondary"
              variant="scrollable"
              scrollButtons="auto"
              sx={{
                '& .MuiTab-root': {
                  color: 'rgba(255, 255, 255, 0.8)',
                  '&.Mui-selected': {
                    color: 'white'
                  }
                }
              }}
            >
              {navigationTabs.map((tab, index) => (
                <Tab 
                  key={index} 
                  label={tab.label}
                  icon={tab.icon}
                  iconPosition="start"
                  sx={{ minHeight: 56 }}
                />
              ))}
            </Tabs>
          </Box>
        </AppBar>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: {
              mt: 1,
              minWidth: 200,
              borderRadius: 2,
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
            }
          }}
        >
          <MenuItem onClick={handleMenuClose}>
            <Typography variant="body2" color="text.secondary">
              Signed in as {userId}
            </Typography>
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <Typography variant="body2" color="error.main">
              Sign Out
            </Typography>
          </MenuItem>
        </Menu>
        
        <Container 
          maxWidth="xl" 
          sx={{ 
            mt: { xs: 3, sm: 4 }, 
            mb: { xs: 3, sm: 4 },
            px: { xs: 2, sm: 3 }
          }}
        >
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadPortal />} />
            <Route path="/schedule" element={<ScheduleView />} />
            <Route path="/progress" element={<ProgressView />} />
          </Routes>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;