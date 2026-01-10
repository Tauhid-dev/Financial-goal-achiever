import { Scope } from "./types";

export const getActiveScopeId = (): string | null => {
  return localStorage.getItem("active_scope_id");
};

export const setActiveScopeId = (id: string): void => {
  localStorage.setItem("active_scope_id", id);
};

export const clearActiveScopeId = () => {
  localStorage.removeItem("active_scope_id");
};

/**
 * Helper to extract the id from a Scope
 */
export const scopeId = (scope: Scope): string => scope.id;

/**
 * Build API path for scoped resources.
 * Example: familyPath("summary", scope) => "/api/summary/<scope.id>"
 */
export const familyPath = (resource: string, scope: Scope) => {
  return `/api/${resource}/${scope.id}`;
};
