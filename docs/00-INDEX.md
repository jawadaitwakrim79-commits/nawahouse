# Nawa House — Document Index

Read in this order. Later files win on implementation detail. Earlier files win on brand and offer rules.

| File | What it locks |
|---|---|
| [01-BRAND-AND-POSITIONING.md](01-BRAND-AND-POSITIONING.md) | Name, enemy, promise, what we never say |
| [02-ICP-AND-LANGUAGE.md](02-ICP-AND-LANGUAGE.md) | Who she is, Saudi voice, words to use and avoid |
| [03-PRODUCTS-AND-SCIENCE.md](03-PRODUCTS-AND-SCIENCE.md) | The only 3 SKUs, claims gate, specs |
| [04-CRO-OFFERS-CHECKOUT.md](04-CRO-OFFERS-CHECKOUT.md) | 199 / 279 / 349, cart, checkout, 99 upsell |
| [05-SITEMAP-PAGES-AND-COPY.md](05-SITEMAP-PAGES-AND-COPY.md) | Every page, section, and Arabic line to ship |
| [06-DESIGN-SYSTEM.md](06-DESIGN-SYSTEM.md) | Color, type, logo, RTL layout, sample images |
| [07-ARCHITECTURE.md](07-ARCHITECTURE.md) | System shape, trust boundaries, request flows |
| [08-FRONTEND.md](08-FRONTEND.md) | Next.js app, components, coding rules |
| [09-BACKEND.md](09-BACKEND.md) | FastAPI, pricing, orders, pixels, sheet |
| [10-DATABASE.md](10-DATABASE.md) | Postgres schema and seed |
| [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md) | Meta, TikTok, Snap web + CAPI, hash, dedup |
| [12-ORDERS-SHEET-AND-CONFIRMATION.md](12-ORDERS-SHEET-AND-CONFIRMATION.md) | Sheet columns, Apps Script, call script |
| [13-DEPLOYMENT-AND-ENV.md](13-DEPLOYMENT-AND-ENV.md) | Docker, EasyPanel, env examples |
| [14-ACCEPTANCE-CRITERIA.md](14-ACCEPTANCE-CRITERIA.md) | Done means this, nothing less |
| [15-PAID-SOCIAL-TRAFFIC-AND-CRO.md](15-PAID-SOCIAL-TRAFFIC-AND-CRO.md) | Snapchat/TikTok traffic, UGC hooks, message match, AOV checks |
| [CODER-PROMPT.md](CODER-PROMPT.md) | Prompt to paste into the coding agent |
| [sheet/orders-template.csv](sheet/orders-template.csv) | Header row for the Google Sheet |
| [sheet/google-apps-script.js](sheet/google-apps-script.js) | Script to paste into the sheet |
| [env/backend.env.example](env/backend.env.example) | EasyPanel env for the API |
| [env/frontend.env.example](env/frontend.env.example) | EasyPanel env for the site |

## Locked decisions

- Domain: `nawahouse.shop`. API: `api.nawahouse.shop`.
- Brand: **نوا للبيت** / **Nawa House**. Not Nama Beauty. Not a reseller name.
- Products: نوا عود، نوا شفق، نوا صفاء. No other SKU in MVP.
- Money: 199 / 279 / 349 SAR by piece count. The only discounted price on the site is the post-submit upsell at 99 SAR.
- Checkout: COD only. Two fields, name and a valid Saudi mobile. No account, no card, no cart page.
- Orders: Postgres is the source of truth. A Google Sheet receives a copy by webhook.
- Pixels: Meta, TikTok, and Snapchat, browser plus server, deferred, deduplicated. Hash only on the server.
- Language of the store: Arabic, `dir="rtl"`, Saudi feminine voice. English appears only in the logo lockup, spec tokens, and legal names of standards.

## What the coder must not do

- Do not put the source prompt's beauty products, beauty claims, or `namabeauty` / `Nama Beauty` anywhere.
- Do not invent certification logos, press logos, review counts, or a fake founder photograph.
- Do not show a discount, a percent, or a struck-through price anywhere except the 15-second upsell.
- Do not add a payment gateway, a login, a `/cart` route, WhatsApp Business API, or SMS OTP.
