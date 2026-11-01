import { NextResponse } from "next/server";
import { adminApiBase } from "@/lib/admin-proxy";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const upstream = await fetch(`${adminApiBase()}/api/store`, { cache: "no-store" });
    const text = await upstream.text();
    return new NextResponse(text, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch {
    return NextResponse.json({ ok: false }, { status: 502 });
  }
}
