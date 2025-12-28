/**
 * Analytics Page for PWA
 * Task 11.1: PWA with service workers for offline functionality
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';
import './Analytics.css';

interface AnalyticsData {
  progressScore: number;
  completionRate: number;
  streakDays: number;
  totalTasks: number;
  categoryBreakdown: {
    work: number;
    health: number;
    personal: number;
    finance: number;
  };
  weeklyProgress: number[];
  insights: string[];
}

const Analytics: React.FC = () => {
  const { isOnline } = useSelector((state: RootState) => state.sync);
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState<'week' | 'month' | 'year'>('week');

  const loadAnalytics = useCallback(async () => {
    try {
      setLoading(true);
      
      if (isOnline) {
        // Load from API
        const response = await fetch(`/api/v1/analytics?timeframe=${timeframe}`);
        if (response.ok) {
          const analyticsData = await response.json();
          setData(analyticsData);
          
          // Cache for offline use
          localStorage.setItem(`analytics_${timeframe}`, JSON.stringify(analyticsData));
        }
      } else {
        // Load from cache when offline
        const cachedData = localStorage.getItem(`analytics_${timeframe}`);
        if (cachedData) {
          setData(JSON.parse(cachedData));
        } else {
          // Show sample data if no cache
          setData(getSampleAnalytics());
        }
      }
    } catch (error) {
      console.error('Failed to load analytics:', error);
      
      // Fallback to cached data or sample data
      const cachedData = localStorage.getItem(`analytics_${timeframe}`);
      if (cachedData) {
        setData(JSON.parse(cachedData));
      } else {
        setData(getSampleAnalytics());
      }
    } finally {
      setLoading(false);
    }
  }, [timeframe, isOnline]);

  useEffect(() => {
    loadAnalytics();
  }, [loadAnalytics]);

  const getSampleAnalytics = (): AnalyticsData => ({
    progressScore: 78,
    completionRate: 85,
    streakDays: 12,
    totalTasks: 156,
    categoryBreakdown: {
      work: 45,
      health: 25,
      personal: 20,
      finance: 10,
    },
    weeklyProgress: [65, 72, 68, 78, 82, 75, 78],
    insights: [
      "You're most productive on Tuesday mornings",
      "Health goals show consistent improvement",
      "Consider scheduling finance tasks earlier in the day"
    ],
  });

  const getCategoryColor = (category: keyof AnalyticsData['categoryBreakdown']) => {
    const colors = {
      work: '#2196f3',
      health: '#4caf50',
      personal: '#ff9800',
      finance: '#9c27b0',
    };
    return colors[category];
  };

  const renderProgressChart = () => {
    if (!data) return null;

    const maxValue = Math.max(...data.weeklyProgress);
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

    return (
      <div className="progress-chart">
        <h3>Weekly Progress</h3>
        <div className="chart-container">
          {data.weeklyProgress.map((value, index) => (
            <div key={index} className="chart-bar">
              <div 
                className="bar-fill"
                style={{ 
                  height: `${(value / maxValue) * 100}%`,
                  backgroundColor: '#ff6b35'
                }}
              ></div>
              <div className="bar-label">{days[index]}</div>
              <div className="bar-value">{value}%</div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderCategoryBreakdown = () => {
    if (!data) return null;

    const total = Object.values(data.categoryBreakdown).reduce((sum, val) => sum + val, 0);

    return (
      <div className="category-breakdown">
        <h3>Category Distribution</h3>
        <div className="category-list">
          {Object.entries(data.categoryBreakdown).map(([category, value]) => {
            const percentage = Math.round((value / total) * 100);
            return (
              <div key={category} className="category-item">
                <div className="category-info">
                  <div 
                    className="category-color"
                    style={{ backgroundColor: getCategoryColor(category as keyof AnalyticsData['categoryBreakdown']) }}
                  ></div>
                  <span className="category-name">{category}</span>
                </div>
                <div className="category-stats">
                  <span className="category-count">{value}</span>
                  <span className="category-percentage">{percentage}%</span>
                </div>
                <div className="category-bar">
                  <div 
                    className="category-bar-fill"
                    style={{ 
                      width: `${percentage}%`,
                      backgroundColor: getCategoryColor(category as keyof AnalyticsData['categoryBreakdown'])
                    }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="loading-spinner"></div>
        <p>Loading analytics...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="analytics-error">
        <div className="error-icon">📊</div>
        <h3>Unable to load analytics</h3>
        <p>Please try again later</p>
        <button onClick={loadAnalytics} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>Analytics</h1>
        <div className="timeframe-selector">
          {(['week', 'month', 'year'] as const).map(period => (
            <button
              key={period}
              className={timeframe === period ? 'active' : ''}
              onClick={() => setTimeframe(period)}
            >
              {period.charAt(0).toUpperCase() + period.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {!isOnline && (
        <div className="offline-notice">
          <span className="offline-icon">📡</span>
          Showing cached data. Connect to internet for latest analytics.
        </div>
      )}

      <div className="analytics-grid">
        {/* Key Metrics */}
        <div className="metrics-section">
          <div className="metric-card primary">
            <div className="metric-icon">🎯</div>
            <div className="metric-content">
              <div className="metric-value">{data.progressScore}%</div>
              <div className="metric-label">Progress Score</div>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">✅</div>
            <div className="metric-content">
              <div className="metric-value">{data.completionRate}%</div>
              <div className="metric-label">Completion Rate</div>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">🔥</div>
            <div className="metric-content">
              <div className="metric-value">{data.streakDays}</div>
              <div className="metric-label">Day Streak</div>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">📋</div>
            <div className="metric-content">
              <div className="metric-value">{data.totalTasks}</div>
              <div className="metric-label">Total Tasks</div>
            </div>
          </div>
        </div>

        {/* Progress Chart */}
        <div className="chart-section">
          {renderProgressChart()}
        </div>

        {/* Category Breakdown */}
        <div className="breakdown-section">
          {renderCategoryBreakdown()}
        </div>

        {/* AI Insights */}
        <div className="insights-section">
          <h3>AI Insights</h3>
          <div className="insights-list">
            {data.insights.map((insight, index) => (
              <div key={index} className="insight-item">
                <div className="insight-icon">💡</div>
                <p className="insight-text">{insight}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="analytics-actions">
        <button className="export-btn" onClick={() => window.print()}>
          📄 Export Report
        </button>
        <button className="refresh-btn" onClick={loadAnalytics}>
          🔄 Refresh Data
        </button>
      </div>
    </div>
  );
};

export default Analytics;