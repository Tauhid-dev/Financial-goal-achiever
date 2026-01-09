/**
 * Simple API client utilities for the frontend.
 * Uses the Vite environment variable VITE_API_BASE_URL as the base URL.
 */

const BASE_URL = (import.meta as any).env.VITE_API_BASE_URL || "";

// Token handling
export function setToken(token: string): void {
  localStorage.setItem("token", token);
}

export function getToken(): string | null {
  return localStorage.getItem("token");
}

export function clearToken(): void {
  localStorage.removeItem("token");
}

// Generic request helper
class ApiError extends Error {
  code?: string;
  status?: number;
  details?: any;
  constructor(message: string, status?: number, code?: string, details?: any) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

async function request<T = any>(path: string, opts: RequestInit = {}): Promise<T | null> {
  // Determine request body handling and headers
  const isFormData = typeof FormData !== "undefined" && opts.body instanceof FormData;

  // Start with provided headers
  const headers: Record<string, string> = {
    ...(opts.headers as Record<string, string> || {}),
  };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Set Content-Type for JSON bodies if not FormData and not already set
  let requestBody: any = undefined;
  if (opts.body === undefined) {
    requestBody = undefined;
  } else if (isFormData) {
    requestBody = opts.body;
    // Do not set Content-Type for FormData
  } else if (typeof opts.body === "string") {
    requestBody = opts.body;
  } else {
    requestBody = JSON.stringify(opts.body);
    if (!headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }
  }

  const fetchOptions: RequestInit = {
    ...opts,
    headers,
  };
  if (requestBody !== undefined) {
    fetchOptions.body = requestBody;
  }
  const response = await fetch(`${BASE_URL}${path}`, fetchOptions);

  if (!response.ok) {
    // Normalize error response
    const errorText = await response.text();
    let parsed: any = null;
    try {
      parsed = JSON.parse(errorText);
    } catch {
      // ignore parse error
    }
    const normalized = {
      status: response.status,
      code: response.status === 401 ? "UNAUTHORIZED" : parsed?.code || "UNKNOWN",
      message: parsed?.message || errorText || `HTTP ${response.status}`,
      details: parsed?.details,
    };
    if (response.status === 401) {
      clearToken();
    }
    throw new ApiError(normalized.message, normalized.status, normalized.code, normalized);
  }

  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text) as T;
  } catch {
    // If response is not JSON, return raw text
    return (text as unknown) as T;
  }
}

// Exported wrapper for compatibility
export async function apiFetch(path: string, opts: RequestInit = {}): Promise<any> {
  return request(path, opts);
}

/**
 * Helper to identify unauthorized errors.
 */
export function isUnauthorized(err: any): boolean {
  return err && err.code === "UNAUTHORIZED";
}

// Auth APIs
export async function loginAPI(formData: URLSearchParams): Promise<any> {
  const response = await fetch(`${BASE_URL}/api/auth/login`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Login error ${response.status}: ${errorText}`);
  }
  return response.json();
}

export async function meAPI(): Promise<any> {
  return request("/api/auth/me");
}
