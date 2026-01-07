import { apiFetch, meAPI } from "./api";
import { ScopeRef } from "./scope";

export const SCOPE_KIND_KEY = "scope_kind";
export const SCOPE_ID_KEY = "scope_id";

export const getScope = (): ScopeRef | null => {
  const kind = localStorage.getItem(SCOPE_KIND_KEY) as ScopeRef["kind"] | null;
  const id = localStorage.getItem(SCOPE_ID_KEY);
  return kind && id ? { kind, id } : null;
};

export const setScope = (scope: ScopeRef): void => {
  localStorage.setItem(SCOPE_KIND_KEY, scope.kind);
  localStorage.setItem(SCOPE_ID_KEY, scope.id);
}

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
  const scopes = await apiFetch("/api/me/scopes");
  if (Array.isArray(scopes) && scopes.length > 0) {
    const first = scopes[0];
    const scope: ScopeRef = { kind: first.kind as ScopeRef["kind"], id: String(first.id) };
    setScope(scope);
    return scope;
  }

  // Fallback to legacy default‑family endpoint
  const data = await apiFetch("/api/me/default-family");
  const scope: ScopeRef = { kind: "family", id: String(data.family_id) };
  setScope(scope);
  return scope;
};
