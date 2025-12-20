import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Fab,
  Paper,
  Divider
} from '@mui/material';
import {
  Schedule as ScheduleIcon,
  Add as AddIcon,
  Event as EventIcon,
  AccessTime as TimeIcon,
  Person as PersonIcon,
  LocationOn as LocationIcon,
  Videocam as VideoIcon,
  Phone as PhoneIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  SmartToy as AIIcon,
  CalendarToday as CalendarIcon,
  Notifications as NotificationIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface ScheduleEvent {
  id: string;
  title: string;
  time: string;
  duration: string;
  type: 'meeting' | 'task' | 'reminder' | 'call';
  priority: 'high' | 'medium' | 'low';
  attendees?: string[];
  location?: string;
  description?: string;
}

const ScheduleView: React.FC = () => {
  const navigate = useNavigate();
  const [events, setEvents] = useState<ScheduleEvent[]>([
    {
      id: '1',
      title: 'AI Model Review Meeting',
      time: '09:00',
      duration: '1h',
      type: 'meeting',
      priority: 'high',
      attendees: ['John Doe', 'Jane Smith'],
      location: 'Conference Room A'
    },
    {
      id: '2',
      title: 'Data Analysis Task',
      time: '11:30',
      duration: '2h',
      type: 'task',
      priority: 'medium',
      description: 'Analyze user behavior patterns'
    },
    {
      id: '3',
      title: 'Client Call - Project Update',
      time: '14:00',
      duration: '30m',
      type: 'call',
      priority: 'high',
      attendees: ['Client Team']
    },
    {
      id: '4',
      title: 'Weekly Progress Review',
      time: '16:00',
      duration: '45m',
      type: 'meeting',
      priority: 'medium',
      location: 'Virtual Meeting'
    }
  ]);

  const [openEventDialog, setOpenEventDialog] = useState(false);
  const [newEvent, setNewEvent] = useState<Partial<ScheduleEvent>>({
    title: '',
    time: '',
    duration: '1h',
    type: 'meeting',
    priority: 'medium'
  });

  const addEvent = () => {
    if (newEvent.title && newEvent.time) {
      const event: ScheduleEvent = {
        id: Date.now().toString(),
        title: newEvent.title,
        time: newEvent.time,
        duration: newEvent.duration || '1h',
        type: newEvent.type || 'meeting',
        priority: newEvent.priority || 'medium'
      };
      setEvents([...events, event]);
      setNewEvent({ title: '', time: '', duration: '1h', type: 'meeting', priority: 'medium' });
      setOpenEventDialog(false);
    }
  };

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'meeting': return <EventIcon />;
      case 'call': return <PhoneIcon />;
      case 'task': return <ScheduleIcon />;
      default: return <NotificationIcon />;
    }
  };

  const getEventColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#f44336';
      case 'medium': return '#ff9800';
      case 'low': return '#4caf50';
      default: return '#2196f3';
    }
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
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            width: 56, 
            height: 56 
          }}>
            <CalendarIcon sx={{ fontSize: 32 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
              Smart Schedule
            </Typography>
            <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              AI-powered calendar management
            </Typography>
          </Box>
        </Box>
        
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenEventDialog(true)}
          sx={{
            background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
            boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
            px: 3,
            py: 1.5
          }}
        >
          Schedule Event
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Today's Schedule */}
        <Grid item xs={12} md={8}>
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            height: '600px',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" fontWeight="bold" color="primary">
                  Today's Schedule
                </Typography>
                <Chip 
                  label={`${events.length} Events`} 
                  color="primary" 
                  variant="outlined"
                />
              </Box>
              
              <List sx={{ maxHeight: '500px', overflow: 'auto' }}>
                {events.map((event, index) => (
                  <React.Fragment key={event.id}>
                    <ListItem
                      sx={{
                        mb: 2,
                        borderRadius: 2,
                        background: `linear-gradient(90deg, ${getEventColor(event.priority)}15 0%, transparent 100%)`,
                        border: `2px solid ${getEventColor(event.priority)}20`,
                        '&:hover': { 
                          background: `linear-gradient(90deg, ${getEventColor(event.priority)}25 0%, transparent 100%)`,
                          transform: 'translateX(5px)',
                          transition: 'all 0.3s ease'
                        }
                      }}
                    >
                      <ListItemIcon>
                        <Avatar sx={{ 
                          background: getEventColor(event.priority),
                          width: 48,
                          height: 48
                        }}>
                          {getEventIcon(event.type)}
                        </Avatar>
                      </ListItemIcon>
                      
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                            <Typography variant="h6" fontWeight="bold">
                              {event.title}
                            </Typography>
                            <Chip 
                              label={event.type} 
                              size="small" 
                              sx={{ 
                                background: getEventColor(event.priority),
                                color: 'white',
                                fontWeight: 'bold'
                              }}
                            />
                          </Box>
                        }
                        secondary={
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <TimeIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                                <Typography variant="body2">
                                  {event.time} ({event.duration})
                                </Typography>
                              </Box>
                              {event.location && (
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <LocationIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                                  <Typography variant="body2">
                                    {event.location}
                                  </Typography>
                                </Box>
                              )}
                            </Box>
                            {event.attendees && (
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <PersonIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                                <Typography variant="body2">
                                  {event.attendees.join(', ')}
                                </Typography>
                              </Box>
                            )}
                          </Box>
                        }
                      />
                      
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                        <IconButton size="small" sx={{ color: getEventColor(event.priority) }}>
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small" sx={{ color: 'text.secondary' }}>
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </ListItem>
                    {index < events.length - 1 && <Divider sx={{ my: 1 }} />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Insights & Quick Actions */}
        <Grid item xs={12} md={4}>
          {/* AI Schedule Insights */}
          <Card sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <AIIcon sx={{ fontSize: 32 }} />
                <Typography variant="h6" fontWeight="bold">
                  AI Schedule Insights
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  📊 You have 4 events scheduled today
                </Typography>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  ⚡ Peak productivity time: 9-11 AM
                </Typography>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  🎯 2 high-priority meetings require prep
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  💡 Suggested 15min break at 12:30 PM
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                Quick Actions
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<VideoIcon />}
                    sx={{
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      py: 2
                    }}
                  >
                    Join Meeting
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<PhoneIcon />}
                    sx={{
                      background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
                      py: 2
                    }}
                  >
                    Quick Call
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AIIcon />}
                    onClick={() => navigate('/progress')}
                    sx={{ py: 2 }}
                  >
                    View Analytics
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Upcoming Events */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                Next Up
              </Typography>
              
              <Box sx={{ 
                p: 2, 
                borderRadius: 2, 
                background: 'linear-gradient(45deg, #FE6B8B15 30%, #FF8E5315 90%)',
                border: '2px solid #FE6B8B30'
              }}>
                <Typography variant="subtitle1" fontWeight="bold">
                  AI Model Review Meeting
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Starting in 15 minutes
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Conference Room A
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Add Event Dialog */}
      <Dialog open={openEventDialog} onClose={() => setOpenEventDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Schedule New Event</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Event Title"
                value={newEvent.title}
                onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Time"
                type="time"
                value={newEvent.time}
                onChange={(e) => setNewEvent({ ...newEvent, time: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Duration</InputLabel>
                <Select
                  value={newEvent.duration}
                  onChange={(e) => setNewEvent({ ...newEvent, duration: e.target.value })}
                >
                  <MenuItem value="15m">15 minutes</MenuItem>
                  <MenuItem value="30m">30 minutes</MenuItem>
                  <MenuItem value="1h">1 hour</MenuItem>
                  <MenuItem value="2h">2 hours</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Type</InputLabel>
                <Select
                  value={newEvent.type}
                  onChange={(e) => setNewEvent({ ...newEvent, type: e.target.value as any })}
                >
                  <MenuItem value="meeting">Meeting</MenuItem>
                  <MenuItem value="call">Call</MenuItem>
                  <MenuItem value="task">Task</MenuItem>
                  <MenuItem value="reminder">Reminder</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Priority</InputLabel>
                <Select
                  value={newEvent.priority}
                  onChange={(e) => setNewEvent({ ...newEvent, priority: e.target.value as any })}
                >
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEventDialog(false)}>Cancel</Button>
          <Button onClick={addEvent} variant="contained">Schedule Event</Button>
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
        onClick={() => setOpenEventDialog(true)}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
};

export default ScheduleView;