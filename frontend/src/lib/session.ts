import { apiFetch, meAPI } from "./api";
import { ScopeRef } from "./scope";

export const getScope = (): ScopeRef | null => {
  const id = localStorage.getItem("active_scope_id");
  return id ? { id } : null;
};

export const setScope = (scope: ScopeRef): void => {
  localStorage.setItem("active_scope_id", scope.id);
};

/**
 * Initialise session – verifies auth token and resolves the default scope.
 * Returns a ScopeRef (family MVP now).
 */
export const ensureSession = async (): Promise<ScopeRef> => {
  // Verify token via /api/auth/me (throws on 401)
  await meAPI();

  // Check if we already have a stored scope
  const stored = getScope();
  if (stored) {
    return stored;
  }

  // Fetch list of scopes
  const scopes = await apiFetch("/api/scopes");
  if (Array.isArray(scopes) && scopes.length > 0) {
    const first = scopes[0];
    const scope: ScopeRef = { id: String(first.id) };
    setScope(scope);
    return scope;
  }

  // Fallback to legacy default‑family endpoint
  const data = await apiFetch("/api/me/default-family");
  const scope: ScopeRef = { id: String(data.family_id) };
  setScope(scope);
  return scope;
};
