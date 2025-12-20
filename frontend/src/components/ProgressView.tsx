import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import PsychologyIcon from '@mui/icons-material/Psychology';
import { progressAPI } from '../services/api';

interface ProgressCardProps {
  title: string;
  icon: React.ReactNode;
  progress: number;
  description: string;
  color: string;
}

const ProgressCard: React.FC<ProgressCardProps> = ({ 
  title, 
  icon, 
  progress, 
  description,
  color 
}) => {
  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box sx={{ color, mr: 1 }}>
            {icon}
          </Box>
          <Typography variant="h6">{title}</Typography>
        </Box>
        
        <Box mb={2}>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <Typography variant="body2" color="text.secondary">
              Progress
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {progress}%
            </Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={progress} 
            sx={{ height: 8, borderRadius: 4 }}
          />
        </Box>
        
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
};

const ProgressView: React.FC = () => {
  const [progressData, setProgressData] = useState<any>(null);
  const [achievements, setAchievements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadProgressData();
    loadAchievements();
  }, []);

  const loadProgressData = async () => {
    try {
      const response = await progressAPI.getOverview();
      if (response.success) {
        setProgressData(response.data);
      }
    } catch (error: any) {
      console.error('Error loading progress data:', error);
      setError('Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  const loadAchievements = async () => {
    try {
      const response = await progressAPI.getAchievements();
      if (response.success) {
        setAchievements(response.data);
      }
    } catch (error: any) {
      console.error('Error loading achievements:', error);
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'health': return <FitnessCenterIcon fontSize="large" />;
      case 'financial': return <AttachMoneyIcon fontSize="large" />;
      case 'nutrition': return <RestaurantIcon fontSize="large" />;
      case 'psychological': return <PsychologyIcon fontSize="large" />;
      default: return <FitnessCenterIcon fontSize="large" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'health': return '#4caf50';
      case 'financial': return '#2196f3';
      case 'nutrition': return '#ff9800';
      case 'psychological': return '#9c27b0';
      default: return '#4caf50';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  // Use real data if available, otherwise fall back to sample data
  const categoryData = progressData?.progress_by_category || {
    health: { average_progress: 75, completed_tasks: 15 },
    financial: { average_progress: 60, completed_tasks: 8 },
    nutrition: { average_progress: 85, completed_tasks: 20 },
    psychological: { average_progress: 70, completed_tasks: 14 }
  };

  const displayData = Object.entries(categoryData).map(([category, data]: [string, any]) => ({
    title: `${category.charAt(0).toUpperCase() + category.slice(1)} Goals`,
    icon: getCategoryIcon(category),
    progress: data.average_progress || 0,
    description: `Completed ${data.completed_tasks || 0} tasks`,
    color: getCategoryColor(category)
  }));

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Progress Tracking
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Monitor your achievements across all vision categories
      </Typography>

      <Grid container spacing={3}>
        {displayData.map((data, index) => (
          <Grid item xs={12} md={6} key={index}>
            <ProgressCard {...data} />
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Achievements
        </Typography>
        <Box>
          {achievements.length > 0 ? (
            achievements.map((achievement, index) => (
              <Typography key={index} variant="body2" color="text.secondary" paragraph>
                {achievement.icon} {achievement.title}
              </Typography>
            ))
          ) : (
            <>
              <Typography variant="body2" color="text.secondary" paragraph>
                🎉 Completed 7-day workout streak!
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                💰 Exceeded savings goal for 2 consecutive weeks
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                🧘 Maintained daily meditation practice for 14 days
              </Typography>
              <Typography variant="body2" color="text.secondary">
                🥗 Prepared healthy meals 20 times this month
              </Typography>
            </>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default ProgressView;