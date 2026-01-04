import React, { useEffect, useState } from 'react';
import { apiFetch, clearToken } from '../lib/api';
import { GoalCreate, GoalWithProjection } from '../lib/types';

export const Goals: React.FC = () => {
  const [familyId, setFamilyId] = useState<string>('');
  const [goals, setGoals] = useState<GoalWithProjection[]>([]);
  const [name, setName] = useState('');
  const [target, setTarget] = useState<number>(0);
  const [error, setError] = useState('');
  // No navigation library; we will reload on logout

  // fetch default family id
  useEffect(() => {
    const fetchFamily = async () => {
      try {
        const data = await apiFetch('/api/families/default');
        if (data && data.id) {
          setFamilyId(String(data.id));
        } else {
          const manual = prompt('Enter your family ID:');
          if (manual) setFamilyId(manual);
        }
      } catch {
        const manual = prompt('Enter your family ID:');
        if (manual) setFamilyId(manual);
      }
    };
    fetchFamily();
  }, []);

  // fetch goals when familyId is set
  useEffect(() => {
    if (!familyId) return;
    const fetchGoals = async () => {
      try {
        const data = await apiFetch(`/api/goals/${familyId}`);
        setGoals(data || []);
      } catch (err: any) {
        setError(err.message);
      }
    };
    fetchGoals();
  }, [familyId]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!familyId) return;
    const payload: GoalCreate = {
      name,
      target_amount: target,
      current_amount: 0,
      monthly_contribution: 0,
    };
    try {
      await apiFetch(`/api/goals/${familyId}`, {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      const refreshed = await apiFetch(`/api/goals/${familyId}`);
      setGoals(refreshed);
      setName('');
      setTarget(0);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDelete = async (goalId: string) => {
    if (!familyId) return;
    try {
      await apiFetch(`/api/goals/${familyId}/${goalId}`, {
        method: 'DELETE',
      });
      setGoals(goals.filter(g => g.id !== goalId));
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    clearToken();
    // Reload to show login screen
    window.location.reload();
  };

  return (
    <div>
      <h2>Goals</h2>
      <button onClick={handleLogout}>Logout</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleCreate}>
        <div>
          <label>Name:</label>
          <input value={name} onChange={e => setName(e.target.value)} required />
        </div>
        <div>
          <label>Target Amount:</label>
          <input type="number" value={target} onChange={e => setTarget(Number(e.target.value))} required />
        </div>
        <button type="submit">Create Goal</button>
      </form>
      <ul>
        {goals.map(g => (
          <li key={g.id}>
            {g.name} - {g.target_amount}{' '}
            <button onClick={() => handleDelete(g.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};
