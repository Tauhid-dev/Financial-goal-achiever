import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ensureSession } from '../lib/session';
import { listGoals, createGoal, deleteGoal } from '../lib/endpoints';
import { GoalWithProjection, GoalCreate } from '../lib/types';
import Spinner from '../components/Spinner';
import ErrorBanner from '../components/ErrorBanner';
import { Scope } from '../lib/types';
import { getErrorMessage, isUnauthorized } from '../lib/errors';
import { clearToken } from '../lib/api';

export const Goals: React.FC = () => {
  const navigate = useNavigate();

  const handleError = (err: unknown) => {
    if (isUnauthorized(err)) {
      clearToken();
      navigate('/login');
    } else {
      setError(getErrorMessage(err));
    }
  };

  // UI state
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
  const [validationErrors, setValidationErrors] = useState<{ [key: string]: string }>({});
  const [creating, setCreating] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [currentScope, setCurrentScope] = useState<Scope | null>(null);

  // Fetch goals for the active family scope
  const fetchGoals = async (scope?: Scope) => {
    try {
      const effectiveScope = scope ?? (await ensureSession());
      setCurrentScope(effectiveScope);
      const data = await listGoals(effectiveScope);
      setGoals(data);
    } catch (e) {
      handleError(e);
    }
  };

  // Form validation
  const validateGoal = (goal: GoalCreate): { [key: string]: string } => {
    const errors: { [key: string]: string } = {};
    if (!goal.name || goal.name.trim().length < 2) {
      errors.name = 'Name must be at least 2 characters';
    }
    if (goal.target_amount <= 0) {
      errors.target_amount = 'Target amount must be greater than 0';
    }
    if (goal.current_amount !== undefined && goal.current_amount < 0) {
      errors.current_amount = 'Current amount cannot be negative';
    }
    if (goal.monthly_contribution !== undefined && goal.monthly_contribution < 0) {
      errors.monthly_contribution = 'Monthly contribution cannot be negative';
    }
    if (goal.target_date) {
      const ts = Date.parse(goal.target_date);
      if (isNaN(ts)) {
        errors.target_date = 'Invalid date';
      }
    }
    return errors;
  };

  // Create goal handler
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    const errors = validateGoal(newGoal);
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }
    setValidationErrors({});
    setCreating(true);
    try {
      const scope = await ensureSession();
      await createGoal(scope, newGoal);
      await fetchGoals(scope);
      setNewGoal({
        name: '',
        target_amount: 0,
        current_amount: undefined,
        monthly_contribution: undefined,
        target_date: null,
      });
    } catch (err) {
      handleError(err);
    } finally {
      setCreating(false);
    }
  };

  // Delete goal handler with confirmation
  const deleteGoalHandler = async (goalId: string) => {
    const confirmed = window.confirm('Are you sure you want to delete this goal?');
    if (!confirmed) return;
    setDeletingId(goalId);
    try {
      const scope = await ensureSession();
      await deleteGoal(scope, goalId);
      await fetchGoals(scope);
    } catch (err) {
      handleError(err);
    } finally {
      setDeletingId(null);
    }
  };

  // Initial load
  useEffect(() => {
    const init = async () => {
      try {
        const scope = await ensureSession();
        await fetchGoals(scope);
      } catch (err) {
        handleError(err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  // Render helpers
  const renderProjection = (proj: any) => {
    if (!proj) return <span>Projection unavailable</span>;
    const years = (proj.months_required / 12).toFixed(1);
    const badgeStyle = {
      color: proj.is_achievable ? 'green' : 'red',
      fontWeight: 'bold' as const,
    };
    return (
      <span>
        {' '}| Months: {proj.months_required}
        {' '}| Years: {years}
        {' '}|{' '}
        <span style={badgeStyle}>
          {proj.is_achievable ? 'Achievable' : 'Needs adjustment'}
        </span>
      </span>
    );
  };

  if (loading) return <Spinner label="Loading goals…" />;
  if (error) return <ErrorBanner error={error} onRetry={() => fetchGoals()} />;

  return (
    <div>
      <h2>Goals</h2>

      {/* Goal creation form */}
      <form onSubmit={handleCreate} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Name"
          aria-label="Goal name"
          value={newGoal.name}
          onChange={e => setNewGoal({ ...newGoal, name: e.target.value })}
          required
        />
        {validationErrors.name && <div style={{ color: 'red' }}>{validationErrors.name}</div>}

        <input
          type="number"
          placeholder="Target Amount"
          aria-label="Target amount"
          value={newGoal.target_amount}
          onChange={e => setNewGoal({ ...newGoal, target_amount: Number(e.target.value) })}
          required
        />
        {validationErrors.target_amount && <div style={{ color: 'red' }}>{validationErrors.target_amount}</div>}

        <input
          type="number"
          placeholder="Current Amount"
          aria-label="Current amount"
          value={newGoal.current_amount ?? ''}
          onChange={e =>
            setNewGoal({
              ...newGoal,
              current_amount: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
        {validationErrors.current_amount && <div style={{ color: 'red' }}>{validationErrors.current_amount}</div>}

        <input
          type="number"
          placeholder="Monthly Contribution"
          aria-label="Monthly contribution"
          value={newGoal.monthly_contribution ?? ''}
          onChange={e =>
            setNewGoal({
              ...newGoal,
              monthly_contribution: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
        {validationErrors.monthly_contribution && <div style={{ color: 'red' }}>{validationErrors.monthly_contribution}</div>}

        <input
          type="date"
          placeholder="Target Date"
          aria-label="Target date"
          value={newGoal.target_date ?? ''}
          onChange={e => setNewGoal({ ...newGoal, target_date: e.target.value || null })}
        />
        {validationErrors.target_date && <div style={{ color: 'red' }}>{validationErrors.target_date}</div>}

        <button type="submit" disabled={creating}>
          {creating ? 'Creating…' : 'Create Goal'}
        </button>
      </form>

      {/* Goals list */}
      {goals.length === 0 ? (
        <div>No goals yet. Create one above.</div>
      ) : (
        <ul>
          {goals.map(goal => (
            <li key={goal.id} style={{ marginBottom: '0.5rem' }}>
              <strong>{goal.name}</strong> – Target: {goal.target_amount}
              {goal.projection && renderProjection(goal.projection)}
              <button
                onClick={() => deleteGoalHandler(goal.id)}
                style={{ marginLeft: '1rem' }}
                disabled={deletingId === goal.id}
              >
                {deletingId === goal.id ? 'Deleting…' : 'Delete'}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Goals;
