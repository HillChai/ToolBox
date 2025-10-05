import { API_BASE, API_KEY } from "./config";
export async function postForm<T>(path: string, form: FormData): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: API_KEY ? { "X-API-Key": API_KEY } : undefined,
    body: form,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json() as Promise<T>;
}
