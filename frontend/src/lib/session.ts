import { apiFetch, meAPI } from "./api";

/**
 * Session helper – determines the current user and default family.
 * Stores the family ID in localStorage under "family_id".
 */

export const FAMILY_ID_KEY = "family_id";

/**
 * Retrieve stored family ID.
 */
export const getFamilyId = (): string | null => {
  return localStorage.getItem(FAMILY_ID_KEY);
};

/**
 * Store family ID.
 */
export const setFamilyId = (familyId: string): void => {
  localStorage.setItem(FAMILY_ID_KEY, familyId);
};

/**
 * Initialise session:
 *  - Verify token via /api/auth/me (throws if invalid)
 *  - Attempt to fetch default family via /api/me/default-family
 *    (fallback to /api/families/default if endpoint missing)
 *  - Store family ID for later use.
 */
export const ensureSession = async (): Promise<{ user: any; familyId: string }> => {
  // Get current user (throws on 401)
  const user = await meAPI();

  // Check if familyId already stored
  let familyId = getFamilyId();
  if (familyId) {
    return { user, familyId };
  }

  // Try default-family endpoint
  try {
    const data = await apiFetch("/api/me/default-family");
    if (data && data.id) {
      familyId = String(data.id);
      setFamilyId(familyId);
      return { user, familyId };
    }
  } catch {
    // ignore, fallback
  }

  // Fallback to families/default
  const fallback = await apiFetch("/api/families/default");
  if (fallback && fallback.id) {
    familyId = String(fallback.id);
    setFamilyId(familyId);
    return { user, familyId };
  }

  throw new Error("Unable to determine default family ID");
};
