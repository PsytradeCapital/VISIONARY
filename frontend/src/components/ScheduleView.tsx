import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Button,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import EventIcon from '@mui/icons-material/Event';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import PsychologyIcon from '@mui/icons-material/Psychology';
import AddIcon from '@mui/icons-material/Add';
import { scheduleAPI } from '../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`schedule-tabpanel-${index}`}
      aria-labelledby={`schedule-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const ScheduleView: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [schedules, setSchedules] = useState<any[]>([]);
  const [currentSchedule, setCurrentSchedule] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [generateDialogOpen, setGenerateDialogOpen] = useState(false);
  const [generatingSchedule, setGeneratingSchedule] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  useEffect(() => {
    loadUserSchedules();
  }, []);

  const loadUserSchedules = async () => {
    setLoading(true);
    try {
      const response = await scheduleAPI.getUserSchedules();
      setSchedules(response.data.schedules || []);
      
      // Load the most recent schedule if available
      if (response.data.schedules && response.data.schedules.length > 0) {
        const latestSchedule = response.data.schedules[0];
        const scheduleDetails = await scheduleAPI.getSchedule(latestSchedule.id);
        setCurrentSchedule(scheduleDetails.data);
      }
    } catch (error: any) {
      setError('Failed to load schedules');
      console.error('Error loading schedules:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSchedule = async (timeframe: string) => {
    setGeneratingSchedule(true);
    try {
      const response = await scheduleAPI.generateSchedule(timeframe, {
        start_date: new Date().toISOString()
      });
      
      setCurrentSchedule(response.data);
      setGenerateDialogOpen(false);
      setError('');
    } catch (error: any) {
      setError(`Failed to generate schedule: ${error.response?.data?.detail || 'Unknown error'}`);
    } finally {
      setGeneratingSchedule(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'health': return <FitnessCenterIcon />;
      case 'financial': return <AttachMoneyIcon />;
      case 'nutrition': return <RestaurantIcon />;
      case 'psychological': return <PsychologyIcon />;
      default: return <EventIcon />;
    }
  };

  const sampleSchedule = [
    {
      time: '6:00 AM',
      title: 'Morning Workout',
      category: 'health',
      description: 'Cardio and strength training',
      priority: 'high'
    },
    {
      time: '7:30 AM',
      title: 'Healthy Breakfast',
      category: 'nutrition',
      description: 'Protein-rich meal with fruits',
      priority: 'medium'
    },
    {
      time: '9:00 AM',
      title: 'Budget Review',
      category: 'financial',
      description: 'Review weekly expenses and savings',
      priority: 'high'
    },
    {
      time: '11:00 AM',
      title: 'Meditation Session',
      category: 'psychological',
      description: '15-minute mindfulness practice',
      priority: 'medium'
    }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Your Schedule
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        AI-generated personalized schedule based on your goals and preferences
      </Typography>

      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Today" />
            <Tab label="This Week" />
            <Tab label="This Month" />
          </Tabs>
        </Box>
        
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom>
                Today's Schedule
              </Typography>
              <List>
                {sampleSchedule.map((item, index) => (
                  <ListItem key={index} divider>
                    <ListItemIcon>
                      {getCategoryIcon(item.category)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1">
                            {item.time} - {item.title}
                          </Typography>
                          <Chip
                            label={item.priority}
                            size="small"
                            color={item.priority === 'high' ? 'error' : 'default'}
                          />
                        </Box>
                      }
                      secondary={item.description}
                    />
                  </ListItem>
                ))}
              </List>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Quick Actions
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={1}>
                    <Button variant="outlined" size="small">
                      Modify Schedule
                    </Button>
                    <Button variant="outlined" size="small">
                      Add New Task
                    </Button>
                    <Button variant="outlined" size="small">
                      View Alternatives
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <Typography variant="h6">
            Weekly Schedule (Coming Soon)
          </Typography>
          <Typography color="text.secondary">
            Your AI assistant is learning your patterns to create the perfect weekly schedule.
          </Typography>
        </TabPanel>
        
        <TabPanel value={tabValue} index={2}>
          <Typography variant="h6">
            Monthly Schedule (Coming Soon)
          </Typography>
          <Typography color="text.secondary">
            Long-term planning and goal tracking will be available here.
          </Typography>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default ScheduleView;