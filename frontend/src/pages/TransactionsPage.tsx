import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listTransactions } from '../lib/endpoints';
import Spinner from '../components/Spinner';
import ErrorBanner from '../components/ErrorBanner';
import { Transaction, Scope } from '../lib/types';

export const TransactionsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [offset, setOffset] = useState(0);
  const limit = 20;
  const [monthFilter, setMonthFilter] = useState<string>('');
  const [currentScope, setCurrentScope] = useState<Scope | null>(null);

const fetchTxns = async (scope?: Scope) => {
  const effectiveScope = scope ?? (await ensureSession());
  setCurrentScope(effectiveScope);
  const params: any = { limit, offset };
  if (monthFilter) {
    params.month = monthFilter;
  }
  const data = await listTransactions(effectiveScope, params);
  setTransactions(data);
};

  const nextPage = () => setOffset(prev => prev + limit);
  const prevPage = () => setOffset(prev => Math.max(prev - limit, 0));

  useEffect(() => {
    const init = async () => {
      try {
        const scope = await ensureSession();
        await fetchTxns(scope);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [offset, monthFilter]);

  if (loading) return <Spinner label="Loading transactions…" />;
  if (error) return <ErrorBanner error={error} onRetry={() => fetchTxns()} />;

  return (
    <div>
      <h2>Transactions</h2>
      <div>
        <label>Month (YYYY-MM): </label>
        <input
          type="text"
          value={monthFilter}
          onChange={e => setMonthFilter(e.target.value)}
          placeholder="2023-07"
        />
      </div>
      <ul>
        {transactions.map((tx) => (
          <li key={tx.id}>
            {tx.date}: {tx.description} – {tx.amount}
          </li>
        ))}
      </ul>
      <div>
        <button onClick={prevPage} disabled={offset === 0}>Prev</button>
        <button onClick={nextPage}>Next</button>
      </div>
    </div>
  );
};

export default TransactionsPage;
