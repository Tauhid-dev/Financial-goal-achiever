import { apiFetch } from "./api";
import {
  GoalCreate,
  GoalWithProjection,
  MonthlySummary,
  Document,
  Scope,
} from "./types";

/**
 * Goals endpoints
 */
export const listGoals = async (familyId: string): Promise<GoalWithProjection[]> => {
  return apiFetch(`/api/goals/${familyId}`);
};

export const listScopes = async (): Promise<Scope[]> => {
  return apiFetch("/api/scopes");
};

export const familyPath = (familyId: string, suffix: string): string => {
  // Centralised              ...
  return `/api/${suffix}/${familyId}`;
};

export const createGoal = async (
  familyId: string,
  payload: GoalCreate
): Promise<GoalWithProjection> => {
  return apiFetch(`/api/goals/${familyId}`, {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });
};

export const deleteGoal = async (familyId: string, goalId: string): Promise<void> => {
  await apiFetch(`/api/goals/${familyId}/${goalId}`, {
    method: "DELETE",
  });
};

/**
 * Summary endpoints
 */
export const listSummaries = async (familyId: string): Promise<MonthlySummary[]> => {
  return apiFetch(`/api/summary/${familyId}`);
};

/**
 * Document endpoints
 */
export const listDocuments = async (familyId: string): Promise<Document[]> => {
  return apiFetch(`/api/documents/${familyId}`);
};

export const uploadDocument = async (familyId: string, file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append("file", file);
  return apiFetch(`/api/documents/${familyId}`, {
    method: "POST",
    body: formData,
  });
};

/**
 * Transactions endpoint – returns a list of transactions for a family.
 */
export const listTransactions = async (
  familyId: string,
  params?: { month?: string; limit?: number; offset?: number }
): Promise<any[]> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`/api/transactions/${familyId}${query}`);
};

/**
 * Placeholder for insights – returns unknown type
 */
export const getInsights = async (familyId: string, params?: any): Promise<any> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`/api/insights/${familyId}${query}`);
};
