/**
 * Login Page for PWA
 * Task 11.1: PWA with service workers for offline functionality
 */

import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';
import './Login.css';

const Login: React.FC = () => {
  const { isOnline } = useSelector((state: RootState) => state.sync);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    if (!isOnline) {
      setError('Please connect to the internet to sign in');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_data', JSON.stringify(data.user));
        
        // Redirect to dashboard
        window.location.href = '/';
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Login failed');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="app-logo">
            <div className="logo-icon">🎯</div>
            <h1>Visionary</h1>
          </div>
          <p className="login-subtitle">
            Your AI-powered personal scheduler
          </p>
        </div>

        {!isOnline && (
          <div className="offline-warning">
            <span className="warning-icon">⚠️</span>
            You're offline. Please connect to the internet to sign in.
          </div>
        )}

        <form className="login-form" onSubmit={handleLogin}>
          {error && (
            <div className="error-message">
              <span className="error-icon">❌</span>
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              disabled={loading || !isOnline}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={loading || !isOnline}
              required
            />
          </div>

          <button 
            type="submit" 
            className="login-btn"
            disabled={loading || !isOnline}
          >
            {loading ? (
              <>
                <div className="loading-spinner small"></div>
                Signing In...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="login-footer">
          <p>Don't have an account? <a href="/register">Sign up</a></p>
          <p><a href="/forgot-password">Forgot your password?</a></p>
        </div>

        <div className="pwa-features">
          <h3>Works Offline</h3>
          <div className="features-list">
            <div className="feature-item">
              <span className="feature-icon">📱</span>
              <span>Install as mobile app</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🔄</span>
              <span>Automatic sync when online</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">💾</span>
              <span>Offline data storage</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;