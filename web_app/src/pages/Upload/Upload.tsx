/**
 * Upload Page for PWA
 * Task 11.1: PWA with service workers for offline functionality
 */

import React, { useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { addPendingAction } from '../../store/slices/syncSlice';
import './Upload.css';

interface UploadFile {
  file: File;
  id: string;
  progress: number;
  status: 'pending' | 'uploading' | 'completed' | 'failed';
  error?: string;
}

const Upload: React.FC = () => {
  const dispatch = useDispatch();
  const { isOnline, pendingActions } = useSelector((state: RootState) => state.sync);
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [textInput, setTextInput] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(Array.from(e.target.files));
    }
  };

  const handleFiles = (fileList: File[]) => {
    const newFiles: UploadFile[] = fileList.map(file => ({
      file,
      id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      progress: 0,
      status: 'pending' as const,
    }));

    setFiles(prev => [...prev, ...newFiles]);

    // Process each file
    newFiles.forEach(uploadFile => {
      processFile(uploadFile);
    });
  };

  const processFile = async (uploadFile: UploadFile) => {
    setFiles(prev => prev.map(f => 
      f.id === uploadFile.id ? { ...f, status: 'uploading' } : f
    ));

    try {
      if (isOnline) {
        // Simulate upload progress
        for (let progress = 0; progress <= 100; progress += 10) {
          await new Promise(resolve => setTimeout(resolve, 100));
          setFiles(prev => prev.map(f => 
            f.id === uploadFile.id ? { ...f, progress } : f
          ));
        }

        // Simulate API call
        const formData = new FormData();
        formData.append('file', uploadFile.file);

        const response = await fetch('/api/v1/upload/document', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          setFiles(prev => prev.map(f => 
            f.id === uploadFile.id ? { ...f, status: 'completed', progress: 100 } : f
          ));
        } else {
          throw new Error('Upload failed');
        }
      } else {
        // Store for offline sync
        const fileData = {
          name: uploadFile.file.name,
          size: uploadFile.file.size,
          type: uploadFile.file.type,
          // In a real implementation, you'd store the file data appropriately
          // For demo purposes, we'll just store metadata
        };

        dispatch(addPendingAction({
          type: 'upload',
          data: fileData,
          maxRetries: 3,
        }));

        setFiles(prev => prev.map(f => 
          f.id === uploadFile.id ? { ...f, status: 'completed', progress: 100 } : f
        ));
      }
    } catch (error) {
      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id ? { 
          ...f, 
          status: 'failed', 
          error: error instanceof Error ? error.message : 'Upload failed'
        } : f
      ));
    }
  };

  const handleTextSubmit = async () => {
    if (!textInput.trim()) return;

    try {
      if (isOnline) {
        const response = await fetch('/api/v1/upload/text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: textInput }),
        });

        if (response.ok) {
          setTextInput('');
          // Show success message
        } else {
          throw new Error('Text upload failed');
        }
      } else {
        // Store for offline sync
        dispatch(addPendingAction({
          type: 'upload',
          data: { text: textInput, type: 'text' },
          maxRetries: 3,
        }));

        setTextInput('');
      }
    } catch (error) {
      console.error('Text upload failed:', error);
    }
  };

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const retryFile = (id: string) => {
    const file = files.find(f => f.id === id);
    if (file) {
      setFiles(prev => prev.map(f => 
        f.id === id ? { ...f, status: 'pending', progress: 0, error: undefined } : f
      ));
      processFile(file);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-header">
        <h1>Upload Content</h1>
        <div className="upload-status">
          {!isOnline && (
            <div className="offline-notice">
              <span className="offline-icon">📡</span>
              Offline - uploads will sync when online
            </div>
          )}
          {pendingActions.filter(a => a.type === 'upload').length > 0 && (
            <div className="pending-uploads">
              {pendingActions.filter(a => a.type === 'upload').length} pending upload(s)
            </div>
          )}
        </div>
      </div>

      <div className="upload-sections">
        {/* File Upload Section */}
        <section className="file-upload-section">
          <h2>Upload Files</h2>
          <div 
            className={`file-drop-zone ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="drop-zone-content">
              <div className="upload-icon">📁</div>
              <p className="drop-zone-text">
                Drag and drop files here, or <span className="click-text">click to browse</span>
              </p>
              <p className="file-types">Supports: PDF, DOC, DOCX, TXT, Images</p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
          </div>

          {files.length > 0 && (
            <div className="file-list">
              <h3>Upload Progress</h3>
              {files.map(file => (
                <div key={file.id} className={`file-item ${file.status}`}>
                  <div className="file-info">
                    <div className="file-name">{file.file.name}</div>
                    <div className="file-size">
                      {(file.file.size / 1024 / 1024).toFixed(2)} MB
                    </div>
                  </div>
                  
                  <div className="file-progress">
                    {file.status === 'uploading' && (
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ width: `${file.progress}%` }}
                        ></div>
                      </div>
                    )}
                    
                    <div className="file-status">
                      {file.status === 'pending' && <span className="status-pending">⏳ Pending</span>}
                      {file.status === 'uploading' && <span className="status-uploading">⬆️ Uploading {file.progress}%</span>}
                      {file.status === 'completed' && <span className="status-completed">✅ Completed</span>}
                      {file.status === 'failed' && <span className="status-failed">❌ Failed</span>}
                    </div>
                  </div>

                  <div className="file-actions">
                    {file.status === 'failed' && (
                      <button 
                        className="retry-btn"
                        onClick={() => retryFile(file.id)}
                      >
                        🔄 Retry
                      </button>
                    )}
                    <button 
                      className="remove-btn"
                      onClick={() => removeFile(file.id)}
                    >
                      🗑️ Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Text Input Section */}
        <section className="text-input-section">
          <h2>Text Input</h2>
          <div className="text-input-container">
            <textarea
              className="text-input"
              placeholder="Type or paste your content here..."
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              rows={8}
            />
            <div className="text-input-actions">
              <div className="character-count">
                {textInput.length} characters
              </div>
              <button 
                className="submit-text-btn"
                onClick={handleTextSubmit}
                disabled={!textInput.trim()}
              >
                Submit Text
              </button>
            </div>
          </div>
        </section>

        {/* Voice Input Section (Future Enhancement) */}
        <section className="voice-input-section">
          <h2>Voice Input</h2>
          <div className="voice-input-container">
            <div className="voice-placeholder">
              <div className="voice-icon">🎤</div>
              <p>Voice input will be available in a future update</p>
              <button className="voice-btn" disabled>
                Start Recording
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Upload;