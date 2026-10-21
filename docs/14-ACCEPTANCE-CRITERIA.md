# Acceptance Criteria

The build is done when every line below is true. A page that looks right but prices wrong is not done.

## Brand and catalog

- The Arabic wordmark is نوا للبيت and the English line is Nawa House.
- The header starts, on the right, with an N inside a circle of `#8C4A32`.
- The only products are نوا عود, نوا شفق, and نوا صفاء, slugs `oud`, `shafaq`, `safa`.
- No beauty SKU, no Nama Beauty, no `namabeauty` database, no reseller language.
- No SASO, SFDA, press, or "verified purchase" badge.
- Sample reviews have no count and no badge.

## Money

- Cards show 199 SAR and no strike-through.
- Picker defaults to two pieces.
- Totals: 1 → 199, 2 → 279, any mix of 2 → 279, 3 → 349, 4 → 548.
- An accepted upsell adds 99 and does not change the ladder count. Two main units plus upsell = 378.
- The struck-through 199 appears only inside the 15-second upsell.
- The server rejects a client total that does not match. Test this by tampering the payload.
- There is no coupon field and no card payment.

## Funnel

- PDP CTA adds the selected quantity and opens the drawer.
- The drawer shows the missing products at 199 and adding one reprices the cart.
- Cart CTA opens the checkout modal. There is no `/cart` page.
- The form accepts `0512345678`, `512345678`, `966512345678`, `+966512345678`, and `00966512345678`.
- The form rejects `0112345678` and `12345`.
- Valid submit shows the upsell for 15 seconds. Yes, No, and timeout all place the order. Yes includes the 99 line.
- A failed POST does not go to thank-you and does not fire Purchase.
- Thank-you tells her to answer the confirmation call.

## Tracking

- Pixel scripts use `lazyOnload` and are absent when their env id is empty.
- Browser payloads are unhashed. TikTok's raw phone includes `+`. Meta and Snap raw phones do not.
- CAPI hashes match the vectors in [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md).
- One order produces one Meta Purchase, one TikTok CompletePayment, and one Snap PURCHASE, each with the same event id on pixel and server.
- Refreshing thank-you does not fire a second purchase.
- Retrying the same `event_id` does not create a second order or a second sheet row.

## Data and deploy

- `GET /health` is ok.
- Migrations run from the backend container entrypoint before uvicorn.
- `DATABASE_URL` is the `nawahouse` internal URL, with `sslmode=disable` handled so asyncpg still connects.
- A successful order is in Postgres and in the sheet, with the columns from the CSV.
- `frontend/.env.example` and `backend/.env.example` exist and match [13-DEPLOYMENT-AND-ENV.md](13-DEPLOYMENT-AND-ENV.md).
- Both folders have a Dockerfile. The repo has a `.gitignore` that ignores `.env`.
- Sample images exist at the paths in [06-DESIGN-SYSTEM.md](06-DESIGN-SYSTEM.md).
- At 390px and 1280px, alternating sections put the text on the right, then on the left, then on the right. Mobile stacks text above the image.

## Tests

`pytest` passes for pricing, phone, and hashing. The frontend pricing tests pass for the same numbers.
