import { NextRequest } from "next/server";
import { proxyAdminGet, proxyAdminWrite } from "@/lib/admin-proxy-request";

export const dynamic = "force-dynamic";

export function GET(request: NextRequest) {
  return proxyAdminGet(request, "/api/admin/settings");
}

export function PUT(request: NextRequest) {
  return proxyAdminWrite(request, "/api/admin/settings");
}
