import React, { useEffect, useState } from "react";
import { apiFetch, clearToken } from "../lib/api";
import { GoalWithProjection, MonthlySummary } from "../lib/types";

export default function AppHome() {
  const [familyId, setFamilyId] = useState<string>("");
  const [summary, setSummary] = useState<MonthlySummary[]>([]);
  const [goals, setGoals] = useState<GoalWithProjection[]>([]);
  const [error, setError] = useState<string>("");

  // fetch default family id
  useEffect(() => {
    const fetchFamily = async () => {
      try {
        const data = await apiFetch("/api/families/default");
        if (data && data.id) {
          setFamilyId(String(data.id));
        } else {
          const manual = prompt("Enter your family ID:");
          if (manual) setFamilyId(manual);
        }
      } catch {
        const manual = prompt("Enter your family ID:");
        if (manual) setFamilyId(manual);
      }
    };
    fetchFamily();
  }, []);

  const loadSummary = async () => {
    if (!familyId) return;
    try {
      const data = await apiFetch(`/api/summary/${familyId}`);
      setSummary(data || []);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const loadGoals = async () => {
    if (!familyId) return;
    try {
      const data = await apiFetch(`/api/goals/${familyId}`);
      setGoals(data || []);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleLogout = () => {
    clearToken();
    window.location.reload();
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Financial Dashboard</h2>
      <button onClick={handleLogout}>Logout</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <label>Family ID: </label>
        <input value={familyId} onChange={(e) => setFamilyId(e.target.value)} />
        <button onClick={loadSummary}>Load Summary</button>
        <button onClick={loadGoals}>Load Goals</button>
      </div>

      {summary.length > 0 && (
        <section>
          <h3>Monthly Summary</h3>
          <table border={1}>
            <thead>
              <tr>
                <th>Month</th>
                <th>Income</th>
                <th>Expenses</th>
                <th>Savings</th>
                <th>Savings Rate</th>
              </tr>
            </thead>
            <tbody>
              {summary.map((s) => (
                <tr key={s.id}>
                  <td>{s.month}</td>
                  <td>{s.income}</td>
                  <td>{s.expenses}</td>
                  <td>{s.savings}</td>
                  <td>{s.savings_rate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {goals.length > 0 && (
        <section>
          <h3>Goals</h3>
          <table border={1}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Target Amount</th>
                <th>Current Amount</th>
                <th>Monthly Contribution</th>
                <th>Months Required</th>
                <th>Years Required</th>
                <th>Achievable</th>
              </tr>
            </thead>
            <tbody>
              {goals.map((g) => (
                <tr key={g.id}>
                  <td>{g.name}</td>
                  <td>{g.target_amount}</td>
                  <td>{g.current_amount}</td>
                  <td>{g.monthly_contribution}</td>
                  <td>{g.projection?.months_required ?? "-"}</td>
                  <td>{g.projection?.years_required ?? "-"}</td>
                  <td>{g.projection?.is_achievable ? "Yes" : "No"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
