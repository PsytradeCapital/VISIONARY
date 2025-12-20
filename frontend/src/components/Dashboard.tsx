import React from 'react';
import { 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent,
  CardMedia,
  Button,
  Avatar,
  Chip,
  LinearProgress,
  IconButton,
  Divider
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PhotoLibraryIcon from '@mui/icons-material/PhotoLibrary';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import InsightsIcon from '@mui/icons-material/Insights';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import StarIcon from '@mui/icons-material/Star';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  // Professional feature cards based on top-rated design principles
  const mainFeatures = [
    {
      icon: <SmartToyIcon sx={{ fontSize: 32 }} />,
      title: 'AI Assistant',
      description: 'Upload your routines, goals, and visions to train your personal AI',
      action: 'Start Training',
      route: '/upload',
      color: 'info.main',
      bgGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      image: '/images/image4.jpeg',
      stats: { label: 'AI Powered', value: '100%' }
    },
    {
      icon: <CalendarTodayIcon sx={{ fontSize: 32 }} />,
      title: 'Smart Schedule',
      description: 'View your personalized daily, weekly, and monthly schedules',
      action: 'View Schedule',
      route: '/schedule',
      color: 'success.main',
      bgGradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
      image: '/images/image2.jpeg',
      stats: { label: 'Rating', value: '4.8★' }
    },
    {
      icon: <InsightsIcon sx={{ fontSize: 32 }} />,
      title: 'Progress Analytics',
      description: 'Monitor progress toward financial, health, and personal goals',
      action: 'View Analytics',
      route: '/progress',
      color: 'warning.main',
      bgGradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
      image: '/images/image3.jpeg',
      stats: { label: 'Goals Tracked', value: '12' }
    }
  ];

  // Quick action items
  const quickActions = [
    { icon: <UploadFileIcon />, label: 'Upload Data', route: '/upload' },
    { icon: <PhotoLibraryIcon />, label: 'Design Gallery', route: '/gallery' },
    { icon: <TrendingUpIcon />, label: 'View Progress', route: '/progress' },
    { icon: <CalendarTodayIcon />, label: 'Today\'s Schedule', route: '/schedule' }
  ];

  // Recent achievements
  const achievements = [
    { title: 'Morning Routine Completed', time: '2 hours ago', type: 'routine' },
    { title: 'Weekly Goal: 75% Complete', time: '1 day ago', type: 'goal' },
    { title: 'AI Training Updated', time: '3 days ago', type: 'ai' }
  ];

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
            Welcome to Visionary
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9, mb: 3, maxWidth: 600 }}>
            Your AI-powered personal scheduling assistant designed with professional aesthetics
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip 
              icon={<StarIcon />} 
              label="4.65★ Design Rating" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
            <Chip 
              label="19 Design Concepts" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
            <Chip 
              label="Professional UI" 
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} 
            />
          </Box>
        </Box>
        
        {/* Decorative elements */}
        <Box
          sx={{
            position: 'absolute',
            top: -50,
            right: -50,
            width: 200,
            height: 200,
            borderRadius: '50%',
            bgcolor: 'rgba(255,255,255,0.1)',
            zIndex: 1
          }}
        />
      </Box>

      <Grid container spacing={4}>
        {/* Main Feature Cards */}
        <Grid item xs={12}>
          <Typography variant="h5" fontWeight={600} gutterBottom sx={{ mb: 3 }}>
            🚀 Core Features
          </Typography>
          <Grid container spacing={3}>
            {mainFeatures.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card 
                  sx={{ 
                    height: '100%',
                    position: 'relative',
                    overflow: 'hidden',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
                    }
                  }}
                  onClick={() => navigate(feature.route)}
                >
                  {/* Background Image */}
                  <CardMedia
                    component="img"
                    height="120"
                    image={feature.image}
                    alt={feature.title}
                    sx={{ 
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      opacity: 0.1,
                      objectFit: 'cover'
                    }}
                  />
                  
                  {/* Gradient Overlay */}
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      height: 120,
                      background: feature.bgGradient,
                      opacity: 0.9
                    }}
                  />
                  
                  <CardContent sx={{ position: 'relative', zIndex: 2, pt: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar 
                        sx={{ 
                          bgcolor: 'white', 
                          color: feature.color,
                          mr: 2,
                          width: 56,
                          height: 56
                        }}
                      >
                        {feature.icon}
                      </Avatar>
                      <Box>
                        <Typography variant="h6" fontWeight={600} color="white">
                          {feature.title}
                        </Typography>
                        <Chip 
                          label={feature.stats.value} 
                          size="small"
                          sx={{ 
                            bgcolor: 'rgba(255,255,255,0.2)', 
                            color: 'white',
                            fontSize: '0.75rem'
                          }} 
                        />
                      </Box>
                    </Box>
                    
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: 'rgba(255,255,255,0.9)', 
                        mb: 3,
                        minHeight: 40
                      }}
                    >
                      {feature.description}
                    </Typography>
                    
                    <Button 
                      variant="contained"
                      fullWidth
                      endIcon={<ArrowForwardIcon />}
                      sx={{ 
                        bgcolor: 'white',
                        color: feature.color,
                        fontWeight: 600,
                        '&:hover': {
                          bgcolor: 'rgba(255,255,255,0.9)'
                        }
                      }}
                    >
                      {feature.action}
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Quick Actions & Recent Activity */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              ⚡ Quick Actions
            </Typography>
            <Grid container spacing={2}>
              {quickActions.map((action, index) => (
                <Grid item xs={6} sm={3} key={index}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={action.icon}
                    onClick={() => navigate(action.route)}
                    sx={{ 
                      py: 2,
                      flexDirection: 'column',
                      gap: 1,
                      borderRadius: 2,
                      '&:hover': {
                        transform: 'translateY(-2px)'
                      }
                    }}
                  >
                    <Typography variant="caption" textAlign="center">
                      {action.label}
                    </Typography>
                  </Button>
                </Grid>
              ))}
            </Grid>
            
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" fontWeight={600} gutterBottom>
              🎯 Recent Activity
            </Typography>
            {achievements.map((achievement, index) => (
              <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <CheckCircleIcon sx={{ color: 'success.main', mr: 2 }} />
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="body2" fontWeight={500}>
                    {achievement.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {achievement.time}
                  </Typography>
                </Box>
              </Box>
            ))}
          </Paper>
        </Grid>

        {/* Stats Overview */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              📊 Overview
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2">Weekly Progress</Typography>
                <Typography variant="body2" fontWeight={600}>75%</Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={75} 
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>
            
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2">AI Training</Typography>
                <Typography variant="body2" fontWeight={600}>92%</Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={92} 
                color="info"
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Grid container spacing={2} sx={{ textAlign: 'center' }}>
              <Grid item xs={6}>
                <Typography variant="h4" color="primary" fontWeight={700}>
                  19
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Design Concepts
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="h4" color="success.main" fontWeight={700}>
                  4.6
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Avg Rating
                </Typography>
              </Grid>
            </Grid>
            
            <Button
              variant="outlined"
              fullWidth
              startIcon={<PhotoLibraryIcon />}
              onClick={() => navigate('/gallery')}
              sx={{ mt: 3 }}
            >
              Explore Gallery
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;