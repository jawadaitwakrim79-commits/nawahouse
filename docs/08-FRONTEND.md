# Frontend

## Stack

Use these. Do not swap in a different framework.

| Piece | Choice |
|---|---|
| Framework | Next.js 15, App Router, React 19, TypeScript |
| Styling | Tailwind CSS v4 |
| Fonts | `next/font/google`: Amiri, IBM Plex Sans Arabic, Outfit |
| Cart state | Zustand, persisted to `localStorage` key `nawa-cart` |
| Validation | Zod |
| Phone | `libphonenumber-js` |
| Data | `fetch` to the API. No React Query in the MVP. |
| Images | `next/image` for the local samples |

Do not add a component library. Buttons, drawer, and modal are local components so the brand stays exact.

## Folder

```
frontend/
  app/
    layout.tsx
    page.tsx
    shop/page.tsx
    products/[slug]/page.tsx
    about/page.tsx
    contact/page.tsx
    thank-you/page.tsx
    policies/shipping/page.tsx
    policies/returns/page.tsx
    policies/privacy/page.tsx
    policies/terms/page.tsx
    globals.css
  components/
    header/
    footer/
    cart/
    checkout/
    product/
    pixels/
    logo.tsx
  content/
    products.ts
    copy.ts
  lib/
    pricing.ts
    phone.ts
    tracking.ts
    api.ts
  public/images/...
  Dockerfile
  .env.example
  package.json
```

`content/products.ts` is the display copy. Prices and stock of truth still come from the pricing function, and the backend rechecks on submit. Slugs are `oud`, `shafaq`, `safa` only.

## Coding rules

- `"use client"` only on components that need state, the cart, the modal, or pixels. Pages stay server components that render client islands.
- All user-facing strings live in `content/copy.ts` or the page docs. No string literals scattered in layout math.
- RTL is set once on `<html lang="ar" dir="rtl">`. Do not set `dir` on random divs.
- The pricing function in `lib/pricing.ts` is a line-for-line port of the Python function in [04-CRO-OFFERS-CHECKOUT.md](04-CRO-OFFERS-CHECKOUT.md). Unit test it with the examples in that file.
- Phone helper returns `{ e164, metaDigits, tiktokE164 }` or an error. `metaDigits` is `9665XXXXXXXX` with no plus. `tiktokE164` is `+9665XXXXXXXX`.
- No `any`. No default exports except pages. Named components.
- Tailwind only, no CSS-in-JS. Tokens from [06-DESIGN-SYSTEM.md](06-DESIGN-SYSTEM.md) are CSS variables in `globals.css` and referenced as colors in `@theme`.
- Do not fetch the sheet from the browser.
- Do not hash phone numbers in the frontend.

## Cart store

```ts
type Line = {
  slug: "oud" | "shafaq" | "safa"
  quantity: number
  pricing: "main" | "upsell"
}

type Cart = {
  lines: Line[]
  open: boolean
  checkoutOpen: boolean
  upsellOpen: boolean
}
```

Main lines merge by slug. There is at most one upsell line, and only after the form is valid, and it is cleared if she presses No or the timer ends before submit. After a successful order, clear the cart.

`mainUnits` is the sum of quantities where `pricing === "main"`.

## Checkout island

One client component owns: form state, validation, the 15 second timer, the in-flight lock, and the call to `POST /api/orders`. Generate `event_id` with `crypto.randomUUID()` when she presses the form CTA, before the upsell, and reuse it for the order and the pixel. If she retries after an error, reuse the same `event_id` so the server stays idempotent.

On 201:

1. `sessionStorage.setItem("nawa_purchase_fired_" + orderId, "1")`
2. Fire the browser purchase pixels if that key was not already set.
3. `router.push("/thank-you?order=" + orderId)`
4. Clear the cart.

Thank-you reads the order id from the query and from `sessionStorage` key `nawa_last_order` (set just before navigation, value is the JSON summary). It does not call the API for another person's order. It does not fire Purchase.

## Pixels

`components/pixels/PixelLoader.tsx` is a client component mounted once in the root layout.

- Load Meta, TikTok, and Snap with `next/script` and `strategy="lazyOnload"`.
- If an env id is empty, skip that platform. The site must work with all three empty.
- Before the scripts load, push calls into `window.__nawaPixelQueue`. Flush the queue when each pixel reports ready.
- SPA: on `usePathname` change, fire PageView / Pageview / PAGE_VIEW with a new event id, and POST `/api/events`.
- Never `await` a pixel before painting or before `POST /api/orders`.
- Identify calls happen only after a valid phone exists, and they send raw values in the format in [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md).

## Env

See [13-DEPLOYMENT-AND-ENV.md](13-DEPLOYMENT-AND-ENV.md). Only `NEXT_PUBLIC_*` values may appear in the client bundle. No secrets.

## Docker

Multi-stage. `node:22-alpine`. Build with `output: "standalone"`. The runtime image copies `.next/standalone` and `.next/static` and `public`. Listen on `0.0.0.0:3000`.

`next.config.ts` must set `images.unoptimized` only if the host cannot run the image optimizer. Prefer the optimizer. Allow no remote patterns; images are local.

## Responsive check

Before calling the frontend done, click through at 390 and 1280: home, a PDP, add the 2-piece offer, open the drawer, add a cross-sell, open checkout, enter `0512345678` and a name, see the upsell, decline, and land on thank-you against a local API. Then repeat and accept the upsell. Confirm the total is 279 then 279+99.
