import React from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { clearToken, getToken } from '../lib/auth';
import { ScopeSwitcher } from '../components/ScopeSwitcher';

const AppShell: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    clearToken();
    navigate('/login');
  };

  return (
    <div>
      <nav style={{ marginBottom: '1rem' }}>
        <Link to="summary" style={{ marginRight: '1rem' }}>Summary</Link>
        <Link to="documents" style={{ marginRight: '1rem' }}>Documents</Link>
        <Link to="transactions" style={{ marginRight: '1rem' }}>Transactions</Link>
        <Link to="goals" style={{ marginRight: '1rem' }}>Goals</Link>
        <Link to="insights" style={{ marginRight: '1rem' }}>Insights</Link>
        <button onClick={handleLogout} style={{ marginLeft: '2rem' }}>
          Logout
        </button>
        {getToken() && <ScopeSwitcher />}
      </nav>
      <Outlet />
    </div>
  );
};

export default AppShell;
