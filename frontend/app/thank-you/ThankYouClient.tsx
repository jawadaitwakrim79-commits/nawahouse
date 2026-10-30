"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { copy } from "@/content/copy";
import { useCartStore } from "@/lib/cart-store";
import { formatMAD } from "@/lib/pricing";

function ThankYouContent() {
  const params = useSearchParams();
  const orderId = params.get("order");
  const [summary, setSummary] = useState<{ orderId: string; total: number } | null>(null);
  const clearCart = useCartStore((s) => s.clearCart);
  const closeCart = useCartStore((s) => s.closeCart);
  const closeCheckout = useCartStore((s) => s.closeCheckout);

  useEffect(() => {
    closeCart();
    closeCheckout();
    const raw = sessionStorage.getItem("nawa_last_order");
    if (raw) clearCart();
  }, [clearCart, closeCart, closeCheckout]);

  useEffect(() => {
    if (!orderId) return;
    try {
      const raw = sessionStorage.getItem("nawa_last_order");
      if (!raw) return;
      const parsed = JSON.parse(raw) as { orderId: string; total: number };
      if (parsed.orderId === orderId) setSummary(parsed);
    } catch {
      /* ignore */
    }
  }, [orderId]);

  if (!orderId) {
    return (
      <div className="max-w-[640px] mx-auto px-5 py-20 text-center">
        <p className="text-muted">{copy.thankYou.notFoundMsg}</p>
        <Link href="/" className="mt-6 inline-flex underline">
          الرئيسية
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-[680px] mx-auto px-5 py-20 text-center">
      <p className="text-brass text-xs tracking-[0.18em] uppercase mb-4">Nawa House</p>
      <h1>{copy.thankYou.title}</h1>
      <p className="text-muted mt-4">
        {copy.thankYou.orderLabel}: <span dir="ltr">{orderId}</span>
      </p>
      {summary && (
        <p className="mt-2">
          {copy.thankYou.totalLabel}: {formatMAD(summary.total)} — {copy.thankYou.cod}
        </p>
      )}
      <div className="bg-ink text-paper p-8 mt-10 text-start">
        <p className="text-lg leading-relaxed">{copy.thankYou.callBlock}</p>
        <p className="text-paper/70 text-sm mt-3">{copy.thankYou.hours}</p>
      </div>
      <Link href="/shop" className="inline-flex mt-10 border border-ink px-6 py-3 text-sm">
        {copy.thankYou.back}
      </Link>
    </div>
  );
}

export default function ThankYouClient() {
  return (
    <Suspense fallback={<div className="py-20 text-center text-muted">جارٍ التحميل…</div>}>
      <ThankYouContent />
    </Suspense>
  );
}
