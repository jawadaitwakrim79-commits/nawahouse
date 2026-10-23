"use client";

import { useEffect, useRef } from "react";
import { usePathname, useSearchParams } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "";
const SESSION_KEY = "nawa_session_id";

function getOrCreateSessionId(): string {
  if (typeof window === "undefined") return "";
  try {
    let sid = window.sessionStorage.getItem(SESSION_KEY);
    if (!sid) {
      sid = crypto.randomUUID();
      window.sessionStorage.setItem(SESSION_KEY, sid);
    }
    return sid;
  } catch {
    return "anon-" + Math.random().toString(36).slice(2);
  }
}

/**
 * Fires a POST to /api/track-click on every pathname change.
 * Backend resolves IP → country + VPN flag and persists one PageClick row.
 * Fire-and-forget; never blocks the UI.
 */
export function ClickTracker() {
  const pathname = usePathname();
  const search = useSearchParams();
  const lastPath = useRef<string | null>(null);

  useEffect(() => {
    if (pathname.startsWith("/admin")) return;
    const fullPath = pathname + (search.toString() ? `?${search.toString()}` : "");
    if (lastPath.current === fullPath) return;
    lastPath.current = fullPath;

    const sid = getOrCreateSessionId();
    if (!sid) return;

    const body = {
      session_id: sid,
      path: fullPath,
      referrer: document.referrer || null,
      utm_source: search.get("utm_source"),
      utm_medium: search.get("utm_medium"),
      utm_campaign: search.get("utm_campaign"),
      fbclid: search.get("fbclid"),
      ttclid: search.get("ttclid"),
      sc_click_id: search.get("sc_click_id") || search.get("ScCid"),
    };

    try {
      // Prefer sendBeacon so page nav doesn't cancel the request.
      const blob = new Blob([JSON.stringify(body)], { type: "application/json" });
      const url = `${API}/api/track-click`;
      if (navigator.sendBeacon && navigator.sendBeacon(url, blob)) return;
      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        keepalive: true,
      }).catch(() => {});
    } catch {
      /* ignore */
    }
  }, [pathname, search]);

  return null;
}
