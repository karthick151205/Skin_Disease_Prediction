import React, { useRef, useState } from 'react';
import { UploadCloud, Image as ImageIcon, RefreshCw, Sparkles, CheckCircle2 } from 'lucide-react';
import ScanAnimation from './ScanAnimation';

// Built-in high quality sample lesion data (encoded data URLs / placeholder sample triggers)
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const SAMPLES = [
  { id: 'bkl', label: 'Benign Keratosis', color: '#10b981', img: `${API_BASE_URL}/api/sample-image/bkl` },
  { id: 'nv', label: 'Common Mole', color: '#10b981', img: `${API_BASE_URL}/api/sample-image/nv` },
  { id: 'akiec', label: 'Sun Damage', color: '#f59e0b', img: `${API_BASE_URL}/api/sample-image/akiec` },
  { id: 'mel', label: 'Melanoma (Urgent)', color: '#ef4444', img: `${API_BASE_URL}/api/sample-image/mel` },
];

export default function ImageUploader({ 
  selectedImage, 
  previewUrl, 
  onImageSelect, 
  onReset, 
  isLoading,
  onSampleSelect 
}) {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        onImageSelect(file);
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onImageSelect(e.target.files[0]);
    }
  };

  return (
    <div className="glass-card" style={{ padding: '1.75rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-heading)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ImageIcon size={20} color="#a855f7" /> Upload Lesion Image
        </h3>
        {previewUrl && (
          <button 
            onClick={onReset} 
            disabled={isLoading}
            style={{
              background: 'rgba(255, 255, 255, 0.06)',
              border: '1px solid var(--border-glass)',
              color: 'var(--text-secondary)',
              padding: '0.4rem 0.8rem',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              transition: 'all 0.2s ease'
            }}
          >
            <RefreshCw size={14} /> New Scan
          </button>
        )}
      </div>

      {!previewUrl ? (
        <div 
          className={`dropzone ${isDragOver ? 'active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept="image/*" 
            style={{ display: 'none' }} 
          />
          <div className="upload-icon-wrapper">
            <UploadCloud size={34} />
          </div>
          <div className="upload-title">Drag & Drop skin lesion image here</div>
          <div className="upload-sub">Supports JPG, JPEG, PNG format • Max 10MB</div>
          <button type="button" className="browse-btn">
            Browse File
          </button>
        </div>
      ) : (
        <div>
          <div className="image-preview-container">
            <img src={previewUrl} alt="Skin Lesion Upload" className="preview-img" />
            {isLoading && <ScanAnimation />}
          </div>
          <div style={{ marginTop: '0.75rem', display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <span>{selectedImage ? selectedImage.name : 'Image Sample'}</span>
            <span>{selectedImage ? `${(selectedImage.size / 1024).toFixed(1)} KB` : 'Ready for AI Scan'}</span>
          </div>
        </div>
      )}

      {/* Quick Test Samples */}
      {!previewUrl && (
        <div className="sample-images-group">
          <div className="sample-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Sparkles size={14} color="#a855f7" /> Real Dataset Test Samples
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem' }}>
            {SAMPLES.map((sample) => (
              <button
                key={sample.id}
                type="button"
                onClick={() => onSampleSelect(sample.id)}
                style={{
                  padding: '0.6rem',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: `1px solid ${sample.color}40`,
                  color: 'var(--text-heading)',
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem'
                }}
              >
                <img 
                  src={sample.img} 
                  alt={sample.label} 
                  style={{ width: '42px', height: '42px', borderRadius: '8px', objectFit: 'cover' }} 
                />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: '600', fontSize: '0.85rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{sample.label}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Click to Run Scan</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
