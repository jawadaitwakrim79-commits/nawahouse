"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useCartStore } from "@/lib/cart-store";
import { PRODUCTS, categoryName, type Slug } from "@/content/products";
import { copy } from "@/content/copy";
import { formatMAD } from "@/lib/pricing";
import { trackAddToCart, trackViewContent } from "@/lib/tracking";
import { sendEvent } from "@/lib/api";

export function PDPHero({ slug }: { slug: Slug }) {
  const product = PRODUCTS[slug];
  const [activeImg, setActiveImg] = useState(0);
  const [colorId, setColorId] = useState(product.colors[0]?.id ?? "");
  const [qty, setQty] = useState(1);
  const addMain = useCartStore((s) => s.addMain);
  const openCheckout = useCartStore((s) => s.openCheckout);
  const color = product.colors.find((item) => item.id === colorId) ?? product.colors[0];

  useEffect(() => {
    const eid = crypto.randomUUID();
    trackViewContent(eid, { value: product.price, contentIds: [slug], numItems: 1, currency: "MAD" });
    void sendEvent({
      event_name: "ViewContent",
      event_id: eid,
      value: product.price,
      currency: "MAD",
      content_ids: [slug],
    });
  }, [product.price, slug]);

  function trackAdd(units: number) {
    const eid = crypto.randomUUID();
    trackAddToCart(eid, {
      value: product.price * units,
      currency: "MAD",
      contentIds: [slug],
      numItems: units,
    });
    void sendEvent({
      event_name: "AddToCart",
      event_id: eid,
      value: product.price * units,
      currency: "MAD",
      content_ids: [slug],
    });
  }

  function add(openBuy: boolean) {
    addMain(slug, qty, color?.label ?? null);
    trackAdd(qty);
    if (openBuy) openCheckout();
  }

  const specRows = specEntries(product.specs);

  return (
    <div className="max-w-[1180px] mx-auto px-5 py-10 grid lg:grid-cols-2 gap-10">
      <div>
        <div className="relative bg-sand overflow-hidden" style={{ aspectRatio: "4/5" }}>
          <Image
            src={product.imageSrcs[activeImg]}
            alt={product.fullNameAr}
            fill
            priority
            className="object-cover"
            sizes="(max-width: 1024px) 100vw, 560px"
          />
        </div>
        {product.imageSrcs.length > 1 && (
          <div className="flex gap-2 mt-3">
            {product.imageSrcs.map((src, index) => (
              <button
                key={src}
                onClick={() => setActiveImg(index)}
                className={`relative w-16 h-20 overflow-hidden border ${index === activeImg ? "border-ink" : "border-transparent"}`}
              >
                <Image src={src} alt="" fill className="object-cover" />
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="flex flex-col gap-6 lg:py-4">
        <div>
          <p className="text-muted text-xs tracking-[0.16em] uppercase mb-2">{categoryName(product.category)}</p>
          <h1>{product.nameAr}</h1>
          <p className="text-muted mt-3 leading-relaxed">{product.description}</p>
        </div>
        <p className="text-2xl">{formatMAD(product.price)}</p>

        {product.colors.length > 0 && (
          <div>
            <p className="text-sm mb-2">
              {copy.pdp.colorLabel}
              {color ? <span className="text-muted"> — {color.label}</span> : null}
            </p>
            <div className="flex gap-2">
              {product.colors.map((item) => (
                <button
                  key={item.id}
                  aria-label={item.label}
                  onClick={() => setColorId(item.id)}
                  className={`w-8 h-8 rounded-full border ${item.id === colorId ? "border-ink" : "border-line"}`}
                  style={{ background: item.swatch }}
                />
              ))}
            </div>
          </div>
        )}

        <div>
          <p className="text-sm mb-2">{copy.pdp.qtyLabel}</p>
          <div className="inline-flex border border-line">
            <button className="w-11 h-11" onClick={() => setQty((value) => Math.max(1, value - 1))} aria-label="إنقاص">
              −
            </button>
            <span className="w-10 h-11 flex items-center justify-center text-sm">{qty}</span>
            <button className="w-11 h-11" onClick={() => setQty((value) => Math.min(6, value + 1))} aria-label="زيادة">
              +
            </button>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <button onClick={() => add(false)} className="flex-1 bg-ink text-paper min-h-[52px] text-sm">
            {copy.pdp.addCta}
          </button>
          <button onClick={() => add(true)} className="flex-1 border border-ink min-h-[52px] text-sm">
            {copy.pdp.buyNow}
          </button>
        </div>

        <div className="border-t border-line pt-5">
          <h2 className="text-lg mb-3">{copy.pdp.specsTitle}</h2>
          <dl className="grid grid-cols-1 gap-2 text-sm">
            {specRows.map((row) => (
              <div key={row.label} className="flex justify-between gap-4 border-b border-line/70 py-2">
                <dt className="text-muted">{row.label}</dt>
                <dd>{row.value}</dd>
              </div>
            ))}
          </dl>
        </div>

        <div className="bg-ivory p-5 text-sm leading-relaxed">
          <p className="font-medium mb-1">{copy.pdp.deliveryTitle}</p>
          <p className="text-muted">{copy.pdp.deliveryBody}</p>
        </div>
      </div>
    </div>
  );
}

function specEntries(specs: (typeof PRODUCTS)[Slug]["specs"]): { label: string; value: string }[] {
  const labels = copy.pdp.specLabels;
  if (specs.kind === "watch") {
    return [
      { label: labels.caseMaterial, value: specs.caseMaterial },
      { label: labels.strapMaterial, value: specs.strapMaterial },
      { label: labels.movement, value: specs.movement },
      { label: labels.color, value: specs.color },
      { label: labels.style, value: specs.style },
    ];
  }
  return [
    { label: labels.frameShape, value: specs.frameShape },
    { label: labels.frameMaterial, value: specs.frameMaterial },
    { label: labels.frameColor, value: specs.frameColor },
    { label: labels.lens, value: specs.lens },
    { label: labels.sizes, value: specs.sizes },
  ];
}
