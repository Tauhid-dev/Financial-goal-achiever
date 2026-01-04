import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listSummaries } from '../lib/endpoints';

export const SummaryPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [summaries, setSummaries] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { scopeId, familyId } = await ensureSession();
        const fid = familyId ?? scopeId;
        if (!fid) {
          setError("No family scope yet");
          return;
        }
        const data = await listSummaries(fid);
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
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

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
