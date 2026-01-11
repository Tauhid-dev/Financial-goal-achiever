import { describe, it, expect, vi } from 'vitest';
import * as api from '../api';
import { getInsights, listGoals } from '../endpoints';
import { familyPath } from '../scope';
import type { Scope } from '../types';

const mockLocalStorage = {
  getItem: vi.fn().mockReturnValue(null),
  setItem: vi.fn(),
  removeItem: vi.fn(),
};
(globalThis as any).localStorage = mockLocalStorage;

const mockScope: Scope = { kind: "family", id: "family1" };

describe('Additional frontend regression tests', () => {
  it('non‑401 response is not considered unauthorized', () => {
    const err = { code: 'SOME_OTHER_ERROR', status: 403 };
    expect(api.isUnauthorized(err)).toBe(false);
  });

  it('clearToken removes token from localStorage', () => {
    api.setToken('test-token');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('token', 'test-token');
    api.clearToken();
    expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('token');
  });

  it('endpoints use correct path builder', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, text: async () => '[]' });
    vi.spyOn(api, 'apiFetch').mockImplementation(fetchMock);
    await listGoals(mockScope);
    const expectedPath = familyPath('goals', mockScope);
    expect(fetchMock).toHaveBeenCalledWith(expectedPath);
  });

  it('getInsights builds correct query string', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, text: async () => '[]' });
    vi.spyOn(api, 'apiFetch').mockImplementation(fetchMock);
    await getInsights(mockScope, '2024-01');
    const expectedPath = `${familyPath('insights', mockScope)}?month=2024-01`;
    expect(fetchMock).toHaveBeenCalledWith(expectedPath);
  });
});
