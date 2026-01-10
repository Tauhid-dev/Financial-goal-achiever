import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { getInsights } from '../lib/endpoints';
import { Scope, InsightsResponse } from '../lib/types';

export const InsightsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [insights, setInsights] = useState<InsightsResponse | null>(null);
  const [month, setMonth] = useState<string>('');

  const fetchInsights = async (scope: Scope, monthParam?: string) => {
    try {
      const data = await getInsights(scope, monthParam);
      setInsights(data);
    } catch (e: any) {
      setError(e.message ?? 'Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const scope = await ensureSession();
        await fetchInsights(scope, month || undefined);
      } catch (e: any) {
        setError(e.message ?? 'Failed to initialise session');
        setLoading(false);
      }
    };
    init();
  }, [month]);

  if (loading) return <div>Loading insights...</div>;
  if (error) return (
    <div style={{ color: 'red' }}>
      {error}
      <button onClick={() => window.location.reload()} style={{ marginLeft: '1rem' }}>Reload</button>
    </div>
  );

  if (!insights) return <div>No insights available.</div>;

  const { summary, top_expense_categories, recommendations, notes } = insights;

  return (
    <div>
      <h2>Insights {month && `for ${month}`}</h2>

      {/* Month selector */}
      <div style={{ marginBottom: '1rem' }}>
        <label>Month (YYYY-MM): </label>
        <input
          type="month"
          value={month}
          onChange={e => setMonth(e.target.value)}
          placeholder="2023-07"
        />
      </div>

      {/* Summary card */}
      {summary && (
        <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
          <h3>Summary</h3>
          <p>Income: {summary.income ?? '—'}</p>
          <p>Expenses: {summary.expenses ?? '—'}</p>
          <p>Savings: {summary.savings ?? '—'}</p>
          <p>Savings Rate: {summary.savings_rate ?? '—'}</p>
        </div>
      )}

      {/* Top expense categories */}
      {top_expense_categories && top_expense_categories.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h3>Top Expense Categories</h3>
          <ul>
            {top_expense_categories.map((c, i) => (
              <li key={i}>
                {c.category}: {c.amount}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h3>Recommendations</h3>
          <ul>
            {recommendations.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Notes */}
      {notes && notes.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h3>Notes</h3>
          <ul>
            {notes.map((n, i) => (
              <li key={i}>{n}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
