import { apiFetch } from "./api";
import {
  GoalCreate,
  GoalWithProjection,
  MonthlySummary,
  Document,
  Scope,
} from "./types";
import { ScopeRef, familyPath } from "./scope";

/**
 * Goals endpoints
 */
export const listGoals = async (scope: ScopeRef): Promise<GoalWithProjection[]> => {
  return apiFetch(familyPath("goals", scope));
};

export const listScopes = async (): Promise<Scope[]> => {
  return apiFetch("/api/scopes");
};

/* Removed local familyPath helper – use the one from scope.ts */

export const createGoal = async (
  scope: ScopeRef,
  payload: GoalCreate
): Promise<GoalWithProjection> => {
  return apiFetch(familyPath("goals", scope), {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });
};

export const deleteGoal = async (scope: ScopeRef, goalId: string): Promise<void> => {
  await apiFetch(`${familyPath("goals", scope)}/${goalId}`, {
    method: "DELETE",
  });
};

/**
 * Summary endpoints
 */
export const listSummaries = async (scope: ScopeRef): Promise<MonthlySummary[]> => {
  return apiFetch(familyPath("summary", scope));
};

/**
 * Document endpoints
 */
export const listDocuments = async (scope: ScopeRef): Promise<Document[]> => {
  return apiFetch(familyPath("documents", scope));
};

export const uploadDocument = async (scope: ScopeRef, file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch(familyPath("documents", scope), {
    method: "POST",
    body: formData,
  });
};

/**
 * Transactions endpoint – returns a list of transactions for a family.
 */
export const listTransactions = async (
  scope: ScopeRef,
  params?: { month?: string; limit?: number; offset?: number }
): Promise<any[]> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`${familyPath("transactions", scope)}${query}`);
};

/**
 * Placeholder for insights – returns unknown type
 */
export const getInsights = async (scope: ScopeRef, params?: any): Promise<any> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`${familyPath("insights", scope)}${query}`);
};
