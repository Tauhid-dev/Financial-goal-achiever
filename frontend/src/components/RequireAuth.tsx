import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { getToken } from '../lib/auth';

const RequireAuth: React.FC = () => {
  const token = getToken();
  const location = useLocation();
  return token ? <Outlet /> : <Navigate to={`/login?next=${encodeURIComponent(location.pathname + location.search)}`} replace />;
};

export default RequireAuth;
