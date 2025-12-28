/**
 * Schedule Page for PWA
 * Task 11.2: Mobile-web synchronization with cloud backend
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { addPendingAction } from '../../store/slices/syncSlice';
import './Schedule.css';

interface ScheduleEvent {
  id: string;
  title: string;
  description?: string;
  startTime: string;
  endTime: string;
  category: 'work' | 'health' | 'personal' | 'finance';
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
}

const Schedule: React.FC = () => {
  const dispatch = useDispatch();
  const { isOnline } = useSelector((state: RootState) => state.sync);
  const [events, setEvents] = useState<ScheduleEvent[]>([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'day' | 'week'>('day');

  const loadSchedule = useCallback(async () => {
    try {
      setLoading(true);
      
      if (isOnline) {
        // Load from API
        const response = await fetch(`/api/v1/schedule?date=${selectedDate}&view=${viewMode}`);
        if (response.ok) {
          const data = await response.json();
          setEvents(data.events || []);
          
          // Cache for offline use
          localStorage.setItem(`schedule_${selectedDate}`, JSON.stringify(data.events));
        }
      } else {
        // Load from cache when offline
        const cachedData = localStorage.getItem(`schedule_${selectedDate}`);
        if (cachedData) {
          setEvents(JSON.parse(cachedData));
        } else {
          // Show sample data if no cache
          setEvents(getSampleEvents());
        }
      }
    } catch (error) {
      console.error('Failed to load schedule:', error);
      
      // Fallback to cached data
      const cachedData = localStorage.getItem(`schedule_${selectedDate}`);
      if (cachedData) {
        setEvents(JSON.parse(cachedData));
      } else {
        setEvents(getSampleEvents());
      }
    } finally {
      setLoading(false);
    }
  }, [selectedDate, viewMode, isOnline]);

  useEffect(() => {
    loadSchedule();
  }, [loadSchedule]);

  const getSampleEvents = (): ScheduleEvent[] => [
    {
      id: '1',
      title: 'Morning Workout',
      description: 'Cardio and strength training',
      startTime: '07:00',
      endTime: '08:00',
      category: 'health',
      priority: 'high',
      status: 'pending',
    },
    {
      id: '2',
      title: 'Team Meeting',
      description: 'Weekly project sync',
      startTime: '10:00',
      endTime: '11:00',
      category: 'work',
      priority: 'medium',
      status: 'pending',
    },
    {
      id: '3',
      title: 'Budget Review',
      description: 'Monthly financial planning',
      startTime: '14:00',
      endTime: '15:00',
      category: 'finance',
      priority: 'high',
      status: 'pending',
    },
  ];

  const updateEventStatus = async (eventId: string, newStatus: ScheduleEvent['status']) => {
    const updatedEvents = events.map(event =>
      event.id === eventId ? { ...event, status: newStatus } : event
    );
    setEvents(updatedEvents);

    // Update cache immediately
    localStorage.setItem(`schedule_${selectedDate}`, JSON.stringify(updatedEvents));

    if (isOnline) {
      try {
        await fetch(`/api/v1/schedule/${eventId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: newStatus }),
        });
      } catch (error) {
        console.error('Failed to update event status:', error);
      }
    } else {
      // Store for offline sync
      dispatch(addPendingAction({
        type: 'schedule_update',
        data: { id: eventId, updates: { status: newStatus } },
        maxRetries: 3,
      }));
    }
  };

  const generateSchedule = async () => {
    try {
      if (isOnline) {
        const response = await fetch('/api/v1/schedule/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            date: selectedDate,
            preferences: { workHours: '9-17', breakDuration: 60 }
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setEvents(data.events || []);
          localStorage.setItem(`schedule_${selectedDate}`, JSON.stringify(data.events));
        }
      } else {
        // Generate basic schedule offline
        const generatedEvents = getSampleEvents();
        setEvents(generatedEvents);
        localStorage.setItem(`schedule_${selectedDate}`, JSON.stringify(generatedEvents));
        
        // Store generation request for sync
        dispatch(addPendingAction({
          type: 'schedule_update',
          data: { action: 'generate', date: selectedDate },
          maxRetries: 3,
        }));
      }
    } catch (error) {
      console.error('Failed to generate schedule:', error);
    }
  };

  const getCategoryColor = (category: ScheduleEvent['category']) => {
    const colors = {
      work: '#2196f3',
      health: '#4caf50',
      personal: '#ff9800',
      finance: '#9c27b0',
    };
    return colors[category];
  };

  const getPriorityIcon = (priority: ScheduleEvent['priority']) => {
    const icons = {
      low: '🔵',
      medium: '🟡',
      high: '🔴',
    };
    return icons[priority];
  };

  const getStatusIcon = (status: ScheduleEvent['status']) => {
    const icons = {
      pending: '⏳',
      in_progress: '🔄',
      completed: '✅',
      cancelled: '❌',
    };
    return icons[status];
  };

  if (loading) {
    return (
      <div className="schedule-loading">
        <div className="loading-spinner"></div>
        <p>Loading schedule...</p>
      </div>
    );
  }

  return (
    <div className="schedule-page">
      <div className="schedule-header">
        <h1>Schedule</h1>
        <div className="schedule-controls">
          <div className="view-toggle">
            <button 
              className={viewMode === 'day' ? 'active' : ''}
              onClick={() => setViewMode('day')}
            >
              Day
            </button>
            <button 
              className={viewMode === 'week' ? 'active' : ''}
              onClick={() => setViewMode('week')}
            >
              Week
            </button>
          </div>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="date-picker"
          />
          <button 
            className="generate-btn"
            onClick={generateSchedule}
          >
            🤖 Generate Schedule
          </button>
        </div>
      </div>

      {!isOnline && (
        <div className="offline-notice">
          <span className="offline-icon">📡</span>
          You're offline. Changes will sync when you're back online.
        </div>
      )}

      <div className="schedule-content">
        {events.length === 0 ? (
          <div className="empty-schedule">
            <div className="empty-icon">📅</div>
            <h3>No events scheduled</h3>
            <p>Generate a schedule or add events manually</p>
            <button className="generate-btn" onClick={generateSchedule}>
              Generate Schedule
            </button>
          </div>
        ) : (
          <div className="events-list">
            {events.map(event => (
              <div 
                key={event.id} 
                className={`event-card ${event.status}`}
                style={{ borderLeftColor: getCategoryColor(event.category) }}
              >
                <div className="event-header">
                  <div className="event-time">
                    {event.startTime} - {event.endTime}
                  </div>
                  <div className="event-meta">
                    <span className="priority-indicator">
                      {getPriorityIcon(event.priority)}
                    </span>
                    <span className="status-indicator">
                      {getStatusIcon(event.status)}
                    </span>
                  </div>
                </div>
                
                <div className="event-content">
                  <h3 className="event-title">{event.title}</h3>
                  {event.description && (
                    <p className="event-description">{event.description}</p>
                  )}
                  <div className="event-category">
                    <span 
                      className="category-badge"
                      style={{ backgroundColor: getCategoryColor(event.category) }}
                    >
                      {event.category}
                    </span>
                  </div>
                </div>

                <div className="event-actions">
                  {event.status === 'pending' && (
                    <>
                      <button 
                        className="action-btn start-btn"
                        onClick={() => updateEventStatus(event.id, 'in_progress')}
                      >
                        ▶️ Start
                      </button>
                      <button 
                        className="action-btn complete-btn"
                        onClick={() => updateEventStatus(event.id, 'completed')}
                      >
                        ✅ Complete
                      </button>
                    </>
                  )}
                  
                  {event.status === 'in_progress' && (
                    <button 
                      className="action-btn complete-btn"
                      onClick={() => updateEventStatus(event.id, 'completed')}
                    >
                      ✅ Complete
                    </button>
                  )}
                  
                  {(event.status === 'pending' || event.status === 'in_progress') && (
                    <button 
                      className="action-btn cancel-btn"
                      onClick={() => updateEventStatus(event.id, 'cancelled')}
                    >
                      ❌ Cancel
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="schedule-stats">
        <div className="stat-item">
          <span className="stat-label">Total Events:</span>
          <span className="stat-value">{events.length}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Completed:</span>
          <span className="stat-value">
            {events.filter(e => e.status === 'completed').length}
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">In Progress:</span>
          <span className="stat-value">
            {events.filter(e => e.status === 'in_progress').length}
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Pending:</span>
          <span className="stat-value">
            {events.filter(e => e.status === 'pending').length}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Schedule;