declare const global: any;

import { apiFetch, isUnauthorized } from '../api';
import { vi, it, expect } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

it('apiFetch throws ApiError with UNAUTHORIZED code on 401', async () => {
  // @ts-ignore
  global.fetch.mockResolvedValueOnce({
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
