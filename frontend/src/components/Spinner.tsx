import React from 'react';

type SpinnerProps = {
  label?: string;
  size?: 'sm' | 'md';
};

const Spinner: React.FC<SpinnerProps> = ({ label, size = 'md' }) => {
  const sizePx = size === 'sm' ? 16 : 32;
  const style: React.CSSProperties = {
    width: sizePx,
    height: sizePx,
    border: `${sizePx / 8}px solid #ccc`,
    borderTop: `${sizePx / 8}px solid #333`,
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    margin: '0 auto',
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={style} />
      {label && <div style={{ marginTop: '0.5rem' }}>{label}</div>}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Spinner;
