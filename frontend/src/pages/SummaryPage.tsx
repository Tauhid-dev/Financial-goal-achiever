import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listSummaries } from '../lib/endpoints';
import { Scope } from '../lib/types';

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

  if (loading) return <div>Loading...</div>;
  if (error) return (
  <div style={{ color: 'red' }}>
    {error}
    <button onClick={() => window.location.reload()} style={{ marginLeft: '1rem' }}>Reload</button>
  </div>
);

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
