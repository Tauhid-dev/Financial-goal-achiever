/**
 * Simple API client utilities for the frontend.
 * Uses the Vite environment variable VITE_API_BASE_URL as the base URL.
 */

export interface Token {
  access_token: string;
  token_type: string;
}

const TOKEN_KEY = 'auth_token';

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Wrapper around fetch that automatically prefixes the base URL,
 * adds JSON headers, and attaches the Authorization header when auth is true.
 *
 * @param path API path, e.g. `/api/auth/login`
 * @param options fetch options: method, body, auth flag
 */
export async function apiFetch(
  path: string,
  {
    method = 'GET',
    body,
    auth = false,
    headers = {},
  }: {
    method?: string;
    body?: any;
    auth?: boolean;
    headers?: Record<string, string>;
  } = {}
): Promise<any> {
  const baseUrl = (import.meta as any).env.VITE_API_BASE_URL;
  const url = `${baseUrl}${path}`;

  const fetchHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers,
  };

  if (auth) {
    const token = getToken();
    if (token) {
      fetchHeaders['Authorization'] = `Bearer ${token}`;
    }
  }

  const response = await fetch(url, {
    method,
    headers: fetchHeaders,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }

  const text = await response.text();
  return text ? JSON.parse(text) : null;
}
