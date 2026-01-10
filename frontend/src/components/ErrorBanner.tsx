import React from 'react';
import { isUnauthorized } from '../lib/api';

type ErrorBannerProps = {
  error: unknown;
  onRetry?: () => void;
};

const ErrorBanner: React.FC<ErrorBannerProps> = ({ error, onRetry }) => {
  const errObj: any = error as any;
  const message = errObj?.message || 'An error occurred.';
  const authError = isUnauthorized(errObj);

  return (
    <div style={{ border: '1px solid #f44336', backgroundColor: '#ffebee', padding: '1rem', margin: '1rem 0' }}>
      <strong>{authError ? 'Session expired. Please log in again.' : message}</strong>
      {onRetry && (
        <button onClick={onRetry} style={{ marginLeft: '1rem' }}>
          Retry
        </button>
      )}
    </div>
  );
};

export default ErrorBanner;
