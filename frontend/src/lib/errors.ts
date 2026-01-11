export function getErrorMessage(err: unknown): string {
  if (typeof err === 'string') return err;
  if (err instanceof Error && err.message) return err.message;
  const anyErr = err as any;
  if (anyErr?.message && typeof anyErr.message === 'string') return anyErr.message;
  if (anyErr?.detail && typeof anyErr.detail === 'string') return anyErr.detail;
  return 'Something went wrong. Please try again.';
}

export function isUnauthorized(err: unknown): boolean {
  const anyErr = err as any;
  return (
    anyErr?.code === 'UNAUTHORIZED' ||
    anyErr?.status === 401 ||
    anyErr?.statusCode === 401
  );
}
