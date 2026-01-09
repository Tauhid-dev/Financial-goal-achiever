import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ensureSession } from '../lib/session';
import { listSummaries } from '../lib/endpoints';
import Spinner from '../components/Spinner';
import ErrorBanner from '../components/ErrorBanner';
import { getErrorMessage, isUnauthorized } from '../lib/errors';
import { clearToken } from '../lib/api';

export const SummaryPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [summaries, setSummaries] = useState<any[]>([]);

  const handleError = (err: unknown) => {
    if (isUnauthorized(err)) {
      clearToken();
      navigate('/login');
    } else {
      setError(getErrorMessage(err));
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const scope = await ensureSession();
        const data = await listSummaries(scope);
        setSummaries(data);
      } catch (err) {
        handleError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <Spinner label="Loading summary…" />;
  if (error) return <ErrorBanner error={error} onRetry={() => {
    const retry = async () => {
      try {
        const scope = await ensureSession();
        const data = await listSummaries(scope);
        setSummaries(data);
        setError(null);
      } catch (err) {
        handleError(err);
      }
    };
    retry();
  }} />;

  return (
    <div>
      <h2>Summary</h2>
      <ul>
        {summaries.map((s) => (
          <li key={s.id}>
            {s.month}: Income {s.income}, Expenses {s.expenses}, Savings {s.savings}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SummaryPage;
