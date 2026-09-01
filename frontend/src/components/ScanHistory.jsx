import React from 'react';
import { History, X, Trash2, Calendar, ChevronRight } from 'lucide-react';

export default function ScanHistory({ isOpen, onClose, history, onSelectHistory, onClearHistory }) {
  if (!isOpen) return null;

  return (
    <div className="history-drawer">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-glass)' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-heading)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <History size={20} color="#a855f7" /> Scan History
        </h3>
        <button 
          onClick={onClose} 
          style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: '0.2rem' }}
        >
          <X size={20} />
        </button>
      </div>

      {history.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
          <History size={40} style={{ margin: '0 auto 1rem', opacity: 0.4 }} />
          <p>No saved scans yet.</p>
          <span style={{ fontSize: '0.8rem' }}>Uploaded scans will automatically appear here.</span>
        </div>
      ) : (
        <>
          <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
            <button 
              onClick={onClearHistory} 
              style={{
                background: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                color: '#ef4444',
                padding: '0.3rem 0.7rem',
                borderRadius: '6px',
                fontSize: '0.8rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.3rem'
              }}
            >
              <Trash2 size={13} /> Clear History
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {history.map((item) => (
              <div 
                key={item.id} 
                className="history-item"
                onClick={() => {
                  onSelectHistory(item);
                  onClose();
                }}
              >
                <img src={item.previewUrl} alt={item.result.primary.name} className="history-thumb" />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: '700', fontSize: '0.9rem', color: 'var(--text-heading)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {item.result.primary.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#a855f7', fontWeight: '600' }}>
                    {item.result.primary.confidence_percent}% Confidence
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.3rem', marginTop: '0.2rem' }}>
                    <Calendar size={11} /> {item.date}
                  </div>
                </div>
                <ChevronRight size={16} color="var(--text-secondary)" />
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
