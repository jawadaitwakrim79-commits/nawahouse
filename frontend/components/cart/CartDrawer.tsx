"use client";

import { useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { useCartStore } from "@/lib/cart-store";
import { PRODUCTS } from "@/content/products";
import { copy } from "@/content/copy";
import { formatMAD } from "@/lib/pricing";
import { CheckoutModal } from "@/components/checkout/CheckoutModal";

export function CartDrawer() {
  const { lines, open, closeCart, openCheckout, checkoutOpen, removeLine, setQuantity, goods } = useCartStore();

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (event.key === "Escape" && open) closeCart();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, closeCart]);

  if (!open && !checkoutOpen) return null;

  return (
    <>
      {open && !checkoutOpen && (
        <button className="fixed inset-0 bg-black/40 z-40" onClick={closeCart} aria-label="إغلاق السلة" />
      )}
      {open && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={copy.cart.title}
          className="fixed inset-y-0 start-0 z-50 w-full max-w-[420px] bg-paper flex flex-col shadow-2xl"
        >
          <div className="flex items-center justify-between p-5 border-b border-line">
            <h2 className="text-xl">{copy.cart.title}</h2>
            <button onClick={closeCart} aria-label="إغلاق" className="text-muted">
              ✕
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-5">
            {lines.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-muted mb-4">{copy.cart.emptyMsg}</p>
                <Link href="/shop" onClick={closeCart} className="text-sm underline">
                  {copy.cart.continue}
                </Link>
              </div>
            ) : (
              lines.map((line) => {
                const product = PRODUCTS[line.slug];
                if (!product) return null;
                return (
                  <div key={`${line.slug}-${line.variant}`} className="flex gap-3">
                    <div className="relative w-20 h-24 bg-sand shrink-0">
                      <Image src={product.imageSrcs[0]} alt="" fill className="object-cover" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium">{product.nameAr}</p>
                      {line.variant && <p className="text-muted text-sm">{line.variant}</p>}
                      <p className="text-sm mt-1">{formatMAD(product.price)}</p>
                      <div className="flex items-center gap-3 mt-2 text-sm">
                        <button onClick={() => setQuantity(line.slug, line.variant, line.quantity - 1)} aria-label="إنقاص">
                          −
                        </button>
                        <span>{line.quantity}</span>
                        <button onClick={() => setQuantity(line.slug, line.variant, line.quantity + 1)} aria-label="زيادة">
                          +
                        </button>
                        <button
                          onClick={() => removeLine(line.slug, line.variant)}
                          className="ms-auto text-muted text-xs"
                        >
                          حذف
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
          {lines.length > 0 && (
            <div className="p-5 border-t border-line flex flex-col gap-3">
              <div className="flex justify-between text-sm">
                <span>{copy.cart.subtotal}</span>
                <span>{formatMAD(goods())}</span>
              </div>
              <p className="text-muted text-xs">{copy.cart.shippingNote}</p>
              <button onClick={openCheckout} className="bg-ink text-paper min-h-[52px] text-sm">
                {copy.cart.checkoutCta}
              </button>
            </div>
          )}
        </div>
      )}
      {checkoutOpen && <CheckoutModal />}
    </>
  );
}
