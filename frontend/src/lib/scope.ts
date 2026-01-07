/**
 * Scope abstraction for future extensibility.
 * Currently only "family" is supported by the backend.
 */

export type ScopeKind = "family" | "individual" | "business";

export type ScopeRef = {
  kind: ScopeKind;
  id: string;
};

/**
 * Convert a ScopeRef to a cache‑friendly key.
 * Example: { kind: "family", id: "123" } => "family:123"
 */
export function toScopeKey(scope: ScopeRef): string {
  return `${scope.kind}:${scope.id}`;
}

/**
 * Build a backend path for family‑only resources.
 * Throws a friendly error if a non‑family kind is used (backend does not support it yet).
 */
export function familyPath(suffix: string, scope: ScopeRef): string {
  if (scope.kind !== "family") {
    throw new Error(`Scope kind '${scope.kind}' not supported by backend yet`);
  }
  // Ensure no leading slash on suffix
  const clean = suffix.startsWith("/") ? suffix.slice(1) : suffix;
  return `/api/${clean}/${scope.id}`;
}

/**
 * Enforce that the current scope is a family scope.
 * Throws an error if no scope is selected or if the scope kind is not "family".
 */
export function requireFamilyScope(scope: ScopeRef | null): { familyId: string } {
  if (!scope) {
    throw new Error("No scope selected");
  }
  if (scope.kind !== "family") {
    throw new Error("This MVP supports family scopes only");
  }
  return { familyId: scope.id };
}
