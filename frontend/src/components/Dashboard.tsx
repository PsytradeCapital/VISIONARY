import React, { useState } from 'react';
import { 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent,
  Button,
  Avatar,
  Chip,
  LinearProgress,
  Divider,
  Fade,
  Zoom,
  Grow
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import InsightsIcon from '@mui/icons-material/Insights';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import StarIcon from '@mui/icons-material/Star';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import TimelineIcon from '@mui/icons-material/Timeline';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [hoveredCard, setHoveredCard] = useState<number | null>(null);

  // Live interactive feature cards with actual interface images
  const mainFeatures = [
    {
      icon: <UploadFileIcon sx={{ fontSize: 40 }} />,
      title: 'Upload Portal',
      description: 'Upload your routines, goals, and visions to train your AI assistant',
      action: 'Start Uploading',
      route: '/upload',
      color: '#8B5CF6',
      image: '/images/upload portal.jpeg',
      stats: { label: 'AI Training', value: '100%' }
    },
    {
      icon: <CalendarTodayIcon sx={{ fontSize: 40 }} />,
      title: 'Schedule & Editor',
      description: 'View and edit your personalized daily, weekly, and monthly schedules',
      action: 'Open Schedule',
      route: '/schedule',
      color: '#10B981',
      image: '/images/schedule and editor.jpeg',
      stats: { label: 'Tasks Today', value: '8' }
    },
    {
      icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
      title: 'Progress Tracker',
      description: 'Monitor your progress with live charts and analytics',
      action: 'View Progress',
      route: '/progress',
      color: '#F59E0B',
      image: '/images/progress tracker.jpeg',
      stats: { label: 'Completion', value: '75%' }
    },
    {
      icon: <TimelineIcon sx={{ fontSize: 40 }} />,
      title: 'Goal Tracking',
      description: 'Track and achieve your financial, health, and personal goals',
      action: 'Track Goals',
      route: '/progress',
      color: '#EF4444',
      image: '/images/goal tracking.jpeg',
      stats: { label: 'Goals Active', value: '12' }
    },
    {
      icon: <NotificationsActiveIcon sx={{ fontSize: 40 }} />,
      title: 'Notifications & Reminders',
      description: 'Stay on track with smart notifications and reminders',
      action: 'View Alerts',
      route: '/schedule',
      color: '#3B82F6',
      image: '/images/notification and reminder.jpeg',
      stats: { label: 'Pending', value: '5' }
    },
    {
      icon: <SmartToyIcon sx={{ fontSize: 40 }} />,
      title: 'Complete Interface',
      description: 'Access all features in one unified, intelligent dashboard',
      action: 'Explore All',
      route: '/',
      color: '#EC4899',
      image: '/images/complete user interface.jpeg',
      stats: { label: 'Features', value: 'All' }
    }
  ];

  // Quick action items
  const quickActions = [
    { icon: <UploadFileIcon />, label: 'Upload Data', route: '/upload', color: '#8B5CF6' },
    { icon: <TrendingUpIcon />, label: 'View Progress', route: '/progress', color: '#F59E0B' },
    { icon: <CalendarTodayIcon />, label: 'Today\'s Schedule', route: '/schedule', color: '#10B981' },
    { icon: <SmartToyIcon />, label: 'AI Assistant', route: '/upload', color: '#3B82F6' }
  ];

  // Recent achievements with animations
  const achievements = [
    { title: 'Morning Routine Completed', time: '2 hours ago', type: 'routine', icon: '✅' },
    { title: 'Weekly Goal: 75% Complete', time: '1 day ago', type: 'goal', icon: '🎯' },
    { title: 'AI Training Updated', time: '3 days ago', type: 'ai', icon: '🤖' }
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section with Gradient Animation */}
      <Fade in timeout={800}>
        <Box
          className="gradient-bg"
          sx={{
            color: 'white',
            p: 4,
            borderRadius: 3,
            mb: 4,
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          <Box sx={{ position: 'relative', zIndex: 2 }}>
            <Zoom in timeout={1000}>
              <Typography variant="h3" fontWeight={700} gutterBottom className="float-animation">
                Welcome to Visionary ✨
              </Typography>
            </Zoom>
            <Typography variant="h6" sx={{ opacity: 0.95, mb: 3, maxWidth: 700 }}>
              Your AI-powered personal scheduling assistant with live, interactive interfaces
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Chip 
                icon={<StarIcon />} 
                label="Professional Design" 
                className="sparkle-effect"
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
              <Chip 
                label="AI-Powered Scheduling" 
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
              <Chip 
                label="Live Analytics" 
                className="heartbeat-animation"
                sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white', fontWeight: 600 }} 
              />
            </Box>
          </Box>
        </Box>
      </Fade>

      <Grid container spacing={4}>
        {/* Main Feature Cards with Live Images */}
        <Grid item xs={12}>
          <Typography variant="h5" fontWeight={600} gutterBottom sx={{ mb: 3 }}>
            🚀 Live Interactive Features
          </Typography>
          <Grid container spacing={3}>
            {mainFeatures.map((feature, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Grow in timeout={500 + index * 100}>
                  <Card 
                    className="interactive-image hover-lift"
                    onMouseEnter={() => setHoveredCard(index)}
                    onMouseLeave={() => setHoveredCard(null)}
                    sx={{ 
                      height: '100%',
                      position: 'relative',
                      overflow: 'hidden',
                      cursor: 'pointer',
                      transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                      transform: hoveredCard === index ? 'scale(1.05) translateY(-10px)' : 'scale(1)',
                      boxShadow: hoveredCard === index 
                        ? `0 25px 50px ${feature.color}40` 
                        : '0 4px 6px rgba(0,0,0,0.1)',
                      '&:hover': {
                        '& .feature-image': {
                          transform: 'scale(1.1)',
                          filter: 'brightness(1.1) contrast(1.05)'
                        },
                        '& .overlay': {
                          opacity: 0.85
                        }
                      }
                    }}
                    onClick={() => navigate(feature.route)}
                  >
                    {/* High-Resolution Background Image */}
                    <Box
                      className="feature-image"
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        backgroundImage: `url(${feature.image})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                        transition: 'all 0.4s ease',
                        zIndex: 1
                      }}
                    />
                    
                    {/* Gradient Overlay */}
                    <Box
                      className="overlay"
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: `linear-gradient(135deg, ${feature.color}dd 0%, ${feature.color}99 100%)`,
                        opacity: 0.75,
                        transition: 'opacity 0.3s ease',
                        zIndex: 2
                      }}
                    />
                    
                    <CardContent sx={{ position: 'relative', zIndex: 3, pt: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar 
                          sx={{ 
                            bgcolor: 'white', 
                            color: feature.color,
                            mr: 2,
                            width: 64,
                            height: 64,
                            boxShadow: '0 8px 16px rgba(0,0,0,0.2)'
                          }}
                          className={hoveredCard === index ? 'heartbeat-animation' : ''}
                        >
                          {feature.icon}
                        </Avatar>
                        <Box>
                          <Typography variant="h6" fontWeight={700} color="white" sx={{ textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}>
                            {feature.title}
                          </Typography>
                          <Chip 
                            label={`${feature.stats.label}: ${feature.stats.value}`}
                            size="small"
                            sx={{ 
                              bgcolor: 'rgba(255,255,255,0.3)', 
                              color: 'white',
                              fontSize: '0.75rem',
                              fontWeight: 600,
                              backdropFilter: 'blur(10px)'
                            }} 
                          />
                        </Box>
                      </Box>
                      
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          color: 'white', 
                          mb: 3,
                          minHeight: 48,
                          textShadow: '0 1px 2px rgba(0,0,0,0.3)',
                          flexGrow: 1
                        }}
                      >
                        {feature.description}
                      </Typography>
                      
                      <Button 
                        variant="contained"
                        fullWidth
                        endIcon={<ArrowForwardIcon />}
                        className="flashy-button"
                        sx={{ 
                          bgcolor: 'white',
                          color: feature.color,
                          fontWeight: 700,
                          py: 1.5,
                          fontSize: '1rem',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
                          '&:hover': {
                            bgcolor: 'rgba(255,255,255,0.95)',
                            transform: 'translateY(-2px)',
                            boxShadow: '0 8px 20px rgba(0,0,0,0.3)'
                          }
                        }}
                      >
                        {feature.action}
                      </Button>
                    </CardContent>
                  </Card>
                </Grow>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Quick Actions & Recent Activity */}
        <Grid item xs={12} md={8}>
          <Fade in timeout={1200}>
            <Paper sx={{ p: 3, height: '100%' }} className="hover-lift">
              <Typography variant="h6" fontWeight={600} gutterBottom>
                ⚡ Quick Actions
              </Typography>
              <Grid container spacing={2}>
                {quickActions.map((action, index) => (
                  <Grid item xs={6} sm={3} key={index}>
                    <Zoom in timeout={800 + index * 100}>
                      <Button
                        variant="outlined"
                        fullWidth
                        startIcon={action.icon}
                        onClick={() => navigate(action.route)}
                        className="clickable-glow"
                        sx={{ 
                          py: 2,
                          flexDirection: 'column',
                          gap: 1,
                          borderRadius: 2,
                          borderWidth: 2,
                          borderColor: action.color,
                          color: action.color,
                          '&:hover': {
                            borderWidth: 2,
                            borderColor: action.color,
                            bgcolor: `${action.color}15`,
                            transform: 'translateY(-4px) scale(1.05)'
                          }
                        }}
                      >
                        <Typography variant="caption" textAlign="center" fontWeight={600}>
                          {action.label}
                        </Typography>
                      </Button>
                    </Zoom>
                  </Grid>
                ))}
              </Grid>
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" fontWeight={600} gutterBottom>
                🎯 Recent Activity
              </Typography>
              {achievements.map((achievement, index) => (
                <Fade in timeout={1000 + index * 200} key={index}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, p: 2, borderRadius: 2, bgcolor: 'grey.50', transition: 'all 0.3s', '&:hover': { bgcolor: 'grey.100', transform: 'translateX(8px)' } }}>
                    <Typography sx={{ fontSize: '2rem', mr: 2 }}>{achievement.icon}</Typography>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="body2" fontWeight={600}>
                        {achievement.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {achievement.time}
                      </Typography>
                    </Box>
                    <CheckCircleIcon sx={{ color: 'success.main' }} />
                  </Box>
                </Fade>
              ))}
            </Paper>
          </Fade>
        </Grid>

        {/* Stats Overview with Live Progress */}
        <Grid item xs={12} md={4}>
          <Fade in timeout={1400}>
            <Paper sx={{ p: 3, height: '100%' }} className="hover-lift">
              <Typography variant="h6" fontWeight={600} gutterBottom>
                📊 Live Overview
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" fontWeight={600}>Weekly Progress</Typography>
                  <Typography variant="body2" fontWeight={700} color="primary">75%</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={75} 
                  sx={{ 
                    height: 10, 
                    borderRadius: 5,
                    bgcolor: 'grey.200',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 5,
                      background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)'
                    }
                  }}
                  className="live-chart"
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" fontWeight={600}>AI Training</Typography>
                  <Typography variant="body2" fontWeight={700} color="success.main">92%</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={92} 
                  color="success"
                  sx={{ 
                    height: 10, 
                    borderRadius: 5,
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 5
                    }
                  }}
                  className="live-chart"
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Grid container spacing={2} sx={{ textAlign: 'center' }}>
                <Grid item xs={6}>
                  <Zoom in timeout={1600}>
                    <Box className="heartbeat-animation">
                      <Typography variant="h3" color="primary" fontWeight={700}>
                        12
                      </Typography>
                      <Typography variant="caption" color="text.secondary" fontWeight={600}>
                        Active Goals
                      </Typography>
                    </Box>
                  </Zoom>
                </Grid>
                <Grid item xs={6}>
                  <Zoom in timeout={1800}>
                    <Box className="heartbeat-animation">
                      <Typography variant="h3" color="success.main" fontWeight={700}>
                        85%
                      </Typography>
                      <Typography variant="caption" color="text.secondary" fontWeight={600}>
                        Success Rate
                      </Typography>
                    </Box>
                  </Zoom>
                </Grid>
              </Grid>
              
              <Button
                variant="contained"
                fullWidth
                startIcon={<InsightsIcon />}
                onClick={() => navigate('/progress')}
                className="flashy-button"
                sx={{ 
                  mt: 3,
                  py: 1.5,
                  fontWeight: 700,
                  background: 'linear-gradient(45deg, #667eea, #764ba2)',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #5a6fd8, #6a4190)'
                  }
                }}
              >
                View Full Analytics
              </Button>
            </Paper>
          </Fade>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
