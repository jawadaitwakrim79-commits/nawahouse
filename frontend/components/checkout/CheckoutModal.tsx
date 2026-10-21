"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useCartStore } from "@/lib/cart-store";
import { copy } from "@/content/copy";
import { PRODUCTS, getUpsellSlug, type Slug } from "@/content/products";
import { mainTotal, orderTotal } from "@/lib/pricing";
import { isValidPhone, normalizePhone } from "@/lib/phone";
import { submitOrder } from "@/lib/api";
import { trackPurchase, identifyPixels } from "@/lib/tracking";

type Step = "form" | "upsell" | "submitting";

export function CheckoutModal() {
  const router = useRouter();
  const { lines, closeCheckout, closeCart, setUpsell, clearCart } = useCartStore();
  const mainLines = lines.filter((l) => l.pricing === "main");
  const mainUnits = mainLines.reduce((s, l) => s + l.quantity, 0);
  const total = mainTotal(mainUnits);

  const [step, setStep] = useState<Step>("form");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [nameError, setNameError] = useState("");
  const [phoneError, setPhoneError] = useState("");
  const [apiError, setApiError] = useState("");
  const [countdown, setCountdown] = useState(15);
  const [upsellSlug, setUpsellSlug] = useState<Slug>("oud");
  const [eventId, setEventId] = useState<string | null>(null);
  const [inFlight, setInFlight] = useState(false);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // Identify pixels when we have a valid phone
  useEffect(() => {
    if (!isValidPhone(phone)) return;
    const p = normalizePhone(phone);
    if (!p) return;
    const eid = typeof localStorage !== "undefined"
      ? (localStorage.getItem("nawa_eid") || crypto.randomUUID())
      : crypto.randomUUID();
    identifyPixels(p, eid);
  }, [phone]);

  // Fire InitiateCheckout on mount
  useEffect(() => {
    const eid = crypto.randomUUID();
    void Promise.resolve().then(() => {
      import("@/lib/tracking").then(({ trackInitiateCheckout: fireIC }) => {
        fireIC(eid, {
          value: total,
          contentIds: mainLines.map((l) => l.slug as Slug),
          numItems: mainUnits,
        });
      });
      import("@/lib/api").then(({ sendEvent }) => {
        sendEvent({
          event_name: "InitiateCheckout",
          event_id: eid,
          value: total,
          content_ids: mainLines.map((l) => l.slug as Slug),
        });
      });
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Focus trap
  useEffect(() => { modalRef.current?.focus(); }, []);

  // Escape key
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") closeCheckout(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [closeCheckout]);

  function validateForm(): boolean {
    let ok = true;
    const n = name.trim();
    if (n.length < 2 || n.length > 60 || /^\d+$/.test(n)) {
      setNameError(copy.checkout.nameError);
      ok = false;
    } else setNameError("");

    if (!isValidPhone(phone)) {
      setPhoneError(copy.checkout.phoneError);
      ok = false;
    } else setPhoneError("");

    return ok;
  }

  function handleFormSubmit() {
    if (!validateForm()) return;
    closeCart(); // ensure drawer is closed before upsell shows
    // Generate event_id before upsell
    const eid = crypto.randomUUID();
    setEventId(eid);
    // Choose upsell product
    const slugsInCart = new Set(mainLines.map((l) => l.slug as Slug));
    const uSlug = getUpsellSlug(slugsInCart);
    setUpsellSlug(uSlug);
    setCountdown(15);
    setStep("upsell");
    startTimer(eid, false);
  }

  function startTimer(eid: string, withUpsell: boolean) {
    if (timerRef.current) clearInterval(timerRef.current);
    let t = 15;
    timerRef.current = setInterval(() => {
      t -= 1;
      setCountdown(t);
      if (t <= 0) {
        if (timerRef.current) clearInterval(timerRef.current);
        void placeOrder(eid, withUpsell);
      }
    }, 1000);
  }

  function handleYes() {
    if (!eventId) return;
    if (timerRef.current) clearInterval(timerRef.current);
    setUpsell(upsellSlug);
    void placeOrder(eventId, true);
  }

  function handleNo() {
    if (!eventId) return;
    if (timerRef.current) clearInterval(timerRef.current);
    setUpsell(null);
    void placeOrder(eventId, false);
  }

  const placeOrder = useCallback(
    async (eid: string, withUpsell: boolean) => {
      if (inFlight) return;
      setInFlight(true);
      setStep("submitting");
      setApiError("");

      const orderLines: { slug: Slug; quantity: number; pricing: "main" | "upsell" }[] = mainLines.map((l) => ({
        slug: l.slug,
        quantity: l.quantity,
        pricing: "main" as const,
      }));
      if (withUpsell) {
        orderLines.push({ slug: upsellSlug, quantity: 1, pricing: "upsell" as const });
      }

      const upsellUnits: 0 | 1 = withUpsell ? 1 : 0;
      const finalTotal = orderTotal(mainUnits, upsellUnits);

      // Read cookies
      const fbp = getCookie("_fbp");
      const fbc = getCookie("_fbc");
      const ttp = getCookie("_ttp");
      const ttclid = getStorage("nawa_ttclid");
      const sc_click_id = getStorage("nawa_sc_cid");
      const external_id = getStorage("nawa_eid");

      const p = normalizePhone(phone);

      try {
        const res = await submitOrder({
          event_id: eid,
          name: name.trim(),
          phone: phone,
          lines: orderLines,
          page_url: window.location.href,
          event_source_url: `https://nawahouse.shop/thank-you`,
          fbp: fbp || null,
          fbc: fbc || null,
          ttp: ttp || null,
          ttclid: ttclid || null,
          sc_click_id: sc_click_id || null,
          external_id: external_id || null,
        });

        // Store last order summary for thank-you page
        sessionStorage.setItem(
          "nawa_last_order",
          JSON.stringify({ orderId: res.order_id, total: res.total_sar })
        );

        // Fire Purchase pixel (once guard)
        trackPurchase(eid, res.order_id, {
          value: finalTotal,
          currency: "SAR",
          contentIds: mainLines.map((l) => l.slug as Slug),
          numItems: mainUnits + upsellUnits,
          orderId: res.order_id,
        });

        clearCart();
        router.push(`/thank-you?order=${res.order_id}`);
      } catch {
        setApiError(copy.errorOrder);
        setStep("form");
        setInFlight(false);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [inFlight, mainLines, mainUnits, name, phone, upsellSlug]
  );

  useEffect(() => () => { if (timerRef.current) clearInterval(timerRef.current); }, []);

  return (
    <div className="fixed inset-0 z-[70] flex items-end md:items-center justify-center p-0 md:p-4">
      {/* Backdrop — covers cart drawer (z-50) and its backdrop (z-40) */}
      <div className="absolute inset-0 bg-black/60" onClick={step === "form" ? closeCheckout : undefined} aria-hidden="true" />

      {/* Modal */}
      <div
        ref={modalRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-label={copy.checkout.title}
        className="relative z-10 w-full md:max-w-[480px] bg-paper rounded-t-[24px] md:rounded-[24px] max-h-[92dvh] overflow-y-auto outline-none"
      >
        {step === "form" && (
          <FormStep
            name={name} setName={setName} nameError={nameError}
            phone={phone} setPhone={setPhone} phoneError={phoneError}
            apiError={apiError} total={total} mainLines={mainLines}
            onSubmit={handleFormSubmit} onClose={closeCheckout}
          />
        )}
        {step === "upsell" && (
          <UpsellStep
            slug={upsellSlug} countdown={countdown}
            onYes={handleYes} onNo={handleNo}
          />
        )}
        {step === "submitting" && (
          <div className="p-8 text-center text-muted">
            <div className="text-3xl mb-4">⏳</div>
            <p>{copy.upsell.pendingMsg}</p>
          </div>
        )}
      </div>
    </div>
  );
}

function FormStep({
  name, setName, nameError,
  phone, setPhone, phoneError,
  apiError, total, mainLines,
  onSubmit, onClose,
}: {
  name: string; setName: (v: string) => void; nameError: string;
  phone: string; setPhone: (v: string) => void; phoneError: string;
  apiError: string; total: number;
  mainLines: { slug: Slug; quantity: number }[];
  onSubmit: () => void; onClose: () => void;
}) {
  return (
    <div className="p-6 flex flex-col gap-5">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-ink">{copy.checkout.title}</h2>
        <button onClick={onClose} className="p-1 text-muted" aria-label="إغلاق"><CloseIcon /></button>
      </div>

      {/* Summary */}
      <div className="bg-ivory rounded-[12px] p-4">
        <div className="text-sm font-bold text-ink mb-2">{copy.checkout.summaryTitle}</div>
        {mainLines.map((l) => {
          const p = PRODUCTS[l.slug];
          return (
            <div key={l.slug} className="flex justify-between text-sm text-muted py-1">
              <span>{p.nameAr} × {l.quantity}</span>
              <span></span>
            </div>
          );
        })}
        <div className="flex justify-between font-bold text-ink pt-2 border-t border-line mt-2">
          <span>{copy.checkout.summaryTitle === "ملخص الطلب" ? "المجموع" : "Total"}</span>
          <span>{total} {copy.cart.currency}</span>
        </div>
      </div>

      <p className="text-muted text-sm">{copy.checkout.socialLine}</p>

      {/* Name */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-bold text-ink">{copy.checkout.nameLabel}</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder={copy.checkout.namePlaceholder}
          maxLength={60}
          className="border border-line rounded-lg px-4 py-3 bg-paper text-ink text-base outline-none focus:border-brand"
        />
        {nameError && <span className="text-brand text-sm">{nameError}</span>}
      </div>

      {/* Phone */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-bold text-ink">{copy.checkout.phoneLabel}</label>
        <input
          type="tel"
          inputMode="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          onBlur={() => {
            if (phone && !isValidPhone(phone)) {
              // show error on blur
            }
          }}
          placeholder={copy.checkout.phonePlaceholder}
          className="border border-line rounded-lg px-4 py-3 bg-paper text-ink text-base outline-none focus:border-brand"
          dir="ltr"
        />
        {phoneError && <span className="text-brand text-sm">{phoneError}</span>}
      </div>

      {apiError && (
        <p className="text-brand text-sm bg-red-50 p-3 rounded-lg">{apiError}</p>
      )}

      <button
        onClick={onSubmit}
        className="w-full bg-brand-deep text-on-brand py-4 rounded-full font-bold text-base hover:opacity-90 transition-opacity min-h-[52px]"
      >
        {copy.checkout.submitCta}
      </button>
    </div>
  );
}

function UpsellStep({
  slug, countdown, onYes, onNo,
}: {
  slug: Slug; countdown: number; onYes: () => void; onNo: () => void;
}) {
  const product = PRODUCTS[slug];
  return (
    <div className="p-6 flex flex-col gap-5 items-center text-center">
      <div className="text-sm font-bold text-brand">{copy.upsell.title}</div>
      <div className="text-3xl font-bold text-ink">
        {countdown} <span className="text-muted text-base">{copy.upsell.timerLabel}</span>
      </div>

      <div className="bg-ivory rounded-[16px] p-5 w-full">
        <div className="text-xl font-bold text-ink mb-1">{product.nameAr}</div>
        <div className="text-muted text-sm mb-3">{product.enemyAr}</div>
        <div className="flex items-center justify-center gap-3">
          <span className="text-muted line-through text-sm">{copy.upsell.price199}</span>
          <span className="text-brand font-bold text-2xl">{copy.upsell.price99}</span>
        </div>
      </div>

      <button
        onClick={onYes}
        className="w-full bg-brand-deep text-on-brand py-4 rounded-full font-bold text-base hover:opacity-90 transition-opacity min-h-[52px]"
      >
        {copy.upsell.yesCta}
      </button>
      <button
        onClick={onNo}
        className="text-muted text-sm underline hover:text-ink"
      >
        {copy.upsell.noCta}
      </button>
    </div>
  );
}

function CloseIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const m = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return m ? decodeURIComponent(m[2]) : null;
}

function getStorage(key: string): string | null {
  try { return localStorage.getItem(key); } catch { return null; }
}
