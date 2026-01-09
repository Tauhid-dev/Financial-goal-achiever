import { Scope } from "./types";

export type ScopeRef = {
  kind: string; // e.g., "family"
  id: string;
};

export const getActiveScopeId = (): string | null => {
  return localStorage.getItem("active_scope_id");
};

export const setActiveScopeId = (id: string): void => {
  localStorage.setItem("active_scope_id", id);
};

export const clearActiveScopeId = (): void => {
  localStorage.removeItem("active_scope_id");
};

/**
 * Build API path for family‑scoped resources.
 * Example: familyPath("summary", scope) => "/api/summary/<family_id>"
 */
export const familyPath = (resource: string, scope: ScopeRef): string => {
  return `/api/${resource}/${scope.id}`;
};
