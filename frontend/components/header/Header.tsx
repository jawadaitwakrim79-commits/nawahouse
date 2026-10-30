"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Logo } from "@/components/Logo";
import { copy } from "@/content/copy";
import { useCartStore } from "@/lib/cart-store";
import { AnnouncementBar } from "./AnnouncementBar";

const NAV_LINKS = [
  { label: copy.nav.shop, href: "/shop" },
  { label: copy.nav.menWatches, href: "/shop?category=mens-watches" },
  { label: copy.nav.womenWatches, href: "/shop?category=womens-watches" },
  { label: copy.nav.sunglasses, href: "/shop?category=sunglasses" },
  { label: copy.nav.optical, href: "/shop?category=optical" },
  { label: copy.nav.about, href: "/about" },
];

export function Header({ hideTicker = false }: { hideTicker?: boolean }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const openCart = useCartStore((s) => s.openCart);
  const cartCount = useCartStore((s) => s.count)();

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <>
      {!hideTicker && <AnnouncementBar />}
      <header
        className={`sticky top-0 z-40 transition-colors duration-200 ${
          scrolled ? "bg-paper/95 backdrop-blur border-b border-line" : "bg-paper"
        }`}
      >
        <div className="max-w-[1180px] mx-auto h-16 px-5 flex items-center justify-between gap-4">
          <button onClick={openCart} className="md:hidden relative p-2 text-ink" aria-label="السلة">
            <CartIcon />
            {cartCount > 0 && <CartBadge count={cartCount} />}
          </button>

          <div className="absolute inset-x-0 flex justify-center pointer-events-none md:static md:justify-start md:pointer-events-auto">
            <span className="pointer-events-auto">
              <Logo size="sm" />
            </span>
          </div>

          <nav className="hidden lg:flex items-center gap-5 text-sm text-ink">
            {NAV_LINKS.map((link) => (
              <Link key={link.href} href={link.href} className="hover:text-brass transition-colors">
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-1">
            <button onClick={openCart} className="hidden md:flex relative p-2 text-ink" aria-label="السلة">
              <CartIcon />
              {cartCount > 0 && <CartBadge count={cartCount} />}
            </button>
            <button onClick={() => setMenuOpen(true)} className="lg:hidden p-2 text-ink" aria-label="القائمة">
              <MenuIcon />
            </button>
          </div>
        </div>

        {menuOpen && (
          <div className="fixed inset-0 z-50 bg-paper flex flex-col" role="dialog" aria-modal="true">
            <div className="flex justify-between items-center p-5 border-b border-line">
              <Logo size="sm" />
              <button onClick={() => setMenuOpen(false)} aria-label="إغلاق">
                <CloseIcon />
              </button>
            </div>
            <nav className="flex flex-col p-5">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMenuOpen(false)}
                  className="py-3 text-lg border-b border-line"
                >
                  {link.label}
                </Link>
              ))}
              <Link href="/contact" onClick={() => setMenuOpen(false)} className="py-3 text-lg">
                {copy.nav.contact}
              </Link>
            </nav>
          </div>
        )}
      </header>
    </>
  );
}

function CartIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 6h15l-1.5 9h-12z" />
      <path d="M6 6 5 3H2" />
      <circle cx="9" cy="20" r="1" />
      <circle cx="18" cy="20" r="1" />
    </svg>
  );
}

function CartBadge({ count }: { count: number }) {
  return (
    <span className="absolute -top-0.5 -end-0.5 bg-ink text-paper text-[10px] rounded-full min-w-5 h-5 px-1 flex items-center justify-center">
      {count}
    </span>
  );
}

function MenuIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
      <line x1="3" y1="7" x2="21" y2="7" />
      <line x1="3" y1="12" x2="21" y2="12" />
      <line x1="3" y1="17" x2="21" y2="17" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}
