import React, { useState } from 'react';
import {
  Box,
  BottomNavigation,
  BottomNavigationAction,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Paper,
  Tooltip,
  Badge
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Schedule as ScheduleIcon,
  CloudUpload as UploadIcon,
  TrendingUp as ProgressIcon,
  SmartToy as AIIcon,
  Add as AddIcon,
  Mic as MicIcon,
  PhotoCamera as CameraIcon,
  Assignment as TaskIcon,
  Event as EventIcon,
  Notifications as NotificationIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

interface NavigationProps {
  onQuickAction?: (action: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({ onQuickAction }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [speedDialOpen, setSpeedDialOpen] = useState(false);

  const navigationItems = [
    { 
      label: 'Dashboard', 
      value: '/', 
      icon: <DashboardIcon />,
      color: '#2563EB'
    },
    { 
      label: 'Schedule', 
      value: '/schedule', 
      icon: <ScheduleIcon />,
      color: '#10B981'
    },
    { 
      label: 'Upload', 
      value: '/upload', 
      icon: <UploadIcon />,
      color: '#F59E0B'
    },
    { 
      label: 'Progress', 
      value: '/progress', 
      icon: <ProgressIcon />,
      color: '#8B5CF6'
    }
  ];

  const speedDialActions = [
    {
      icon: <TaskIcon />,
      name: 'Quick Task',
      action: 'add-task',
      color: '#EF4444'
    },
    {
      icon: <EventIcon />,
      name: 'Schedule Event',
      action: 'add-event',
      color: '#3B82F6'
    },
    {
      icon: <MicIcon />,
      name: 'Voice Note',
      action: 'voice-note',
      color: '#10B981'
    },
    {
      icon: <CameraIcon />,
      name: 'Quick Capture',
      action: 'camera',
      color: '#F59E0B'
    }
  ];

  const handleNavigation = (value: string) => {
    navigate(value);
  };

  const handleSpeedDialAction = (action: string) => {
    setSpeedDialOpen(false);
    if (onQuickAction) {
      onQuickAction(action);
    }
  };

  const getCurrentValue = () => {
    return navigationItems.find(item => item.value === location.pathname)?.value || '/';
  };

  return (
    <>
      {/* Bottom Navigation */}
      <Paper
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 1000,
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%)',
          backdropFilter: 'blur(20px)',
          borderTop: '1px solid rgba(255,255,255,0.2)',
          boxShadow: '0 -10px 30px rgba(0,0,0,0.1)'
        }}
        elevation={0}
      >
        <BottomNavigation
          value={getCurrentValue()}
          onChange={(event, newValue) => handleNavigation(newValue)}
          sx={{
            background: 'transparent',
            height: 80,
            '& .MuiBottomNavigationAction-root': {
              minWidth: 'auto',
              padding: '8px 12px',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              borderRadius: '16px',
              margin: '4px',
              '&:hover': {
                transform: 'translateY(-4px) scale(1.05)',
                background: 'rgba(255,255,255,0.8)',
                boxShadow: '0 8px 25px rgba(0,0,0,0.15)'
              },
              '&.Mui-selected': {
                transform: 'translateY(-6px) scale(1.1)',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                boxShadow: '0 12px 30px rgba(102, 126, 234, 0.4)',
                '& .MuiBottomNavigationAction-label': {
                  fontSize: '0.75rem',
                  fontWeight: 'bold'
                }
              }
            },
            '& .MuiBottomNavigationAction-label': {
              fontSize: '0.7rem',
              fontWeight: '600',
              marginTop: '4px'
            }
          }}
        >
          {navigationItems.map((item) => (
            <BottomNavigationAction
              key={item.value}
              label={item.label}
              value={item.value}
              icon={
                <Badge
                  badgeContent={item.label === 'Schedule' ? 3 : undefined}
                  color="error"
                  variant="dot"
                  sx={{
                    '& .MuiBadge-badge': {
                      animation: 'pulse 2s infinite'
                    }
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 32,
                      height: 32,
                      borderRadius: '50%',
                      background: location.pathname === item.value 
                        ? 'rgba(255,255,255,0.2)' 
                        : 'transparent',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    {React.cloneElement(item.icon, {
                      sx: { 
                        fontSize: 24,
                        filter: location.pathname === item.value 
                          ? 'drop-shadow(0 0 8px rgba(255,255,255,0.5))' 
                          : 'none'
                      }
                    })}
                  </Box>
                </Badge>
              }
            />
          ))}
        </BottomNavigation>
      </Paper>

      {/* AI Assistant Floating Button */}
      <Fab
        sx={{
          position: 'fixed',
          bottom: 100,
          right: 20,
          background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
          color: 'white',
          width: 64,
          height: 64,
          boxShadow: '0 8px 25px rgba(254, 107, 139, 0.4)',
          '&:hover': {
            transform: 'scale(1.1) rotate(5deg)',
            boxShadow: '0 12px 35px rgba(254, 107, 139, 0.6)',
            background: 'linear-gradient(45deg, #FF8E53 30%, #FE6B8B 90%)'
          },
          '&:active': {
            transform: 'scale(0.95)'
          },
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          animation: 'float 3s ease-in-out infinite'
        }}
        onClick={() => handleSpeedDialAction('ai-assistant')}
      >
        <AIIcon sx={{ fontSize: 32 }} />
      </Fab>

      {/* Speed Dial for Quick Actions */}
      <SpeedDial
        ariaLabel="Quick Actions"
        sx={{
          position: 'fixed',
          bottom: 180,
          right: 20,
          '& .MuiFab-primary': {
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
              transform: 'scale(1.1)'
            }
          },
          '& .MuiSpeedDialAction-fab': {
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255,255,255,0.2)',
            '&:hover': {
              transform: 'scale(1.1)',
              boxShadow: '0 8px 25px rgba(0,0,0,0.15)'
            }
          }
        }}
        icon={<SpeedDialIcon />}
        onClose={() => setSpeedDialOpen(false)}
        onOpen={() => setSpeedDialOpen(true)}
        open={speedDialOpen}
        direction="up"
      >
        {speedDialActions.map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={React.cloneElement(action.icon, { 
              sx: { color: action.color, fontSize: 24 } 
            })}
            tooltipTitle={action.name}
            tooltipOpen
            onClick={() => handleSpeedDialAction(action.action)}
            sx={{
              '& .MuiSpeedDialAction-staticTooltip': {
                background: 'rgba(0,0,0,0.8)',
                color: 'white',
                borderRadius: '8px',
                fontSize: '0.75rem',
                fontWeight: '600'
              }
            }}
          />
        ))}
      </SpeedDial>

      {/* Notification Badge */}
      <Tooltip title="3 new notifications" placement="left">
        <Fab
          size="small"
          sx={{
            position: 'fixed',
            top: 20,
            right: 20,
            background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
            color: 'white',
            width: 48,
            height: 48,
            boxShadow: '0 4px 15px rgba(76, 175, 80, 0.4)',
            '&:hover': {
              transform: 'scale(1.1)',
              boxShadow: '0 6px 20px rgba(76, 175, 80, 0.6)'
            },
            animation: 'bounce 2s infinite'
          }}
        >
          <Badge badgeContent={3} color="error">
            <NotificationIcon />
          </Badge>
        </Fab>
      </Tooltip>

      {/* CSS Animations */}
      <style>
        {`
          @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
          }
          
          @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
          }
          
          @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
          }
          
          @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
            50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
          }
        `}
      </style>
    </>
  );
};

export default Navigation;