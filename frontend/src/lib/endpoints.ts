import { apiFetch } from "./api";
import {
  GoalCreate,
  GoalWithProjection,
  MonthlySummary,
  Document,
  Scope,
} from "./types";
import { familyPath } from "./scope";

export const SCOPES_LIST = "/scopes";

/**
 * Goals endpoints
 */
export const listGoals = async (scope: Scope): Promise<GoalWithProjection[]> => {
  return apiFetch(familyPath("goals", scope));
};

export const listScopes = async (): Promise<Scope[]> => {
  return apiFetch(SCOPES_LIST);
};

/* Removed local familyPath helper – use the one from scope.ts */

export const createGoal = async (
  scope: Scope,
  payload: GoalCreate
): Promise<GoalWithProjection> => {
  return apiFetch(familyPath("goals", scope), {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });
};

export const deleteGoal = async (scope: Scope, goalId: string): Promise<void> => {
  await apiFetch(`${familyPath("goals", scope)}/${goalId}`, {
    method: "DELETE",
  });
};

/**
 * Summary endpoints
 */
export const listSummaries = async (scope: Scope): Promise<MonthlySummary[]> => {
  return apiFetch(familyPath("summary", scope));
};

/**
 * Document endpoints
 */
export const listDocuments = async (scope: Scope): Promise<Document[]> => {
  return apiFetch(familyPath("documents", scope));
};

export const uploadDocument = async (scope: Scope, file: File): Promise<Document> => {
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
  scope: Scope,
  params?: { month?: string; limit?: number; offset?: number }
): Promise<any[]> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`${familyPath("transactions", scope)}${query}`);
};

/**
 * Placeholder for insights – returns unknown type
 */
export const getInsights = async (scope: Scope, params?: any): Promise<any> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`${familyPath("insights", scope)}${query}`);
};
