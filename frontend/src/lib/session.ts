import { apiFetch, meAPI } from "./api";
import { ScopeRef } from "./scope";

export const getScope = (): ScopeRef | null => {
  const id = localStorage.getItem("active_scope_id");
  const kind = localStorage.getItem("active_scope_kind") ?? "family";
  return id ? { id, kind } : null;
};

export const setScope = (scope: ScopeRef): void => {
  localStorage.setItem("active_scope_id", scope.id);
  localStorage.setItem("active_scope_kind", scope.kind);
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
    const scope: ScopeRef = {
      id: String(first.id),
      kind: String(first.kind ?? "family")
    };
    setScope(scope);
    return scope;
}

  // Fallback to legacy default‑family endpoint
const data = await apiFetch("/api/me/default-family");
const scope: ScopeRef = {
  id: String(data.family_id),
  kind: "family"
};
setScope(scope);
return scope;
};
