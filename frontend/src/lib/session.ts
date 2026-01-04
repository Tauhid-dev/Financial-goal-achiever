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
export const initSession = async (): Promise<void> => {
  // Verify token – will throw on 401
  await meAPI();

  // Try default-family endpoint
  try {
    const data = await apiFetch("/api/me/default-family");
    if (data && data.id) {
      setFamilyId(String(data.id));
      return;
    }
  } catch {
    // Endpoint may not exist
  }

  // Fallback: use families/default
  const fallback = await apiFetch("/api/families/default");
  if (fallback && fallback.id) {
    setFamilyId(String(fallback.id));
  } else {
    console.warn("Unable to determine default family ID.");
  }
};
