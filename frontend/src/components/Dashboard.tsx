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
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PhotoLibraryIcon from '@mui/icons-material/PhotoLibrary';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  // Featured images for the dashboard
  const featuredImages = [
    {
      src: '/images/image2.jpeg',
      title: 'AI-Powered Scheduling',
      description: 'Intelligent schedule planning'
    },
    {
      src: '/images/image3.jpeg',
      title: 'Progress Tracking',
      description: 'Visual goal monitoring'
    },
    {
      src: '/images/image4.jpeg',
      title: 'Personal Assistant',
      description: 'Your AI companion'
    }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to Visionary
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Your AI-powered personal scheduling assistant
      </Typography>

      <Grid container spacing={3}>
        {/* Main Action Cards */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <UploadFileIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Upload Data</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                Upload your routines, goals, and visions to train your AI assistant
              </Typography>
              <Button 
                variant="contained" 
                onClick={() => navigate('/upload')}
                fullWidth
              >
                Start Uploading
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <CalendarTodayIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">View Schedule</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                See your personalized daily, weekly, and monthly schedules
              </Typography>
              <Button 
                variant="contained" 
                onClick={() => navigate('/schedule')}
                fullWidth
              >
                View Schedule
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Track Progress</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                Monitor your progress toward financial, health, and personal goals
              </Typography>
              <Button 
                variant="contained" 
                onClick={() => navigate('/progress')}
                fullWidth
              >
                View Progress
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Featured Design Gallery */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, mt: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
              <Box>
                <Typography variant="h5" gutterBottom>
                  🎨 Design Inspiration
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Explore the visual concepts behind Visionary
                </Typography>
              </Box>
              <Button
                variant="outlined"
                startIcon={<PhotoLibraryIcon />}
                onClick={() => navigate('/gallery')}
              >
                View Gallery
              </Button>
            </Box>
            
            <Grid container spacing={2}>
              {featuredImages.map((image, index) => (
                <Grid item xs={12} sm={4} key={index}>
                  <Card sx={{ height: '100%' }}>
                    <CardMedia
                      component="img"
                      height="160"
                      image={image.src}
                      alt={image.title}
                      sx={{ objectFit: 'cover' }}
                    />
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {image.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {image.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, mt: 2 }}>
            <Typography variant="h5" gutterBottom>
              📊 Quick Stats
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h3" color="primary">
                    19
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Design Concepts
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h3" color="success.main">
                    4.6
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Average Rating
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h3" color="warning.main">
                    8
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Categories
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Box textAlign="center">
                  <Typography variant="h3" color="info.main">
                    100%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI-Powered
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;