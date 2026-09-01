import React, { useState } from 'react';
import { 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  Activity, 
  ExternalLink, 
  MapPin, 
  FileText, 
  HeartHandshake,
  BarChart3
} from 'lucide-react';

export default function ResultsDashboard({ result }) {
  const [activeTab, setActiveTab] = useState('care');

  if (!result) return null;

  const { primary, breakdown, disclaimer } = result;

  const getBadgeIcon = (color) => {
    if (color === 'red') return <ShieldAlert size={16} />;
    if (color === 'amber') return <AlertTriangle size={16} />;
    return <CheckCircle2 size={16} />;
  };

  return (
    <div className="glass-card" style={{ padding: '1.75rem' }}>
      {/* Primary Diagnosis Hero Header */}
      <div className="diagnosis-hero-card">
        <div className="diagnosis-header">
          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#a855f7', marginBottom: '0.2rem' }}>
              Primary AI Prediction
            </div>
            <div className="diagnosis-title">{primary.name}</div>
            <div className="diagnosis-category">{primary.category} ({primary.code.toUpperCase()})</div>
          </div>
          <div className={`risk-badge ${primary.badge_color}`}>
            {getBadgeIcon(primary.badge_color)}
            {primary.risk_label}
          </div>
        </div>

        <div className="confidence-display">
          <span className="confidence-num">{primary.confidence_percent}%</span>
          <span className="confidence-label">AI Confidence Score</span>
        </div>
      </div>

      {/* Probability Breakdown Progress List */}
      <div className="breakdown-section" style={{ marginBottom: '2rem' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-heading)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <BarChart3 size={18} color="#06b6d4" /> 7-Class Probability Distribution
        </h4>

        {breakdown.map((item, index) => (
          <div key={item.class_id} className="breakdown-row">
            <div className="breakdown-meta">
              <span className="breakdown-name">
                {index === 0 && <span style={{ color: '#06b6d4', marginRight: '0.4rem' }}>★</span>}
                {item.name} <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>({item.code})</span>
              </span>
              <span className="breakdown-percent">{item.confidence_percent}%</span>
            </div>
            <div className="progress-track">
              <div 
                className={`progress-fill ${index === 0 ? 'top-match' : ''}`}
                style={{ 
                  width: `${Math.max(item.confidence_percent, 2)}%`,
                  background: index === 0 
                    ? 'linear-gradient(90deg, #9333ea, #06b6d4)' 
                    : item.badge_color === 'red' 
                    ? 'linear-gradient(90deg, #ef4444, #f87171)' 
                    : 'linear-gradient(90deg, #6b21a8, #a855f7)'
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="tab-group">
        <button 
          className={`tab-btn ${activeTab === 'care' ? 'active' : ''}`}
          onClick={() => setActiveTab('care')}
        >
          <HeartHandshake size={16} /> Suggestions & Care
        </button>
        <button 
          className={`tab-btn ${activeTab === 'resources' ? 'active' : ''}`}
          onClick={() => setActiveTab('resources')}
        >
          <FileText size={16} /> Medical Resources
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'care' && (
        <div>
          <div className="care-card">
            <div className="care-title">
              <Activity size={18} color="#a855f7" /> Clinical Action Plan
            </div>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
              {primary.action}
            </p>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>Recommended Care:</strong> {primary.care}
            </div>
          </div>

          <div className="action-links-group">
            <a 
              href="https://www.google.com/maps/search/dermatologists+near+me/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="action-link-btn primary"
            >
              <MapPin size={18} /> Find a Dermatologist Near Me
            </a>
          </div>
        </div>
      )}

      {activeTab === 'resources' && (
        <div>
          <div className="care-card" style={{ background: 'rgba(6, 182, 212, 0.06)', borderColor: 'rgba(6, 182, 212, 0.2)' }}>
            <div className="care-title" style={{ color: '#0284c7' }}>
              <FileText size={18} color="#06b6d4" /> Lesion Profile & Medical Guide
            </div>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
              {primary.description}
            </p>
          </div>

          <div className="action-links-group">
            <a 
              href={primary.resource_url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="action-link-btn secondary"
            >
              <ExternalLink size={18} /> Read Dermatology Article on {primary.name}
            </a>
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <div style={{ marginTop: '1.5rem', padding: '0.75rem', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', fontSize: '0.75rem', color: '#64748b' }}>
        <strong>Medical Disclaimer:</strong> {disclaimer}
      </div>
    </div>
  );
}
