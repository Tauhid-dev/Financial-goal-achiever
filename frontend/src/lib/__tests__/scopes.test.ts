import { apiFetch } from "../api";
import { listScopes, getDefaultScope } from "../endpoints";
import { Scope } from "../types";

vi.mock("../api");

// Cast to any to avoid type issues
const mockedApiFetch = apiFetch as any;

describe("Scope API wrappers", () => {
  const mockScopes: Scope[] = [
    { id: "fam1", kind: "family" },
    { id: "fam2", kind: "family" },
  ];

  afterEach(() => {
    mockedApiFetch.mockReset();
  });

  test("listScopes returns parsed array", async () => {
    mockedApiFetch.mockResolvedValueOnce(mockScopes);
    const result = await listScopes();
    expect(result).toEqual(mockScopes);
    expect(mockedApiFetch).toHaveBeenCalledWith("/api/scopes");
  });

  test("getDefaultScope returns parsed scope", async () => {
    const defaultScope = mockScopes[0];
    mockedApiFetch.mockResolvedValueOnce(defaultScope);
    const result = await getDefaultScope();
    expect(result).toEqual(defaultScope);
    expect(mockedApiFetch).toHaveBeenCalledWith("/api/scopes/default");
  });
});
