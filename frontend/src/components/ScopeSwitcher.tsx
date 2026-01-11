import React, { useEffect, useState } from "react";
import { listScopes } from "../lib/endpoints";
import { getScope, setScope } from "../lib/session";
import { Scope, ScopeItem } from "../lib/types";

/**
 * UI component to select the active scope.
 * On mount it loads available scopes, persists the selected one,
 * and triggers a page reload on change (simple MVP behavior).
 */
export const ScopeSwitcher: React.FC = () => {
  const [scopes, setScopes] = useState<ScopeItem[]>([]);
  const [selected, setSelected] = useState<string>("");

  useEffect(() => {
    (async () => {
      const fetched = await listScopes();
      setScopes(fetched);
      const stored = getScope();
      if (stored) {
        setSelected(JSON.stringify(stored));
      } else if (fetched.length > 0) {
        const first = fetched[0];
        const ref: Scope = { kind: first.kind, id: first.id };
        setScope(ref);
        setSelected(JSON.stringify(ref));
      }
    })();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelected(value);
    const parsed: Scope = JSON.parse(value);
    setScope(parsed);
    // Simple reload to refresh data
    window.location.reload();
  };

  if (scopes.length === 0) {
    return <div>No scopes available</div>;
  }

  return (
    <select value={selected} onChange={handleChange} style={{ marginLeft: "1rem" }}>
      {scopes.map((s) => {
        const label = s.label ?? `${s.kind}:${s.id.slice(0, 8)}`;
        const value = JSON.stringify({ kind: s.kind, id: s.id });
        return (
          <option key={s.id} value={value}>
            {label}
          </option>
        );
      })}
    </select>
  );
};
