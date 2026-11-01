import type { Metadata } from "next";
import Link from "next/link";
import { ProductCard } from "@/components/product/ProductCard";
import { copy } from "@/content/copy";
import { adminApiBase } from "@/lib/admin-proxy";
import { CATEGORIES, PRODUCTS_ARRAY, type CategorySlug } from "@/content/products";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "المتجر",
  description: "ساعات رجالية ونسائية، نظارات شمسية، وإطارات طبية من نوا هاوس.",
};

const KNOWN = new Set(CATEGORIES.map((category) => category.slug));

export default async function ShopPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string }>;
}) {
  const { category } = await searchParams;
  const remote = await loadCategories();
  const visible = new Set(
    (remote ?? CATEGORIES.map((item) => ({ slug: item.slug, name_ar: item.nameAr, active: true })))
      .filter((item) => item.active)
      .map((item) => item.slug)
  );
  const labels = new Map((remote ?? []).map((item) => [item.slug, item.name_ar]));
  const active = category && KNOWN.has(category as CategorySlug) && visible.has(category) ? (category as CategorySlug) : null;
  const products = (active ? PRODUCTS_ARRAY.filter((product) => product.category === active) : PRODUCTS_ARRAY).filter(
    (product) => visible.has(product.category)
  );

  return (
    <div className="max-w-[1180px] mx-auto px-5 py-12">
      <h1 className="mb-3">{copy.shop.title}</h1>
      <p className="text-muted mb-8">{copy.shop.sub}</p>
      <div className="flex gap-2 overflow-x-auto pb-4 mb-8">
        <Chip href="/shop" active={!active} label={copy.shop.all} />
        {CATEGORIES.filter((item) => visible.has(item.slug)).map((item) => (
          <Chip key={item.slug} href={item.href} active={active === item.slug} label={labels.get(item.slug) || item.nameAr} />
        ))}
      </div>
      {products.length === 0 ? (
        <p className="text-muted">{copy.shop.empty}</p>
      ) : (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-10">
          {products.map((product) => (
            <ProductCard key={product.slug} slug={product.slug} />
          ))}
        </div>
      )}
    </div>
  );
}

async function loadCategories(): Promise<{ slug: string; name_ar: string; active: boolean }[] | null> {
  try {
    const response = await fetch(`${adminApiBase()}/api/store`, { cache: "no-store" });
    if (!response.ok) return null;
    const data = (await response.json()) as { categories?: { slug: string; name_ar: string; active: boolean }[] };
    return data.categories ?? null;
  } catch {
    return null;
  }
}

function Chip({ href, label, active }: { href: string; label: string; active: boolean }) {
  return (
    <Link
      href={href}
      className={`shrink-0 px-4 py-2 text-sm border ${
        active ? "bg-ink text-paper border-ink" : "border-line text-ink"
      }`}
    >
      {label}
    </Link>
  );
}
