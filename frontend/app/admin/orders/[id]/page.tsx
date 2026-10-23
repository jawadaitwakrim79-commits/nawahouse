"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { formatSar, formatWhen, type AdminOrder } from "@/lib/admin-view";

export default function AdminOrderPage() {
  const params = useParams<{ id: string }>();
  const [order, setOrder] = useState<AdminOrder | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const id = params.id;
    if (!id) return;
    fetch(`/api/admin/orders/${encodeURIComponent(id)}`, { cache: "no-store" })
      .then(async (response) => {
        if (response.status === 401) {
          window.location.href = "/admin";
          return null;
        }
        if (!response.ok) throw new Error("missing");
        return response.json() as Promise<{ order: AdminOrder }>;
      })
      .then((data) => {
        if (data) setOrder(data.order);
      })
      .catch(() => setError("تعذر قراءة هذا الطلب."));
  }, [params.id]);

  if (error) {
    return <p className="px-4 py-16 text-center text-[#8B2E2E]">{error}</p>;
  }
  if (!order) {
    return <p className="px-4 py-16 text-center text-muted">جارٍ التحميل…</p>;
  }

  const whatsapp = order.phone_e164.replace(/^\+/, "");

  return (
    <main className="mx-auto max-w-5xl px-4 py-6 sm:px-6">
      <Link href="/admin" className="text-sm text-muted">
        رجوع إلى اللوحة
      </Link>
      <h1 className="mt-3 font-serif text-3xl text-brand">{order.public_id}</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <section className="rounded-[20px] border border-line bg-white p-4">
          <h2 className="text-sm text-muted">العميلة</h2>
          <p className="mt-2 text-lg">{order.customer_name}</p>
          <p className="mt-1 font-display" dir="ltr">{order.phone_e164}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            <a className="rounded-full bg-brand px-4 py-2 text-sm text-on-brand" href={`tel:${order.phone_e164}`}>
              اتصال
            </a>
            <a className="rounded-full border border-brand px-4 py-2 text-sm text-brand" href={`https://wa.me/${whatsapp}`}>
              واتساب
            </a>
          </div>
        </section>
        <section className="rounded-[20px] border border-line bg-white p-4">
          <h2 className="text-sm text-muted">المجموع</h2>
          <p className="mt-2 font-serif text-3xl text-brass">{formatSar(order.total_sar)} <span className="text-base text-muted">ر.س</span></p>
          <p className="mt-2 text-sm">القطع الأساسية: {order.main_units}</p>
          <p className="text-sm">الإضافة: {order.upsell_slug || "—"}</p>
          <p className="text-sm">الدفع: عند الاستلام</p>
        </section>
        <section className="rounded-[20px] border border-line bg-white p-4">
          <h2 className="text-sm text-muted">الحالة</h2>
          <p className="mt-2">{order.status}</p>
          <p className="text-sm text-muted">الجدول: {order.sheet_status}</p>
          <p className="mt-2 text-sm">{formatWhen(order.created_at)}</p>
        </section>
      </div>
      <section className="mt-4 overflow-x-auto rounded-[20px] border border-line bg-white">
        <table className="w-full min-w-[480px] text-sm">
          <thead className="bg-ivory text-muted">
            <tr>
              <th className="px-3 py-2 text-right font-medium">القطعة</th>
              <th className="px-3 py-2 text-right font-medium">الكمية</th>
              <th className="px-3 py-2 text-right font-medium">التسعير</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item, index) => (
              <tr key={`${item.slug}-${index}`} className="border-t border-line">
                <td className="px-3 py-3">{item.slug}</td>
                <td className="px-3 py-3">{item.quantity}</td>
                <td className="px-3 py-3">{item.pricing}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
