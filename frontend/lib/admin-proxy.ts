/**
 * Server-side helpers for the website admin.
 * ADMIN_TOKEN is never read here. The browser sends it once to the backend,
 * and only the short-lived session cookie is kept.
 */

export const ADMIN_COOKIE = "nawa_admin_session";

export function adminApiBase(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL || "https://api.nawahouse.shop";
  return raw.replace(/\/$/, "");
}

export function adminUpstream(path: string, search = ""): string {
  const base = adminApiBase();
  const query = search ? (search.startsWith("?") ? search : `?${search}`) : "";
  return `${base}${path}${query}`;
}
