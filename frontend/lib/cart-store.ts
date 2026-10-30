"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { isSlug, type Slug } from "@/content/products";
import { goodsTotal } from "@/lib/pricing";

export interface CartLine {
  slug: Slug;
  quantity: number;
  pricing: "main";
  variant: string | null;
}

interface CartState {
  lines: CartLine[];
  open: boolean;
  checkoutOpen: boolean;
  count: () => number;
  goods: () => number;
  addMain: (slug: Slug, quantity?: number, variant?: string | null) => void;
  removeLine: (slug: Slug, variant: string | null) => void;
  setQuantity: (slug: Slug, variant: string | null, quantity: number) => void;
  clearCart: () => void;
  openCart: () => void;
  closeCart: () => void;
  openCheckout: () => void;
  closeCheckout: () => void;
}

function sameLine(line: CartLine, slug: Slug, variant: string | null) {
  return line.slug === slug && (line.variant || null) === (variant || null);
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      lines: [],
      open: false,
      checkoutOpen: false,

      count: () => get().lines.reduce((sum, line) => sum + line.quantity, 0),
      goods: () => goodsTotal(get().lines),

      addMain: (slug, quantity = 1, variant = null) =>
        set((state) => {
          const existing = state.lines.find((line) => sameLine(line, slug, variant));
          if (existing) {
            return {
              lines: state.lines.map((line) =>
                sameLine(line, slug, variant)
                  ? { ...line, quantity: Math.min(6, line.quantity + quantity) }
                  : line
              ),
              open: true,
            };
          }
          return {
            lines: [...state.lines, { slug, quantity, pricing: "main", variant }],
            open: true,
          };
        }),

      removeLine: (slug, variant) =>
        set((state) => ({
          lines: state.lines.filter((line) => !sameLine(line, slug, variant)),
        })),

      setQuantity: (slug, variant, quantity) =>
        set((state) => ({
          lines:
            quantity <= 0
              ? state.lines.filter((line) => !sameLine(line, slug, variant))
              : state.lines.map((line) =>
                  sameLine(line, slug, variant) ? { ...line, quantity: Math.min(6, quantity) } : line
                ),
        })),

      clearCart: () => set({ lines: [], open: false, checkoutOpen: false }),
      openCart: () => set({ open: true }),
      closeCart: () => set({ open: false }),
      openCheckout: () => set({ checkoutOpen: true, open: false }),
      closeCheckout: () => set({ checkoutOpen: false }),
    }),
    {
      name: "nawa-cart",
      version: 2,
      migrate: () => ({ lines: [] }),
      partialize: (state) => ({
        lines: state.lines.filter((line) => isSlug(line.slug)),
      }),
    }
  )
);
