"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useCartStore } from "@/lib/cart-store";
import { PRODUCTS } from "@/content/products";
import { copy } from "@/content/copy";
import { formatMAD, goodsTotal, orderTotal } from "@/lib/pricing";
import { isValidPhone, normalizePhone } from "@/lib/phone";
import { fetchStoreConfig, OrderApiError, submitOrder } from "@/lib/api";
import { trackInitiateCheckout, trackPurchase } from "@/lib/tracking";

function getCookie(name: string): string {
  if (typeof document === "undefined") return "";
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : "";
}

export function CheckoutModal() {
  const router = useRouter();
  const lines = useCartStore((s) => s.lines);
  const closeCheckout = useCartStore((s) => s.closeCheckout);
  const clearCart = useCartStore((s) => s.clearCart);

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [city, setCity] = useState("");
  const [address, setAddress] = useState("");
  const [notes, setNotes] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [apiError, setApiError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [shipping, setShipping] = useState<number | null>(null);
  const [shippingError, setShippingError] = useState(false);

  const goods = goodsTotal(lines);
  const total = shipping === null ? null : orderTotal(goods, shipping);

  const loadShipping = useCallback(() => {
    setShippingError(false);
    fetchStoreConfig()
      .then((config) => setShipping(config.shipping_mad))
      .catch(() => {
        setShipping(null);
        setShippingError(true);
      });
  }, []);

  useEffect(() => {
    loadShipping();
    const eid = crypto.randomUUID();
    trackInitiateCheckout(eid, {
      value: goods,
      currency: "MAD",
      contentIds: lines.map((line) => line.slug),
      numItems: lines.reduce((sum, line) => sum + line.quantity, 0),
    });
  }, [goods, lines, loadShipping]);

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    const next: Record<string, string> = {};
    if (name.trim().length < 2) next.name = copy.checkout.nameError;
    if (!isValidPhone(phone)) next.phone = copy.checkout.phoneError;
    if (city.trim().length < 2) next.city = copy.checkout.cityError;
    if (address.trim().length < 4) next.address = copy.checkout.addressError;
    setErrors(next);
    if (Object.keys(next).length || shipping === null || submitting || lines.length === 0) return;

    setSubmitting(true);
    setApiError("");
    const eid = crypto.randomUUID();
    const normalized = normalizePhone(phone);
    try {
      const res = await submitOrder({
        event_id: eid,
        name: name.trim(),
        phone: normalized?.e164 || phone,
        city: city.trim(),
        address: address.trim(),
        delivery_notes: notes.trim() || null,
        lines: lines.map((line) => ({
          slug: line.slug,
          quantity: line.quantity,
          pricing: "main" as const,
          variant: line.variant,
        })),
        page_url: window.location.href,
        event_source_url: "https://nawahouse.shop/thank-you",
        fbp: getCookie("_fbp") || null,
        fbc: getCookie("_fbc") || null,
        ttp: getCookie("_ttp") || null,
        ttclid: window.localStorage.getItem("nawa_ttclid"),
        sc_click_id: window.localStorage.getItem("nawa_sc_cid"),
        external_id: window.localStorage.getItem("nawa_eid"),
      });
      sessionStorage.setItem(
        "nawa_last_order",
        JSON.stringify({ orderId: res.order_id, total: res.total_mad })
      );
      trackPurchase(eid, res.order_id, {
        value: res.total_mad,
        currency: "MAD",
        contentIds: lines.map((line) => line.slug),
        numItems: lines.reduce((sum, line) => sum + line.quantity, 0),
        orderId: res.order_id,
      });
      clearCart();
      router.push(`/thank-you?order=${res.order_id}`);
    } catch (err) {
      setApiError(err instanceof OrderApiError && err.message ? err.message : copy.errorOrder);
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-[70] flex items-end md:items-center justify-center">
      <button className="absolute inset-0 bg-black/50" aria-label="إغلاق" onClick={closeCheckout} />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={copy.checkout.title}
        className="relative z-10 w-full md:max-w-[520px] bg-paper max-h-[92dvh] overflow-y-auto"
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-line">
          <h2 className="text-xl">{copy.checkout.title}</h2>
          <button onClick={closeCheckout} aria-label="إغلاق" className="text-muted">
            ✕
          </button>
        </div>
        <form onSubmit={onSubmit} className="px-5 py-5 flex flex-col gap-4">
          <Field label={copy.checkout.nameLabel} error={errors.name}>
            <input value={name} onChange={(e) => setName(e.target.value)} autoComplete="name" className={inputClass} />
          </Field>
          <Field label={copy.checkout.phoneLabel} error={errors.phone}>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              inputMode="tel"
              autoComplete="tel"
              placeholder={copy.checkout.phonePlaceholder}
              dir="ltr"
              className={`${inputClass} text-left`}
            />
          </Field>
          <Field label={copy.checkout.cityLabel} error={errors.city}>
            <input
              value={city}
              onChange={(e) => setCity(e.target.value)}
              list="ma-cities"
              placeholder={copy.checkout.cityPlaceholder}
              autoComplete="address-level2"
              className={inputClass}
            />
            <datalist id="ma-cities">
              {copy.cities.map((item) => (
                <option key={item} value={item} />
              ))}
            </datalist>
          </Field>
          <Field label={copy.checkout.addressLabel} error={errors.address}>
            <textarea
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder={copy.checkout.addressPlaceholder}
              rows={2}
              className={inputClass}
            />
          </Field>
          <Field label={copy.checkout.notesLabel}>
            <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} className={inputClass} />
          </Field>

          <div className="border border-line p-4 text-sm flex flex-col gap-2">
            {lines.map((line) => {
              const product = PRODUCTS[line.slug];
              return (
                <div key={`${line.slug}-${line.variant}`} className="flex justify-between gap-3">
                  <span>
                    {product.nameAr} × {line.quantity}
                    {line.variant ? <span className="text-muted"> · {line.variant}</span> : null}
                  </span>
                  <span>{formatMAD(product.price * line.quantity)}</span>
                </div>
              );
            })}
            <div className="flex justify-between text-muted">
              <span>{copy.checkout.shippingLabel}</span>
              <span>
                {shippingError
                  ? copy.checkout.shippingError
                  : shipping === null
                    ? copy.checkout.shippingLoading
                    : formatMAD(shipping)}
              </span>
            </div>
            <div className="flex justify-between font-medium pt-2 border-t border-line">
              <span>{copy.checkout.totalLabel}</span>
              <span>{total === null ? "—" : formatMAD(total)}</span>
            </div>
            <p className="text-muted">{copy.checkout.cod}</p>
          </div>

          {shippingError && (
            <button type="button" onClick={loadShipping} className="text-sm underline text-start">
              إعادة تحميل التوصيل
            </button>
          )}
          {apiError && <p className="text-sm text-[#8B2E2E]">{apiError}</p>}
          <button
            type="submit"
            disabled={submitting || shipping === null}
            className="bg-ink text-paper min-h-[52px] text-sm disabled:opacity-50"
          >
            {submitting ? copy.checkout.submitting : copy.checkout.submitCta}
          </button>
        </form>
      </div>
    </div>
  );
}

const inputClass =
  "w-full border border-line bg-paper px-3 py-3 text-base text-ink outline-none focus:border-ink";

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      <span>{label}</span>
      {children}
      {error && <span className="text-[#8B2E2E] text-xs">{error}</span>}
    </label>
  );
}
