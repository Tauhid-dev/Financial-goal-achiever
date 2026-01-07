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
    if (response.status === 401) {
      clearToken();
    }
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }

  const text = await response.text();
  return text ? JSON.parse(text) : null;
}

// Exported wrapper for compatibility
export async function apiFetch(path: string, opts: RequestInit = {}): Promise<any> {
  return request(path, opts);
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
