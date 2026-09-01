import React from 'react';

export default function ScanAnimation() {
  return (
    <>
      <div className="laser-scanner" />
      <div className="scanning-grid-overlay" />
      <div 
        style={{
          position: 'absolute',
          bottom: '15px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(9, 8, 20, 0.85)',
          border: '1px solid rgba(168, 85, 247, 0.5)',
          padding: '0.4rem 1rem',
          borderRadius: '100px',
          fontSize: '0.85rem',
          fontWeight: '600',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          backdropFilter: 'blur(8px)',
          zIndex: 20
        }}
      >
        <span className="pulse-dot" style={{ background: '#a855f7', boxShadow: '0 0 10px #a855f7' }} />
        Vision Transformer AI Analyzing Lesion...
      </div>
    </>
  );
}
