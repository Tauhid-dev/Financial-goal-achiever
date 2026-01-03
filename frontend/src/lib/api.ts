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
async function request(path: string, opts: RequestInit = {}): Promise<any> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> || {}),
  };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Determine request body handling:
  let requestBody: any = undefined;
  if (typeof opts.body === "string") {
    requestBody = opts.body;
  } else if (opts.body !== undefined) {
    requestBody = JSON.stringify(opts.body);
  }

    const response = await fetch(`${BASE_URL}${path}`, {
      ...opts,
      headers,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });

  if (!response.ok) {
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
