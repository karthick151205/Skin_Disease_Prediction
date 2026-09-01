import React, { useState, useEffect } from 'react';
import { Sparkles, History, Activity, AlertCircle, Sun, Moon } from 'lucide-react';
import confetti from 'canvas-confetti';

import ImageUploader from './components/ImageUploader';
import ResultsDashboard from './components/ResultsDashboard';
import ScanHistory from './components/ScanHistory';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem('skincare_ai_theme') || 'dark');

  // Handle theme changes
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('skincare_ai_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  // Load scan history from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('skincare_ai_history');
      if (saved) {
        setHistory(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Failed to parse history:', e);
    }
  }, []);

  const saveToHistory = (scanResult, imagePreview) => {
    const newItem = {
      id: Date.now().toString(),
      date: new Date().toLocaleDateString() + ' ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      result: scanResult,
      previewUrl: imagePreview
    };
    const updated = [newItem, ...history.slice(0, 9)];
    setHistory(updated);
    try {
      localStorage.setItem('skincare_ai_history', JSON.stringify(updated));
    } catch (e) {
      console.error('Failed to save history:', e);
    }
  };

  const handleImageSelect = async (file) => {
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setResult(null);
    setError(null);

    await runPrediction(file, url);
  };

  const runPrediction = async (file, imagePreviewUrl) => {
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Prediction failed');
      }

      const data = await response.json();
      setResult(data);
      saveToHistory(data, imagePreviewUrl);

      // Trigger celebrate confetti if benign
      if (data.primary.badge_color === 'green') {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 }
        });
      }
    } catch (err) {
      console.error('API Error:', err);
      setError(err.message || 'Could not connect to FastAPI server. Please check backend status.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSampleSelect = async (sampleId) => {
    try {
      setIsLoading(true);
      const res = await fetch(`${API_BASE_URL}/api/sample-image/${sampleId}`);
      if (!res.ok) throw new Error("Could not fetch sample image");
      const blob = await res.blob();
      const file = new File([blob], `sample_${sampleId}.jpg`, { type: 'image/jpeg' });
      handleImageSelect(file);
    } catch (err) {
      console.error("Failed to load sample image:", err);
      setError("Could not load sample image from server.");
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('skincare_ai_history');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* App Header */}
      <header className="app-header">
        <div className="logo-group">
          <div className="logo-icon">🔮</div>
          <div>
            <div className="logo-text">SkinCare AI</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: '500' }}>
              Vision Transformer Diagnostic Assistant
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div className="model-pill">
            <span className="pulse-dot" /> ViT-16 (ImageNet21k) Active
          </div>

          {/* Theme Toggle Button */}
          <button 
            className="theme-toggle-btn"
            onClick={toggleTheme}
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            aria-label="Toggle Theme"
          >
            {theme === 'dark' ? <Sun size={18} color="#fcd34d" /> : <Moon size={18} color="#9333ea" />}
          </button>

          <button 
            onClick={() => setIsHistoryOpen(true)}
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-glass)',
              color: 'var(--text-primary)',
              padding: '0.5rem 1rem',
              borderRadius: '10px',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              transition: 'all 0.2s ease'
            }}
          >
            <History size={16} color="#a855f7" /> History ({history.length})
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="main-container" style={{ flex: 1 }}>
        {error && (
          <div 
            style={{ 
              marginBottom: '1.5rem', 
              padding: '1rem 1.25rem', 
              borderRadius: '12px', 
              background: 'rgba(239, 68, 68, 0.12)', 
              border: '1px solid rgba(239, 68, 68, 0.3)', 
              color: '#fca5a5', 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.75rem',
              fontSize: '0.9rem'
            }}
          >
            <AlertCircle size={20} color="#ef4444" />
            <div style={{ flex: 1 }}>
              <strong>API Error:</strong> {error}
            </div>
          </div>
        )}

        <div className="grid-layout">
          {/* Left Column: Upload & Image Inspection */}
          <div>
            <ImageUploader 
              selectedImage={selectedFile}
              previewUrl={previewUrl}
              onImageSelect={handleImageSelect}
              onReset={handleReset}
              isLoading={isLoading}
              onSampleSelect={handleSampleSelect}
            />
          </div>

          {/* Right Column: AI Analysis & Diagnostic Results */}
          <div>
            {result ? (
              <ResultsDashboard result={result} />
            ) : (
              <div className="glass-card" style={{ padding: '3rem 2rem', textAlign: 'center', minHeight: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <div style={{ width: '70px', height: '70px', borderRadius: '50%', background: 'rgba(168, 85, 247, 0.1)', display: 'flex', alignItems: 'center', justifyCenter: 'center', marginBottom: '1.25rem', color: '#c084fc' }}>
                  <Activity size={36} />
                </div>
                <h3 style={{ fontSize: '1.3rem', fontWeight: '700', color: 'var(--text-heading)', marginBottom: '0.5rem' }}>
                  Awaiting Lesion Image
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '380px' }}>
                  Upload a skin lesion photograph on the left panel or click a quick demo test case to perform instant AI analysis.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* History Drawer */}
      <ScanHistory 
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectHistory={(item) => {
          setPreviewUrl(item.previewUrl);
          setResult(item.result);
        }}
        onClearHistory={clearHistory}
      />

      {/* Footer */}
      <footer className="footer-disclaimer">
        <strong>Disclaimer:</strong> SkinCare AI Assistant is an artificial intelligence decision-support prototype for educational purposes. It does not replace professional clinical evaluation or biopsy diagnosis by a board-certified dermatologist.
      </footer>
    </div>
  );
}
