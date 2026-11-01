"use client";

import { FormEvent, useEffect, useState } from "react";
import type { StoreCategorySetting } from "@/lib/admin-view";

export function StoreSettingsPanel() {
  const [shipping, setShipping] = useState("0");
  const [categories, setCategories] = useState<StoreCategorySetting[]>([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/admin/settings", { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) return null;
        return response.json() as Promise<{ shipping_mad: number; categories: StoreCategorySetting[] }>;
      })
      .then((data) => {
        if (!data) return;
        setShipping(String(data.shipping_mad ?? 0));
        setCategories(data.categories || []);
      })
      .catch(() => setError("تعذر قراءة إعدادات المتجر."));
  }, []);

  async function saveShipping(event: FormEvent) {
    event.preventDefault();
    setMessage("");
    setError("");
    const amount = Number(shipping);
    if (!Number.isInteger(amount) || amount < 0) {
      setError("أدخل تكلفة توصيل صحيحة بالدرهم.");
      return;
    }
    const response = await fetch("/api/admin/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shipping_mad: amount }),
    });
    if (!response.ok) {
      setError("لم تُحفظ تكلفة التوصيل.");
      return;
    }
    setMessage("حُفظت تكلفة التوصيل.");
  }

  async function saveCategories(event: FormEvent) {
    event.preventDefault();
    setMessage("");
    setError("");
    const response = await fetch("/api/admin/categories", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ categories }),
    });
    if (!response.ok) {
      setError("لم تُحفظ الفئات.");
      return;
    }
    const data = (await response.json()) as { categories: StoreCategorySetting[] };
    setCategories(data.categories);
    setMessage("حُفظت الفئات.");
  }

  return (
    <section className="mt-6 grid gap-4 lg:grid-cols-2">
      <form onSubmit={saveShipping} className="rounded-[20px] border border-line bg-white p-4">
        <h2 className="text-sm text-muted">تكلفة التوصيل</h2>
        <p className="mt-1 text-xs text-muted">بالدرهم. تظهر للعميل قبل تأكيد الطلب. لا يوجد سعر افتراضي غير الصفر حتى تحدده.</p>
        <label className="mt-3 block text-sm">
          التوصيل (DH)
          <input
            inputMode="numeric"
            value={shipping}
            onChange={(event) => setShipping(event.target.value)}
            className="mt-1 block w-full rounded-xl border border-line px-3 py-2"
          />
        </label>
        <button type="submit" className="mt-3 rounded-full bg-brand px-4 py-2 text-sm text-on-brand">
          حفظ التوصيل
        </button>
      </form>

      <form onSubmit={saveCategories} className="rounded-[20px] border border-line bg-white p-4">
        <h2 className="text-sm text-muted">الفئات</h2>
        <div className="mt-3 flex flex-col gap-2">
          {categories.map((category, index) => (
            <label key={category.slug} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={category.active}
                onChange={(event) => {
                  const next = [...categories];
                  next[index] = { ...category, active: event.target.checked };
                  setCategories(next);
                }}
              />
              <input
                value={category.name_ar}
                onChange={(event) => {
                  const next = [...categories];
                  next[index] = { ...category, name_ar: event.target.value };
                  setCategories(next);
                }}
                className="flex-1 rounded-xl border border-line px-3 py-2"
              />
            </label>
          ))}
        </div>
        <button type="submit" className="mt-3 rounded-full bg-brand px-4 py-2 text-sm text-on-brand">
          حفظ الفئات
        </button>
      </form>
      {message ? <p className="text-sm text-brand lg:col-span-2">{message}</p> : null}
      {error ? <p className="text-sm text-[#8B2E2E] lg:col-span-2">{error}</p> : null}
    </section>
  );
}
