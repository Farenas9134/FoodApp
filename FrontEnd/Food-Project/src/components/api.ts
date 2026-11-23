const API = import.meta.env.VITE_API_URL ?? "";

let csrfToken: string | null = null;

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function fetchCsrf(): Promise<string> {
  const res = await fetch(`${API}/csrf`, { credentials: "include" });
  const data = await res.json();
  csrfToken = data.csrf_token;
  return csrfToken!;
}

export function setCsrfToken(token: string | undefined) {
  if (token) csrfToken = token;
}

export async function api<T = unknown>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const method = (init.method ?? "GET").toUpperCase();
  const needsCsrf = method !== "GET" && method !== "HEAD";

  if (needsCsrf && !csrfToken) await fetchCsrf();

  const res = await fetch(`${API}${path}`, {
    ...init,
    credentials: "include", // send and accept cookies cross-origin
    headers: {
      "Content-Type": "application/json",
      ...(needsCsrf && csrfToken ? { "X-CSRF-Token": csrfToken } : {}),
      ...init.headers,
    },
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(res.status, data.error ?? "Request failed");

  setCsrfToken((data as { csrf_token?: string }).csrf_token); // login/logout refresh it
  return data as T;
}