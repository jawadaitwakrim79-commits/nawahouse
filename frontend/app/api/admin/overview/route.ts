import { NextRequest } from "next/server";
import { proxyAdminGet } from "@/lib/admin-proxy-request";

export const dynamic = "force-dynamic";

export function GET(request: NextRequest) {
  return proxyAdminGet(request, "/api/admin/overview");
}
