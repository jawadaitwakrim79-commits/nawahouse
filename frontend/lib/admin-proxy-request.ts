import { NextRequest, NextResponse } from "next/server";
import { ADMIN_COOKIE, adminUpstream } from "@/lib/admin-proxy";

export async function proxyAdminGet(request: NextRequest, path: string) {
  const session = request.cookies.get(ADMIN_COOKIE)?.value;
  if (!session) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }

  const search = new URL(request.url).search;
  let upstream: Response;
  try {
    upstream = await fetch(adminUpstream(path, search), {
      headers: { Authorization: `Bearer ${session}` },
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ ok: false, error: "backend" }, { status: 502 });
  }

  const text = await upstream.text();
  return new NextResponse(text, {
    status: upstream.status,
    headers: { "Content-Type": "application/json" },
  });
}
