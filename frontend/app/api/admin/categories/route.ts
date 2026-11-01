import { NextRequest } from "next/server";
import { proxyAdminWrite } from "@/lib/admin-proxy-request";

export const dynamic = "force-dynamic";

export function PUT(request: NextRequest) {
  return proxyAdminWrite(request, "/api/admin/categories");
}
