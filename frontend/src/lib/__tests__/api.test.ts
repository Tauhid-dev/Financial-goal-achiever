import { describe, it, expect, vi } from 'vitest';
import { apiFetch, isUnauthorized } from '../api';

const mockLocalStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {},
};
(globalThis as any).localStorage = mockLocalStorage;

// Mock fetch globally
globalThis.fetch = vi.fn();

it('apiFetch throws ApiError with UNAUTHORIZED code on 401', async () => {
  // @ts-ignore
  globalThis.fetch.mockResolvedValueOnce({
    ok: false,
    status: 401,
    text: async () => '',
  });

await expect(apiFetch('/test')).rejects.toMatchObject({
  code: 'UNAUTHORIZED',
  status: 401,
});
});

it('isUnauthorized correctly identifies UNAUTHORIZED errors', () => {
  const err = { code: 'UNAUTHORIZED', status: 401 };
  expect(isUnauthorized(err)).toBe(true);
});
