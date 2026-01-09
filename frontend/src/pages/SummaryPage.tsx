import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listSummaries } from '../lib/endpoints';
import Spinner from '../components/Spinner';
import ErrorBanner from '../components/ErrorBanner';

export const SummaryPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [summaries, setSummaries] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const scope = await ensureSession();
        const data = await listSummaries(scope);
        setSummaries(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <Spinner label="Loading summary…" />;
  if (error) return <ErrorBanner error={error} onRetry={() => {
    // retry fetching summary
    const retry = async () => {
      try {
        const scope = await ensureSession();
        const data = await listSummaries(scope);
        setSummaries(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
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
