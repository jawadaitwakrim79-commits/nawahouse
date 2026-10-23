import { NextRequest } from "next/server";
import { proxyAdminGet } from "@/lib/admin-proxy-request";

export const dynamic = "force-dynamic";

export function GET(request: NextRequest, context: { params: Promise<{ id: string }> }) {
  return context.params.then((params) =>
    proxyAdminGet(request, `/api/admin/orders/${encodeURIComponent(params.id)}`)
  );
}
