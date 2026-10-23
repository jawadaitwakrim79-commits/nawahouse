"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { formatRate, formatSar, formatWhen, type AdminOverview } from "@/lib/admin-view";

function todayRiyadh(): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Riyadh" }).format(new Date());
}

function daysAgo(days: number): string {
  const start = new Date(`${todayRiyadh()}T00:00:00+03:00`);
  start.setUTCDate(start.getUTCDate() - days);
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Riyadh" }).format(start);
}

export function AdminDashboard() {
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");
  const [from, setFrom] = useState(daysAgo(29));
  const [to, setTo] = useState(todayRiyadh());
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function load(nextFrom = from, nextTo = to) {
    setError("");
    const params = new URLSearchParams({ from: nextFrom, to: nextTo });
    const response = await fetch(`/api/admin/overview?${params.toString()}`, { cache: "no-store" });
    if (response.status === 401) {
      setOverview(null);
      setReady(true);
      return;
    }
    if (!response.ok) {
      setError("تعذر قراءة بيانات المتجر من قاعدة البيانات.");
      setReady(true);
      return;
    }
    setOverview((await response.json()) as AdminOverview);
    setReady(true);
  }

  useEffect(() => {
    load().catch(() => {
      setError("تعذر الاتصال بالخادم.");
      setReady(true);
    });
    // Initial load only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onLogin(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const response = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: token.trim() || undefined,
          username: username.trim() || undefined,
          password: password || undefined,
        }),
      });
      if (!response.ok) {
        setError(response.status === 503 ? "لوحة الإدارة غير مهيّأة على الخادم." : "بيانات الدخول غير صحيحة.");
        return;
      }
      setToken("");
      setPassword("");
      await load();
    } catch {
      setError("تعذر الاتصال بالخادم.");
    } finally {
      setSubmitting(false);
    }
  }

  async function onLogout() {
    await fetch("/api/admin/logout", { method: "POST" });
    setOverview(null);
  }

  if (!ready) {
    return <p className="px-4 py-16 text-center text-muted">جارٍ التحميل…</p>;
  }

  if (!overview) {
    return (
      <main className="mx-auto flex min-h-screen max-w-md items-center px-4 py-10">
        <form onSubmit={onLogin} className="w-full rounded-[20px] border border-line bg-white p-6">
          <p className="font-display text-xs uppercase tracking-[0.2em] text-brass">Nawa House</p>
          <h1 className="mt-2 font-serif text-3xl text-brand">لوحة الإدارة</h1>
          <p className="mt-2 text-sm text-muted">أدخلي رمز الإدارة. الرمز يبقى على الخادم ولا يُحفظ في الصفحة.</p>
          <label className="mt-6 block text-sm">
            رمز الإدارة
            <input
              type="password"
              autoComplete="current-password"
              value={token}
              onChange={(event) => setToken(event.target.value)}
              className="mt-1 w-full rounded-xl border border-line bg-paper px-3 py-3"
            />
          </label>
          <details className="mt-4 text-sm text-muted">
            <summary className="cursor-pointer">أو اسم المستخدم وكلمة المرور</summary>
            <label className="mt-3 block">
              اسم المستخدم
              <input
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                className="mt-1 w-full rounded-xl border border-line bg-paper px-3 py-3 text-ink"
              />
            </label>
            <label className="mt-3 block">
              كلمة المرور
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-1 w-full rounded-xl border border-line bg-paper px-3 py-3 text-ink"
              />
            </label>
          </details>
          {error ? <p className="mt-4 text-sm text-[#8B2E2E]">{error}</p> : null}
          <button
            type="submit"
            disabled={submitting}
            className="mt-6 w-full rounded-full bg-brand px-4 py-3 text-on-brand disabled:opacity-60"
          >
            {submitting ? "جارٍ الدخول…" : "دخول"}
          </button>
        </form>
      </main>
    );
  }

  const maxBar = Math.max(1, ...overview.series.map((point) => point.orders + point.clicks));

  return (
    <main className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
      <header className="flex flex-col gap-3 border-b border-line pb-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="font-display text-xs uppercase tracking-[0.2em] text-brass">Nawa House</p>
          <h1 className="font-serif text-3xl text-brand">لوحة الإدارة</h1>
        </div>
        <button type="button" onClick={onLogout} className="rounded-full border border-brand px-4 py-2 text-sm text-brand">
          خروج
        </button>
      </header>

      <form
        className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-end"
        onSubmit={(event) => {
          event.preventDefault();
          load().catch(() => setError("تعذر تحديث البيانات."));
        }}
      >
        <label className="text-sm text-muted">
          من
          <input type="date" value={from} onChange={(event) => setFrom(event.target.value)} className="mt-1 block w-full rounded-xl border border-line bg-white px-3 py-2 text-ink" />
        </label>
        <label className="text-sm text-muted">
          إلى
          <input type="date" value={to} onChange={(event) => setTo(event.target.value)} className="mt-1 block w-full rounded-xl border border-line bg-white px-3 py-2 text-ink" />
        </label>
        <button type="submit" className="rounded-full bg-brand px-5 py-2 text-on-brand">
          عرض
        </button>
      </form>
      {error ? <p className="mt-4 text-sm text-[#8B2E2E]">{error}</p> : null}

      <section className="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="الطلبات" value={formatSar(overview.orders_count)} />
        <Stat label="الإيراد (ر.س)" value={formatSar(overview.orders_revenue)} />
        <Stat label="معدل التحويل" value={formatRate(overview.conversion_rate)} />
        <Stat label="زيارات سعودية صالحة" value={formatSar(overview.valid_ksa_clicks)} />
      </section>

      <p className="mt-3 text-xs text-muted">
        كل الزيارات {formatSar(overview.total_clicks)} · جلسات {formatSar(overview.unique_sessions)} · VPN {formatSar(overview.vpn_clicks)} · خارج السعودية {formatSar(overview.foreign_clicks)}
      </p>

      <section className="mt-6 rounded-[20px] border border-line bg-white p-4">
        <h2 className="text-sm text-muted">الطلبات والزيارات يوميًا</h2>
        {overview.series.length === 0 ? (
          <p className="py-8 text-sm text-muted">لا توجد حركة في هذه الفترة.</p>
        ) : (
          <div className="mt-4 flex h-36 items-end gap-1 overflow-x-auto">
            {overview.series.map((point) => (
              <div key={point.date} className="flex min-w-3 flex-1 flex-col justify-end" title={`${point.date}: ${point.orders} طلبات`}>
                <div
                  className="rounded-t bg-brand"
                  style={{ height: `${Math.max(4, ((point.orders + point.clicks) / maxBar) * 120)}px` }}
                />
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="mt-6 overflow-x-auto rounded-[20px] border border-line bg-white">
        <table className="w-full min-w-[640px] text-sm">
          <thead className="bg-ivory text-muted">
            <tr>
              <th className="px-3 py-2 text-right font-medium">الطلب</th>
              <th className="px-3 py-2 text-right font-medium">العميلة</th>
              <th className="px-3 py-2 text-right font-medium">المبلغ</th>
              <th className="px-3 py-2 text-right font-medium">الحالة</th>
              <th className="px-3 py-2 text-right font-medium">التاريخ</th>
            </tr>
          </thead>
          <tbody>
            {overview.orders.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-3 py-8 text-center text-muted">
                  لا توجد طلبات في هذه الفترة.
                </td>
              </tr>
            ) : (
              overview.orders.map((order) => (
                <tr key={order.public_id} className="border-t border-line">
                  <td className="px-3 py-3">
                    <Link href={`/admin/orders/${order.public_id}`} className="text-brand">
                      {order.public_id}
                    </Link>
                  </td>
                  <td className="px-3 py-3">{order.customer_name}</td>
                  <td className="px-3 py-3">{formatSar(order.total_sar)} ر.س</td>
                  <td className="px-3 py-3">{order.status}</td>
                  <td className="px-3 py-3">{formatWhen(order.created_at)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>

      <section className="mt-6 rounded-[20px] border border-line bg-white p-4">
        <h2 className="text-sm text-muted">المنتجات</h2>
        {overview.top_products.length === 0 ? (
          <p className="mt-3 text-sm text-muted">لا توجد قطع مباعة في هذه الفترة.</p>
        ) : (
          <ul className="mt-3 space-y-2 text-sm">
            {overview.top_products.map((product) => (
              <li key={product.slug} className="flex justify-between border-b border-line py-2">
                <span>{product.slug}</span>
                <span>{formatSar(product.qty)}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[20px] border border-line bg-white p-4">
      <div className="font-serif text-2xl text-brand sm:text-3xl">{value}</div>
      <div className="mt-1 text-xs text-muted">{label}</div>
    </div>
  );
}
