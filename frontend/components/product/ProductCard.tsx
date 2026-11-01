"use client";

import Image from "next/image";
import Link from "next/link";
import { PRODUCTS, categoryName, type Slug } from "@/content/products";
import { formatMAD } from "@/lib/pricing";

export function ProductCard({ slug }: { slug: Slug }) {
  const product = PRODUCTS[slug];
  return (
    <article className="lift group flex flex-col">
      <Link href={`/products/${slug}`} className="block">
        <div className="relative bg-sand overflow-hidden" style={{ aspectRatio: "4/5" }}>
          <Image
            src={product.imageSrcs[0]}
            alt={product.fullNameAr}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
            sizes="(max-width: 768px) 100vw, 320px"
          />
          {product.badge && (
            <span className="absolute top-3 start-3 bg-paper/90 text-ink text-[11px] tracking-wide px-2 py-1">
              {product.badge === "bestseller" ? "الأكثر طلباً" : "وصل حديثاً"}
            </span>
          )}
        </div>
        <div className="pt-4 flex flex-col gap-1">
          <p className="text-muted text-xs tracking-wide">{categoryName(product.category)}</p>
          <h3 className="text-ink text-lg">{product.nameAr}</h3>
          <p className="text-ink text-sm">{formatMAD(product.price)}</p>
        </div>
      </Link>
    </article>
  );
}
