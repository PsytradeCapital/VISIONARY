/**
 * Dashboard Page for PWA
 * Task 11.1: PWA with service workers for offline functionality
 */

import React, { useEffect, useState, useCallback } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { performBackgroundSync } from '../../store/slices/syncSlice';
import './Dashboard.css';

interface DashboardStats {
  totalTasks: number;
  completedTasks: number;
  upcomingEvents: number;
  progressScore: number;
}

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { isOnline, pendingActions, lastSyncTime } = useSelector((state: RootState) => state.sync);
  const [stats, setStats] = useState<DashboardStats>({
    totalTasks: 0,
    completedTasks: 0,
    upcomingEvents: 0,
    progressScore: 0,
  });
  const [loading, setLoading] = useState(true);

  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true);
      
      if (isOnline) {
        // Load from API
        const response = await fetch('/api/v1/dashboard/stats');
        if (response.ok) {
          const data = await response.json();
          setStats(data);
          
          // Cache data for offline use
          localStorage.setItem('dashboardStats', JSON.stringify(data));
        }
      } else {
        // Load from cache when offline
        const cachedData = localStorage.getItem('dashboardStats');
        if (cachedData) {
          setStats(JSON.parse(cachedData));
        }
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      
      // Fallback to cached data
      const cachedData = localStorage.getItem('dashboardStats');
      if (cachedData) {
        setStats(JSON.parse(cachedData));
      }
    } finally {
      setLoading(false);
    }
  }, [isOnline]);

  useEffect(() => {
    loadDashboardData();
    
    // Set up periodic sync when online
    if (isOnline) {
      const syncInterval = setInterval(() => {
        // @ts-ignore
        dispatch(performBackgroundSync());
      }, 30000); // 30 seconds

      return () => clearInterval(syncInterval);
    }
  }, [isOnline, dispatch, loadDashboardData]);

  const handleRefresh = () => {
    if (isOnline) {
      loadDashboardData();
      // @ts-ignore
      dispatch(performBackgroundSync());
    }
  };

  const formatLastSync = (timestamp: string | null) => {
    if (!timestamp) return 'Never';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="dashboard-status">
          <div className={`connection-status ${isOnline ? 'online' : 'offline'}`}>
            <span className="status-indicator"></span>
            {isOnline ? 'Online' : 'Offline'}
          </div>
          {pendingActions.length > 0 && (
            <div className="pending-sync">
              {pendingActions.length} pending sync{pendingActions.length !== 1 ? 's' : ''}
            </div>
          )}
        </div>
      </div>

      <div className="dashboard-actions">
        <button 
          className="refresh-btn" 
          onClick={handleRefresh}
          disabled={!isOnline}
        >
          <span className="refresh-icon">↻</span>
          Refresh
        </button>
        <div className="last-sync">
          Last sync: {formatLastSync(lastSyncTime)}
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <h3>Total Tasks</h3>
            <div className="stat-value">{stats.totalTasks}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Completed</h3>
            <div className="stat-value">{stats.completedTasks}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Upcoming</h3>
            <div className="stat-value">{stats.upcomingEvents}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Progress</h3>
            <div className="stat-value">{stats.progressScore}%</div>
          </div>
        </div>
      </div>

      <div className="dashboard-sections">
        <section className="recent-activity">
          <h2>Recent Activity</h2>
          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-icon">📝</div>
              <div className="activity-content">
                <p>Uploaded new document</p>
                <span className="activity-time">2 hours ago</span>
              </div>
            </div>
            <div className="activity-item">
              <div className="activity-icon">✅</div>
              <div className="activity-content">
                <p>Completed morning workout</p>
                <span className="activity-time">4 hours ago</span>
              </div>
            </div>
            <div className="activity-item">
              <div className="activity-icon">🎯</div>
              <div className="activity-content">
                <p>Achieved weekly goal</p>
                <span className="activity-time">1 day ago</span>
              </div>
            </div>
          </div>
        </section>

        <section className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-buttons">
            <button className="action-btn">
              <span className="action-icon">📤</span>
              Upload Content
            </button>
            <button className="action-btn">
              <span className="action-icon">📅</span>
              View Schedule
            </button>
            <button className="action-btn">
              <span className="action-icon">📊</span>
              Check Progress
            </button>
          </div>
        </section>
      </div>

      {!isOnline && (
        <div className="offline-banner">
          <div className="offline-content">
            <span className="offline-icon">📡</span>
            <div>
              <p><strong>You're offline</strong></p>
              <p>Some features may be limited. Changes will sync when you're back online.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;