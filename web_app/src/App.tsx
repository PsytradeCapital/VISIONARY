/**
 * Visionary PWA - Main Application Component
 */

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import './App.css';

import { store } from './store/store';
import { registerSW } from './utils/serviceWorker';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Schedule from './pages/Schedule/Schedule';
import Upload from './pages/Upload/Upload';
import Analytics from './pages/Analytics/Analytics';
import Login from './pages/Auth/Login';
import { AuthProvider } from './contexts/AuthContext';

function App() {
  useEffect(() => {
    // Register service worker for PWA functionality
    registerSW();
  }, []);

  return (
    <Provider store={store}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<Layout />}>
                <Route index element={<Dashboard />} />
                <Route path="schedule" element={<Schedule />} />
                <Route path="upload" element={<Upload />} />
                <Route path="analytics" element={<Analytics />} />
              </Route>
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </Provider>
  );
}

export default App;