import { NextRequest, NextResponse } from "next/server";
import { ADMIN_COOKIE, adminUpstream } from "@/lib/admin-proxy";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  let body: { token?: unknown; username?: unknown; password?: unknown } = {};
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 });
  }

  let upstream: Response;
  try {
    upstream = await fetch(adminUpstream("/api/admin/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        token: typeof body.token === "string" ? body.token : undefined,
        username: typeof body.username === "string" ? body.username : undefined,
        password: typeof body.password === "string" ? body.password : undefined,
      }),
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ ok: false, error: "backend" }, { status: 502 });
  }

  if (!upstream.ok) {
    return NextResponse.json({ ok: false }, { status: upstream.status === 503 ? 503 : 401 });
  }

  const data = (await upstream.json()) as { session?: string };
  if (!data.session) {
    return NextResponse.json({ ok: false }, { status: 502 });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set(ADMIN_COOKIE, data.session, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: 60 * 60 * 12,
  });
  return response;
}
