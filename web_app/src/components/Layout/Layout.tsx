/**
 * Layout Component for PWA
 * Task 11.2: Mobile-web synchronization with cloud backend
 */

import React, { useEffect, useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { setOnlineStatus, performBackgroundSync, loadPersistedState } from '../../store/slices/syncSlice';
import './Layout.css';

const Layout: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { isOnline, pendingActions, syncing, lastSyncTime } = useSelector((state: RootState) => state.sync);
  const [showSyncStatus, setShowSyncStatus] = useState(false);

  useEffect(() => {
    // Load persisted state on app start
    // @ts-ignore
    dispatch(loadPersistedState());

    // Set up online/offline listeners
    const handleOnline = () => {
      // @ts-ignore
      dispatch(setOnlineStatus(true));
      // @ts-ignore
      dispatch(performBackgroundSync());
    };

    const handleOffline = () => {
      // @ts-ignore
      dispatch(setOnlineStatus(false));
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Set up periodic sync when online
    const syncInterval = setInterval(() => {
      if (navigator.onLine && pendingActions.length > 0) {
        // @ts-ignore
        dispatch(performBackgroundSync());
      }
    }, 30000); // 30 seconds

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(syncInterval);
    };
  }, [dispatch, pendingActions.length]);

  useEffect(() => {
    // Show sync status when there are pending actions
    if (pendingActions.length > 0 || syncing) {
      setShowSyncStatus(true);
      const timer = setTimeout(() => setShowSyncStatus(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [pendingActions.length, syncing]);

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const handleManualSync = () => {
    if (isOnline) {
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

  const navigationItems = [
    { path: '/', label: 'Dashboard', icon: 'dashboard-icon' },
    { path: '/schedule', label: 'Schedule', icon: 'schedule-icon' },
    { path: '/upload', label: 'Upload', icon: 'upload-icon' },
    { path: '/analytics', label: 'Analytics', icon: 'analytics-icon' },
  ];

  return (
    <div className="layout">
      {/* Header */}
      <header className="layout-header">
        <div className="header-content">
          <div className="app-brand">
            <div className="brand-icon">
              <div className="ai-brain-icon"></div>
            </div>
            <h1>Visionary</h1>
          </div>

          <div className="header-actions">
            {/* Connection Status */}
            <div className={`connection-status ${isOnline ? 'online' : 'offline'}`}>
              <span className="status-indicator"></span>
              <span className="status-text">{isOnline ? 'Online' : 'Offline'}</span>
            </div>

            {/* Sync Button */}
            <button 
              className={`sync-btn ${syncing ? 'syncing' : ''}`}
              onClick={handleManualSync}
              disabled={!isOnline || syncing}
              title={`Last sync: ${formatLastSync(lastSyncTime)}`}
            >
              <div className="sync-icon"></div>
              {syncing ? 'Syncing...' : 'Sync'}
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="layout-nav">
        <div className="nav-content">
          {navigationItems.map(item => (
            <button
              key={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => handleNavigation(item.path)}
            >
              <div className={`nav-icon ${item.icon}`}></div>
              <span className="nav-label">{item.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Sync Status Banner */}
      {showSyncStatus && (pendingActions.length > 0 || syncing) && (
        <div className="sync-status-banner">
          <div className="sync-status-content">
            {syncing ? (
              <>
                <div className="loading-spinner small"></div>
                <span>Syncing {pendingActions.length} item(s)...</span>
              </>
            ) : (
              <>
                <div className="connection-online-icon"></div>
                <span>{pendingActions.length} item(s) pending sync</span>
                {isOnline && (
                  <button className="sync-now-btn" onClick={handleManualSync}>
                    Sync Now
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="layout-main">
        <Outlet />
      </main>

      {/* Offline Banner */}
      {!isOnline && (
        <div className="offline-banner">
          <div className="offline-content">
            <div className="connection-offline-icon"></div>
            <div className="offline-text">
              <strong>You're offline</strong>
              <p>Changes will sync when you're back online</p>
            </div>
          </div>
        </div>
      )}

      {/* PWA Install Prompt */}
      <PWAInstallPrompt />
    </div>
  );
};

// PWA Install Prompt Component
const PWAInstallPrompt: React.FC = () => {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
      console.log('PWA installed');
    }
    
    setDeferredPrompt(null);
    setShowPrompt(false);
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    setDeferredPrompt(null);
  };

  if (!showPrompt) return null;

  return (
    <div className="install-prompt">
      <div className="install-prompt-content">
        <h4>Install Visionary</h4>
        <p>Add to your home screen for quick access</p>
      </div>
      <div className="install-prompt-actions">
        <button className="install-btn" onClick={handleInstall}>
          Install
        </button>
        <button className="dismiss-btn" onClick={handleDismiss}>
          Later
        </button>
      </div>
    </div>
  );
};

export default Layout;