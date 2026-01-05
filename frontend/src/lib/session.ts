import { apiFetch, meAPI } from "./api";

export const SCOPE_TYPE_KEY = "scope_type";
export const SCOPE_ID_KEY = "scope_id";

export const getScope = (): { scope_type: string; scope_id: string } | null => {
  const type = localStorage.getItem(SCOPE_TYPE_KEY);
  const id = localStorage.getItem(SCOPE_ID_KEY);
  return type && id ? { scope_type: type, scope_id: id } : null;
};

export const setScope = (type: string, id: string): void => {
  localStorage.setItem(SCOPE_TYPE_KEY, type);
  localStorage.setItem(SCOPE_ID_KEY, id);
};

/**
 * Initialise session – verifies auth token and resolves the default scope.
 * Returns generic scope fields plus a backward‑compatible `familyId` when applicable.
 */
export const ensureSession = async (): Promise<{
  scopeType: string;
  scopeId: string;
  familyId?: string;
}> => {
  // Verify token via /api/auth/me (throws on 401)
  await meAPI();

  // Check if we already have a stored scope
  const stored = getScope();
  if (stored) {
    return {
      scopeType: stored.scope_type,
      scopeId: stored.scope_id,
      familyId: stored.scope_type === "family" ? stored.scope_id : undefined,
    };
  }

  // Fetch list of scopes
  const scopesResponse = await apiFetch("/api/scopes");
  const scopes = await scopesResponse.json();
  if (Array.isArray(scopes) && scopes.length > 0) {
    const first = scopes[0];
    const scopeType = first.type;
    const scopeId = String(first.id);
    setScope(scopeType, scopeId);
    return {
      scopeType,
      scopeId,
      familyId: scopeType === "family" ? scopeId : undefined,
    };
  }

  // Fallback to legacy family endpoint
  const data = await apiFetch("/api/me/default-family");
  const scopeType = "family";
  const scopeId = String(data.family_id);
  setScope(scopeType, scopeId);
  return {
    scopeType,
    scopeId,
    familyId: scopeId,
  };
};
