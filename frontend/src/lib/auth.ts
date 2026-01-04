export function getToken(): string | null {
  return localStorage.getItem('token');
}

export function setToken(token: string): void {
  localStorage.setItem('token', token);
}

export function clearToken(): void {
  localStorage.removeItem('token');
}

/**
 * Perform login and store JWT token.
 */
export async function login(email: string, password: string): Promise<void> {
  const body = new URLSearchParams();
  body.append('username', email);
  body.append('password', password);

  const response = await fetch(`${(import.meta as any).env.VITE_API_BASE_URL || ''}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Login failed (${response.status}): ${err}`);
  }

  const data: { access_token: string } = await response.json();
  setToken(data.access_token);
}
