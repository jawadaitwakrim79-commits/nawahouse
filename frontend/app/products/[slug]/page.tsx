import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PRODUCTS, PRODUCTS_ARRAY, isSlug } from "@/content/products";
import { copy } from "@/content/copy";
import { PDPHero } from "@/components/product/PDPHero";
import { ProductCard } from "@/components/product/ProductCard";

export function generateStaticParams() {
  return PRODUCTS_ARRAY.map((product) => ({ slug: product.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  if (!isSlug(slug)) return {};
  const product = PRODUCTS[slug];
  return { title: product.fullNameAr, description: product.oneLine };
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  if (!isSlug(slug)) notFound();
  const product = PRODUCTS[slug];

  return (
    <>
      <PDPHero slug={product.slug} />
      <section className="max-w-[1180px] mx-auto px-5 py-16">
        <h2 className="mb-8">{copy.pdp.relatedTitle}</h2>
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-10">
          {product.related.map((related) => (
            <ProductCard key={related} slug={related} />
          ))}
        </div>
      </section>
    </>
  );
}
