import { Scope } from "./types";

export type ScopeRef = { id: string };

export const getActiveScopeId = (): string | null => {
  return localStorage.getItem("active_scope_id");
};

export const setActiveScopeId = (id: string): void => {
  localStorage.setItem("active_scope_id", id);
};

export const clearActiveScopeId = (): void => {
  localStorage.removeItem("active_scope_id");
};

export const familyPath = (resource: string, scope: ScopeRef): string => {
  // For MVP, treat scope.id as family_id
  return `/api/families/${scope.id}/${resource}`;
};
