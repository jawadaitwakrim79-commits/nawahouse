# Coder prompt

Copy everything below the line into the coding agent. The repo root is `C:\Users\PC\nawahouse`. Docs are already there. Do not ask the agent to reinvent them.

---

Build the Nawa House store from the docs in `docs/`. Read `docs/00-INDEX.md` first and follow the files in that order. `docs/14-ACCEPTANCE-CRITERIA.md` is the definition of done.

Create two apps:

- `frontend/` — Next.js 15, React 19, TypeScript, Tailwind CSS v4, RTL Arabic. Rules and folders are in `docs/08-FRONTEND.md`. Design tokens are in `docs/06-DESIGN-SYSTEM.md`.
- `backend/` — Python 3.12 FastAPI. Rules are in `docs/09-BACKEND.md`. Schema is in `docs/10-DATABASE.md`.

Also add root `docker-compose.yml` and root `.gitignore` as `docs/13-DEPLOYMENT-AND-ENV.md` describes. Copy `docs/env/frontend.env.example` to `frontend/.env.example` and `docs/env/backend.env.example` to `backend/.env.example`.

The live database URL is:

`postgres://nawahouse:nawahouse@nawahouse_database:5432/nawahouse?sslmode=disable`

Normalize it for asyncpg the way `docs/09-BACKEND.md` says. Run `alembic upgrade head` in the backend container entrypoint before uvicorn.

Brand is نوا للبيت / Nawa House. Domain `https://nawahouse.shop`. API `https://api.nawahouse.shop`. The only products are نوا عود (`oud`), نوا شفق (`shafaq`), and نوا صفاء (`safa`), specified in `docs/03-PRODUCTS-AND-SCIENCE.md`. Do not build Nama Beauty and do not sell biotin, collagen, or magnesium.

Prices, cart drawer, checkout modal, Saudi phone rules, and the 15-second 99 SAR upsell are in `docs/04-CRO-OFFERS-CHECKOUT.md`. Page copy is in `docs/05-SITEMAP-PAGES-AND-COPY.md`. Paste that Arabic. Do not rewrite it.

Paid-social message match is in `docs/15-PAID-SOCIAL-TRAFFIC-AND-CRO.md`. The store will receive cold Snapchat and TikTok traffic from UGC/AI videos, so each PDP first fold must repeat the exact pain and product promise from the ad. Preserve `fbclid`, `ttclid`, `ScCid`, and UTM context as described there.

Generate the sample WebP images listed in `docs/06-DESIGN-SYSTEM.md` into `frontend/public/images/`. No text inside the images.

Pixels and CAPI: implement `docs/11-TRACKING-PIXELS-CAPI.md` exactly. Browser pixels are deferred with `next/script` `strategy="lazyOnload"`, send raw identifiers, and never hash. The backend hashes. TikTok phone keeps the `+` before hashing (`+9665XXXXXXXX`). Meta and Snap hash digits only (`9665XXXXXXXX`). Dedup with one shared `event_id`. Unit tests must match the SHA-256 vectors in that file.

Orders go to Postgres and to the Google Sheet. Use `docs/sheet/google-apps-script.js` and `docs/sheet/orders-template.csv` as-is. Webhook contract is in `docs/12-ORDERS-SHEET-AND-CONFIRMATION.md`.

Ship Dockerfiles for both apps. Do not commit a filled `.env`. When you finish, walk `docs/14-ACCEPTANCE-CRITERIA.md` and fix anything that is still false.
