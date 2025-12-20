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
  LinearProgress,
  IconButton,
  Fab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Checkbox,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Schedule as ScheduleIcon,
  CloudUpload as UploadIcon,
  TrendingUp as ProgressIcon,
  Add as AddIcon,
  CheckCircle as CheckIcon,
  RadioButtonUnchecked as UncheckIcon,
  SmartToy as AIIcon,
  Analytics as AnalyticsIcon,
  Assignment as TaskIcon,
  Notifications as NotificationIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  dueDate: string;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([
    { id: '1', title: 'Complete AI model training', completed: false, priority: 'high', dueDate: '2024-12-21' },
    { id: '2', title: 'Review progress analytics', completed: true, priority: 'medium', dueDate: '2024-12-20' },
    { id: '3', title: 'Upload new dataset', completed: false, priority: 'low', dueDate: '2024-12-22' },
    { id: '4', title: 'Schedule team meeting', completed: false, priority: 'medium', dueDate: '2024-12-21' }
  ]);
  
  const [openTaskDialog, setOpenTaskDialog] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');

  const toggleTask = (taskId: string) => {
    setTasks(tasks.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const addTask = () => {
    if (newTaskTitle.trim()) {
      const newTask: Task = {
        id: Date.now().toString(),
        title: newTaskTitle,
        completed: false,
        priority: 'medium',
        dueDate: new Date().toISOString().split('T')[0]
      };
      setTasks([...tasks, newTask]);
      setNewTaskTitle('');
      setOpenTaskDialog(false);
    }
  };

  const completedTasks = tasks.filter(task => task.completed).length;
  const totalTasks = tasks.length;
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

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
            background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
            width: 56, 
            height: 56 
          }}>
            <AIIcon sx={{ fontSize: 32 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
              AI Personal Assistant
            </Typography>
            <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              Your intelligent productivity companion
            </Typography>
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton 
            sx={{ 
              background: 'rgba(255,255,255,0.2)', 
              color: 'white',
              '&:hover': { background: 'rgba(255,255,255,0.3)' }
            }}
          >
            <NotificationIcon />
          </IconButton>
          <IconButton 
            sx={{ 
              background: 'rgba(255,255,255,0.2)', 
              color: 'white',
              '&:hover': { background: 'rgba(255,255,255,0.3)' }
            }}
          >
            <SettingsIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            color: 'white',
            height: '100%'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TaskIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {totalTasks}
                  </Typography>
                  <Typography variant="body2">Total Tasks</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
            color: 'white',
            height: '100%'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <CheckIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {completedTasks}
                  </Typography>
                  <Typography variant="body2">Completed</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(45deg, #FF9800 30%, #FFC107 90%)',
            color: 'white',
            height: '100%'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <AnalyticsIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {Math.round(completionRate)}%
                  </Typography>
                  <Typography variant="body2">Completion Rate</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(45deg, #9C27B0 30%, #E91E63 90%)',
            color: 'white',
            height: '100%'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <ProgressIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {tasks.filter(t => !t.completed).length}
                  </Typography>
                  <Typography variant="body2">Pending</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Task Management */}
        <Grid item xs={12} md={8}>
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            height: '500px',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5" fontWeight="bold" color="primary">
                  Smart Task Manager
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => setOpenTaskDialog(true)}
                  sx={{
                    background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
                    boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)'
                  }}
                >
                  Add Task
                </Button>
              </Box>
              
              <LinearProgress 
                variant="determinate" 
                value={completionRate} 
                sx={{ 
                  mb: 3, 
                  height: 8, 
                  borderRadius: 4,
                  background: 'rgba(0,0,0,0.1)'
                }} 
              />
              
              <List sx={{ maxHeight: '350px', overflow: 'auto' }}>
                {tasks.map((task) => (
                  <ListItem
                    key={task.id}
                    sx={{
                      mb: 1,
                      borderRadius: 2,
                      background: task.completed ? 'rgba(76, 175, 80, 0.1)' : 'rgba(0,0,0,0.02)',
                      '&:hover': { background: 'rgba(0,0,0,0.05)' }
                    }}
                  >
                    <ListItemIcon>
                      <Checkbox
                        checked={task.completed}
                        onChange={() => toggleTask(task.id)}
                        icon={<UncheckIcon />}
                        checkedIcon={<CheckIcon sx={{ color: '#4CAF50' }} />}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography
                          sx={{
                            textDecoration: task.completed ? 'line-through' : 'none',
                            color: task.completed ? 'text.secondary' : 'text.primary',
                            fontWeight: task.completed ? 'normal' : 'medium'
                          }}
                        >
                          {task.title}
                        </Typography>
                      }
                      secondary={`Due: ${task.dueDate}`}
                    />
                    <Chip
                      label={task.priority}
                      size="small"
                      color={
                        task.priority === 'high' ? 'error' :
                        task.priority === 'medium' ? 'warning' : 'success'
                      }
                      variant="outlined"
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
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
                    startIcon={<ScheduleIcon />}
                    onClick={() => navigate('/schedule')}
                    sx={{
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      py: 2
                    }}
                  >
                    Schedule
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<UploadIcon />}
                    onClick={() => navigate('/upload')}
                    sx={{
                      background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
                      py: 2
                    }}
                  >
                    Upload
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<ProgressIcon />}
                    onClick={() => navigate('/progress')}
                    sx={{
                      background: 'linear-gradient(45deg, #9C27B0 30%, #E91E63 90%)',
                      py: 2
                    }}
                  >
                    View Progress
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* AI Insights */}
          <Card sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                AI Insights
              </Typography>
              <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
                Based on your activity patterns, here are some recommendations:
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  🎯 You're most productive in the morning
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  📈 Task completion rate improved by 15%
                </Typography>
                <Typography variant="body2">
                  ⚡ Consider breaking large tasks into smaller ones
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Add Task Dialog */}
      <Dialog open={openTaskDialog} onClose={() => setOpenTaskDialog(false)}>
        <DialogTitle>Add New Task</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Task Title"
            fullWidth
            variant="outlined"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTask()}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTaskDialog(false)}>Cancel</Button>
          <Button onClick={addTask} variant="contained">Add Task</Button>
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
        onClick={() => setOpenTaskDialog(true)}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
};

export default Dashboard;