export async function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has('content-type')) {
    headers.set('content-type', 'application/json');
  }
  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'same-origin',
  });
  if (response.status === 401 && !url.startsWith('/api/auth/')) {
    window.dispatchEvent(new Event('pulse:session-expired'));
  }
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.error || body?.message || `Request failed (${response.status}).`);
  }
  return response.status === 204 ? null : response.json();
}
