export interface AdminOrder {
  public_id: string;
  customer_name: string;
  phone_e164: string;
  total_sar: number;
  status: string;
  sheet_status: string;
  main_units: number;
  upsell_slug: string | null;
  page_url?: string | null;
  client_ip?: string | null;
  client_event_id?: string | null;
  created_at: string | null;
  items: { slug: string; quantity: number; pricing: string }[];
}

export interface AdminOverview {
  from: string;
  to: string;
  orders_count: number;
  orders_revenue: number;
  conversion_rate: number;
  total_clicks: number;
  valid_ksa_clicks: number;
  vpn_clicks: number;
  foreign_clicks: number;
  unique_sessions: number;
  series: { date: string; clicks: number; orders: number }[];
  top_products: { slug: string; qty: number }[];
  orders: AdminOrder[];
}

export function formatSar(value: number): string {
  return new Intl.NumberFormat("ar-SA").format(value);
}

export function formatRate(rate: number): string {
  if (!Number.isFinite(rate)) return "—";
  return `${(rate * 100).toFixed(1)}%`;
}

export function formatWhen(iso: string | null): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return new Intl.DateTimeFormat("ar-SA", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Riyadh",
  }).format(date);
}
