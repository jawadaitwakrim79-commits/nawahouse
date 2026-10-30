/**
 * Display prices. The server recalculates the order from the catalog.
 */

import { PRODUCTS, type Slug } from "@/content/products";

export function productPrice(slug: Slug): number {
  return PRODUCTS[slug]?.price ?? 0;
}

export function goodsTotal(lines: { slug: Slug; quantity: number }[]): number {
  return lines.reduce((sum, line) => sum + productPrice(line.slug) * line.quantity, 0);
}

export function orderTotal(goods: number, shippingMad: number): number {
  return goods + Math.max(0, shippingMad);
}

/** Western digits and DH, the mark used across the store. */
export function formatMAD(amount: number): string {
  const formatted = new Intl.NumberFormat("fr-MA", { maximumFractionDigits: 0 }).format(amount);
  return `${formatted} DH`;
}
