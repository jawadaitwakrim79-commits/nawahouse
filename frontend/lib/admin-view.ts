export interface AdminOrder {
  public_id: string;
  customer_name: string;
  phone_e164: string;
  total_mad: number;
  shipping_mad?: number;
  city?: string | null;
  address?: string | null;
  delivery_notes?: string | null;
  status: string;
  sheet_status: string;
  main_units: number;
  upsell_slug: string | null;
  page_url?: string | null;
  client_ip?: string | null;
  client_event_id?: string | null;
  created_at: string | null;
  items: { slug: string; name_ar?: string; quantity: number; pricing: string; variant?: string | null }[];
}

export interface AdminOverview {
  from: string;
  to: string;
  orders_count: number;
  orders_revenue: number;
  currency?: string;
  conversion_rate: number;
  total_clicks: number;
  valid_ksa_clicks: number;
  morocco_clicks?: number;
  vpn_clicks: number;
  foreign_clicks: number;
  unique_sessions: number;
  series: { date: string; clicks: number; orders: number }[];
  top_products: { slug: string; qty: number }[];
  orders: AdminOrder[];
}

export interface StoreCategorySetting {
  slug: string;
  name_ar: string;
  sort_order: number;
  active: boolean;
}

export function formatMad(value: number): string {
  return new Intl.NumberFormat("fr-MA").format(value);
}

export function formatRate(rate: number): string {
  if (!Number.isFinite(rate)) return "—";
  return `${(rate * 100).toFixed(1)}%`;
}

export function formatWhen(iso: string | null): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return new Intl.DateTimeFormat("ar-MA", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Africa/Casablanca",
  }).format(date);
}
