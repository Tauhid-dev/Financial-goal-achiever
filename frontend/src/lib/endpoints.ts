import { apiFetch } from "./api";
import {
  GoalCreate,
  GoalWithProjection,
  MonthlySummary,
  Document,
} from "./types";

/**
 * Goals endpoints
 */
export const listGoals = async (familyId: string): Promise<GoalWithProjection[]> => {
  return apiFetch(`/api/goals/${familyId}`);
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

/**
 * Placeholder for insights – returns unknown type
 */
export const getInsights = async (familyId: string, params?: any): Promise<any> => {
  const query = params ? `?${new URLSearchParams(params as any).toString()}` : "";
  return apiFetch(`/api/insights/${familyId}${query}`);
};
