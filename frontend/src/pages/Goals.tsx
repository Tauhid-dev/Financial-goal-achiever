import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listGoals, createGoal, deleteGoal } from '../lib/endpoints';
import { GoalWithProjection, GoalCreate } from '../lib/types';

export const Goals: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [goals, setGoals] = useState<GoalWithProjection[]>([]);
  const [newGoal, setNewGoal] = useState<GoalCreate>({
    name: '',
    target_amount: 0,
    current_amount: undefined,
    monthly_contribution: undefined,
    target_date: null,
  });

  const fetchGoals = async (familyId: string) => {
    const data = await listGoals(familyId);
    setGoals(data);
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { scopeId, familyId } = await ensureSession();
      const fid = familyId ?? scopeId;
      if (!fid) {
        setError("No family scope yet");
        return;
      }
      await createGoal(fid, newGoal);
      await fetchGoals(fid);
      setNewGoal({
        name: '',
        target_amount: 0,
        current_amount: undefined,
        monthly_contribution: undefined,
        target_date: null,
      });
    } catch (err: any) {
      setError(err.message);
    }
  };

  const deleteGoalHandler = async (goalId: string) => {
    try {
      const { scopeId, familyId } = await ensureSession();
      const fid = familyId ?? scopeId;
      if (!fid) {
        setError("No family scope yet");
        return;
      }
      await deleteGoal(fid, goalId);
      await fetchGoals(fid);
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const { scopeId, familyId } = await ensureSession();
        const fid = familyId ?? scopeId;
        await fetchGoals(fid);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Goals</h2>

      <form onSubmit={handleCreate} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Name"
          value={newGoal.name}
          onChange={e => setNewGoal({ ...newGoal, name: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Target Amount"
          value={newGoal.target_amount}
          onChange={e => setNewGoal({ ...newGoal, target_amount: Number(e.target.value) })}
          required
        />
        <input
          type="number"
          placeholder="Current Amount"
          value={newGoal.current_amount ?? ''}
          onChange={e =>
            setNewGoal({
              ...newGoal,
              current_amount: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
        <input
          type="number"
          placeholder="Monthly Contribution"
          value={newGoal.monthly_contribution ?? ''}
          onChange={e =>
            setNewGoal({
              ...newGoal,
              monthly_contribution: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
        <input
          type="date"
          placeholder="Target Date"
          value={newGoal.target_date ?? ''}
          onChange={e => setNewGoal({ ...newGoal, target_date: e.target.value || null })}
        />
        <button type="submit">Create Goal</button>
      </form>

      <ul>
        {goals.map(goal => (
          <li key={goal.id}>
            <strong>{goal.name}</strong> – Target: {goal.target_amount}
            {goal.projection && (
              <span>
                {' '}| Months Required: {goal.projection.months_required}
                {' '}| Achievable: {goal.projection.is_achievable ? 'Yes' : 'No'}
              </span>
            )}
            <button onClick={() => deleteGoalHandler(goal.id)} style={{ marginLeft: '1rem' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Goals;
