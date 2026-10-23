"use client";

import { Suspense } from "react";
import { usePathname } from "next/navigation";
import { Header } from "@/components/header/Header";
import { Footer } from "@/components/footer/Footer";
import { CartDrawer } from "@/components/cart/CartDrawer";
import { PixelLoader } from "@/components/pixels/PixelLoader";
import { ClickTracker } from "@/components/ClickTracker";

export function SiteShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "";
  if (pathname.startsWith("/admin")) {
    return <>{children}</>;
  }
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
      <CartDrawer />
      <PixelLoader />
      <Suspense fallback={null}>
        <ClickTracker />
      </Suspense>
    </>
  );
}
