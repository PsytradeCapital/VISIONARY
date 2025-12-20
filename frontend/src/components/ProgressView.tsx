import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  LinearProgress,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Fab,
  Paper
} from '@mui/material';
import {
  TrendingUp as ProgressIcon,
  EmojiEvents as AchievementIcon,
  Timeline as TimelineIcon,
  Assessment as AnalyticsIcon,
  TrackChanges as GoalIcon,
  Star as StarIcon,
  CheckCircle as CheckIcon,
  Schedule as ScheduleIcon,
  SmartToy as AIIcon,
  Add as AddIcon,
  Insights as InsightsIcon,
  Psychology as PsychologyIcon,
  FitnessCenter as FitnessIcon,
  School as LearningIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Goal {
  id: string;
  title: string;
  category: 'fitness' | 'learning' | 'productivity' | 'personal';
  progress: number;
  target: number;
  unit: string;
  deadline: string;
  status: 'active' | 'completed' | 'paused';
}

interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  unlockedDate: string;
  category: string;
}

const ProgressView: React.FC = () => {
  const navigate = useNavigate();
  const [goals, setGoals] = useState<Goal[]>([
    {
      id: '1',
      title: 'Complete AI Course',
      category: 'learning',
      progress: 75,
      target: 100,
      unit: '%',
      deadline: '2024-12-31',
      status: 'active'
    },
    {
      id: '2',
      title: 'Daily Workout',
      category: 'fitness',
      progress: 18,
      target: 30,
      unit: 'days',
      deadline: '2024-12-31',
      status: 'active'
    },
    {
      id: '3',
      title: 'Read Books',
      category: 'personal',
      progress: 8,
      target: 12,
      unit: 'books',
      deadline: '2024-12-31',
      status: 'active'
    },
    {
      id: '4',
      title: 'Project Tasks',
      category: 'productivity',
      progress: 45,
      target: 60,
      unit: 'tasks',
      deadline: '2024-12-25',
      status: 'active'
    }
  ]);

  const [achievements, setAchievements] = useState<Achievement[]>([
    {
      id: '1',
      title: 'Early Bird',
      description: 'Completed 7 morning tasks in a row',
      icon: '🌅',
      unlockedDate: '2024-12-15',
      category: 'productivity'
    },
    {
      id: '2',
      title: 'Learning Streak',
      description: 'Studied for 14 consecutive days',
      icon: '📚',
      unlockedDate: '2024-12-10',
      category: 'learning'
    },
    {
      id: '3',
      title: 'Fitness Champion',
      description: 'Completed 10 workout sessions',
      icon: '💪',
      unlockedDate: '2024-12-08',
      category: 'fitness'
    }
  ]);

  const [openGoalDialog, setOpenGoalDialog] = useState(false);
  const [newGoal, setNewGoal] = useState({
    title: '',
    category: 'productivity' as const,
    target: 0,
    unit: '',
    deadline: ''
  });

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'fitness': return <FitnessIcon />;
      case 'learning': return <LearningIcon />;
      case 'productivity': return <ScheduleIcon />;
      case 'personal': return <PsychologyIcon />;
      default: return <GoalIcon />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'fitness': return '#f44336';
      case 'learning': return '#2196f3';
      case 'productivity': return '#4caf50';
      case 'personal': return '#ff9800';
      default: return '#9e9e9e';
    }
  };

  const addGoal = () => {
    if (newGoal.title && newGoal.target && newGoal.unit && newGoal.deadline) {
      const goal: Goal = {
        id: Date.now().toString(),
        title: newGoal.title,
        category: newGoal.category,
        progress: 0,
        target: newGoal.target,
        unit: newGoal.unit,
        deadline: newGoal.deadline,
        status: 'active'
      };
      setGoals([...goals, goal]);
      setNewGoal({ title: '', category: 'productivity', target: 0, unit: '', deadline: '' });
      setOpenGoalDialog(false);
    }
  };

  const overallProgress = Math.round(
    goals.reduce((sum, goal) => sum + (goal.progress / goal.target) * 100, 0) / goals.length
  );

  const completedGoals = goals.filter(goal => goal.progress >= goal.target).length;
  const activeGoals = goals.filter(goal => goal.status === 'active').length;

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
            background: 'linear-gradient(45deg, #9C27B0 30%, #E91E63 90%)',
            width: 56, 
            height: 56 
          }}>
            <ProgressIcon sx={{ fontSize: 32 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
              Progress Analytics
            </Typography>
            <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              AI-powered goal tracking and insights
            </Typography>
          </Box>
        </Box>
        
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenGoalDialog(true)}
          sx={{
            background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
            boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
            px: 3,
            py: 1.5
          }}
        >
          New Goal
        </Button>
      </Box>

      {/* Progress Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            color: 'white',
            height: '100%'
          }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <CircularProgress
                variant="determinate"
                value={overallProgress}
                size={80}
                thickness={6}
                sx={{ 
                  color: 'white',
                  mb: 2,
                  '& .MuiCircularProgress-circle': {
                    strokeLinecap: 'round'
                  }
                }}
              />
              <Typography variant="h4" fontWeight="bold">
                {overallProgress}%
              </Typography>
              <Typography variant="body2">Overall Progress</Typography>
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
                    {completedGoals}
                  </Typography>
                  <Typography variant="body2">Goals Completed</Typography>
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
                <GoalIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {activeGoals}
                  </Typography>
                  <Typography variant="body2">Active Goals</Typography>
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
                <AchievementIcon sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {achievements.length}
                  </Typography>
                  <Typography variant="body2">Achievements</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Goals Progress */}
        <Grid item xs={12} md={8}>
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            height: '600px',
            overflow: 'hidden'
          }}>
            <CardContent>
              <Typography variant="h5" fontWeight="bold" color="primary" gutterBottom>
                Goal Progress
              </Typography>
              
              <List sx={{ maxHeight: '520px', overflow: 'auto' }}>
                {goals.map((goal) => (
                  <ListItem
                    key={goal.id}
                    sx={{
                      mb: 2,
                      borderRadius: 2,
                      background: `linear-gradient(90deg, ${getCategoryColor(goal.category)}15 0%, transparent 100%)`,
                      border: `2px solid ${getCategoryColor(goal.category)}20`,
                      '&:hover': { 
                        background: `linear-gradient(90deg, ${getCategoryColor(goal.category)}25 0%, transparent 100%)`,
                        transform: 'translateX(5px)',
                        transition: 'all 0.3s ease'
                      }
                    }}
                  >
                    <ListItemIcon>
                      <Avatar sx={{ 
                        background: getCategoryColor(goal.category),
                        width: 48,
                        height: 48
                      }}>
                        {getCategoryIcon(goal.category)}
                      </Avatar>
                    </ListItemIcon>
                    
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                          <Typography variant="h6" fontWeight="bold">
                            {goal.title}
                          </Typography>
                          <Chip 
                            label={goal.category} 
                            size="small" 
                            sx={{ 
                              background: getCategoryColor(goal.category),
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2">
                              {goal.progress} / {goal.target} {goal.unit}
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {Math.round((goal.progress / goal.target) * 100)}%
                            </Typography>
                          </Box>
                          <LinearProgress 
                            variant="determinate" 
                            value={(goal.progress / goal.target) * 100} 
                            sx={{ 
                              height: 8, 
                              borderRadius: 4,
                              backgroundColor: 'rgba(0,0,0,0.1)',
                              '& .MuiLinearProgress-bar': {
                                backgroundColor: getCategoryColor(goal.category)
                              }
                            }}
                          />
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                            Deadline: {new Date(goal.deadline).toLocaleDateString()}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Insights & Achievements */}
        <Grid item xs={12} md={4}>
          {/* AI Insights */}
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
                  AI Insights
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  🎯 You're 25% ahead of schedule on learning goals
                </Typography>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  💪 Fitness consistency improved by 40% this month
                </Typography>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  📈 Productivity peaks between 9-11 AM
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  🏆 On track to unlock 3 new achievements this week
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Recent Achievements */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3,
            mb: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                Recent Achievements
              </Typography>
              
              <List sx={{ maxHeight: '200px', overflow: 'auto' }}>
                {achievements.map((achievement) => (
                  <ListItem
                    key={achievement.id}
                    sx={{
                      mb: 1,
                      borderRadius: 2,
                      background: 'linear-gradient(45deg, #FFD70015 30%, #FFA50015 90%)',
                      border: '2px solid #FFD70030'
                    }}
                  >
                    <ListItemIcon>
                      <Typography sx={{ fontSize: 32 }}>
                        {achievement.icon}
                      </Typography>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle2" fontWeight="bold">
                          {achievement.title}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="body2" color="text.secondary">
                          {achievement.description}
                        </Typography>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card sx={{ 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 3
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" color="primary" gutterBottom>
                Quick Actions
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<InsightsIcon />}
                    sx={{
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      py: 2
                    }}
                  >
                    Detailed Analytics
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<ScheduleIcon />}
                    onClick={() => navigate('/schedule')}
                    sx={{ py: 2 }}
                  >
                    Schedule
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<TimelineIcon />}
                    sx={{ py: 2 }}
                  >
                    Timeline
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Add Goal Dialog */}
      <Dialog open={openGoalDialog} onClose={() => setOpenGoalDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Goal</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Goal Title"
                value={newGoal.title}
                onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                select
                label="Category"
                value={newGoal.category}
                onChange={(e) => setNewGoal({ ...newGoal, category: e.target.value as any })}
                SelectProps={{ native: true }}
              >
                <option value="productivity">Productivity</option>
                <option value="fitness">Fitness</option>
                <option value="learning">Learning</option>
                <option value="personal">Personal</option>
              </TextField>
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Target"
                value={newGoal.target}
                onChange={(e) => setNewGoal({ ...newGoal, target: parseInt(e.target.value) })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Unit"
                value={newGoal.unit}
                onChange={(e) => setNewGoal({ ...newGoal, unit: e.target.value })}
                placeholder="e.g., days, books, tasks"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="date"
                label="Deadline"
                value={newGoal.deadline}
                onChange={(e) => setNewGoal({ ...newGoal, deadline: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenGoalDialog(false)}>Cancel</Button>
          <Button onClick={addGoal} variant="contained">Create Goal</Button>
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
        onClick={() => setOpenGoalDialog(true)}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
};

export default ProgressView;