import { adminApiBase, adminUpstream } from "../lib/admin-proxy";
import { formatRate, formatSar } from "../lib/admin-view";

describe("admin proxy", () => {
  const previous = process.env.NEXT_PUBLIC_API_URL;

  afterEach(() => {
    process.env.NEXT_PUBLIC_API_URL = previous;
  });

  test("builds the backend url without embedding a token", () => {
    process.env.NEXT_PUBLIC_API_URL = "https://api.nawahouse.shop/";
    expect(adminApiBase()).toBe("https://api.nawahouse.shop");
    expect(adminUpstream("/api/admin/overview", "?from=2026-10-01")).toBe(
      "https://api.nawahouse.shop/api/admin/overview?from=2026-10-01"
    );
    expect(adminUpstream("/api/admin/overview")).not.toContain("ADMIN_TOKEN");
  });
});

describe("admin figures", () => {
  test("formats database numbers without inventing them", () => {
    expect(formatSar(0)).toBe(new Intl.NumberFormat("ar-SA").format(0));
    expect(formatRate(0)).toBe("0.0%");
    expect(formatRate(0.125)).toBe("12.5%");
  });
});
