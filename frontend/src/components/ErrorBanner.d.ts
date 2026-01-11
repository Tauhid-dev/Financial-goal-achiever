import React from 'react';

export interface ErrorBannerProps {
  error: unknown;
  onRetry?: () => void;
}

declare const ErrorBanner: React.FC<ErrorBannerProps>;

export default ErrorBanner;
