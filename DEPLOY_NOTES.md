# نوا للبيت — Deploy notes (post-rebrand + admin dashboard)

## 1. Database migration

Run **one** of the following:

```bash
# Option A — via Alembic (preferred if you deploy backend normally)
cd backend && alembic upgrade head

# Option B — raw SQL (if you want to apply directly)
psql "$DATABASE_URL" -f backend/sql/0002_page_clicks.sql
```

Creates one new table: `page_clicks` (indexes on `session_id`, `client_ip`,
`country_code`, `is_valid_ksa`, `created_at`).

Nothing is dropped or altered on existing tables.

## 2. Backend dependencies

Rebuild the backend container so `jinja2` and `maxminddb` are installed:

```bash
docker compose build backend
docker compose up -d backend
```

## 3. New environment variables (backend `.env`)

Copy these into your deployed `.env` and fill in real values:

```ini
# ── Admin dashboard (REQUIRED — otherwise /admin returns 503) ──
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me-to-a-long-random-string-at-least-32-chars

# ── MaxMind (choose A or B) ──
# A. Local MMDB file (free GeoLite2-Country.mmdb or paid GeoIP2-City.mmdb).
#    Mount the file into the container at this absolute path:
MAXMIND_DB_PATH=/app/geoip/GeoLite2-Country.mmdb
# B. OR MaxMind Web Services (paid; one API call per lookup):
MAXMIND_ACCOUNT_ID=
MAXMIND_LICENSE_KEY=

# ── VPN detection (pick ONE provider) ──
VPN_PROVIDER=ipqualityscore   # or: proxycheck | ipinfo
VPN_API_KEY=your-api-key-here

# When true, dashboard counts only clicks from SA + non-VPN as valid.
STRICT_KSA_ONLY=true
```

### MaxMind setup (free tier)

1. Sign up at <https://www.maxmind.com/en/geolite2/signup>
2. Create a license key under "Manage License Keys".
3. Download `GeoLite2-Country.mmdb` (free, updates weekly).
4. Add to your `docker-compose.yml` for the backend service:
   ```yaml
   volumes:
     - ./geoip:/app/geoip:ro
   ```
5. Place the `.mmdb` file in `./geoip/` on the host.

### VPN provider setup — one of

- **IPQualityScore** (recommended, 5,000 free lookups/mo): <https://ipqualityscore.com/create-account>
- **ProxyCheck.io** (1,000 free/day): <https://proxycheck.io/>
- **IPinfo** (requires paid "Standard" plan for VPN flag): <https://ipinfo.io/account/billing>

## 4. Admin dashboard access

Once deployed with `ADMIN_USERNAME` + `ADMIN_PASSWORD` set:

- **URL**: `https://api.nawahouse.shop/admin`
- Browser pops HTTP Basic Auth prompt → enter the credentials from `.env`.
- Three pages:
  - `/admin/` — overview (KPIs, traffic breakdown, 30-day chart, top products, recent orders)
  - `/admin/orders` — paginated orders list with filter by status + date range
  - `/admin/orders/{public_id}` — single order detail with click-to-call and WhatsApp links

**Security notes**:
- `noindex, nofollow` is set on all admin pages.
- `/admin` returns `503` if either env var is empty — won't accidentally expose
  the dashboard with default credentials.
- Credentials use `secrets.compare_digest` (constant-time, timing-safe).
- **Recommended**: restrict access at the reverse-proxy level with an IP allowlist
  for your own IP, in addition to Basic Auth.

## 5. Frontend changes

No new env vars. Rebuild:

```bash
docker compose build frontend
docker compose up -d frontend
```

The site now:
- Fires a `POST /api/track-click` on every page view (fire-and-forget).
- Uses the new olive-apothecary palette automatically (all existing
  `bg-brand` / `bg-brand-deep` classes inherit new values from updated CSS tokens).
- Serves auto-generated favicon via `app/icon.tsx` + `app/apple-icon.tsx`
  (Next.js generates PNGs at build time — no manual `.ico` needed).

## 6. What was NOT changed

- Database tables `orders`, `order_items`, `tracking_events`, `contact_messages`,
  `products` — untouched.
- Order flow, pricing (199/279/349), COD, confirmation call — all preserved.
- Zustand cart, checkout modal, upsell modal — unchanged.
- Google Sheet mirror — unchanged.
- Meta/TikTok/Snap pixel + CAPI — unchanged.
- Fonts (Amiri, IBM Plex Arabic, Outfit) — unchanged.

## 7. What's still MISSING (needs your input)

I built pluggable integration points for MaxMind + VPN detection, but I did
**not** find either library/credentials in your existing codebase. Before
`STRICT_KSA_ONLY=true` becomes meaningful, you must either:

1. **Download MaxMind GeoLite2-Country.mmdb** (free) and set `MAXMIND_DB_PATH`, **or**
2. **Add paid MaxMind credentials** (`MAXMIND_ACCOUNT_ID` + `MAXMIND_LICENSE_KEY`).

AND one of:

3. **Sign up for a VPN detection provider** and set `VPN_PROVIDER` + `VPN_API_KEY`.

Until then, every click is marked `is_valid_ksa = FALSE` and the dashboard will
show 0 valid clicks. The admin UI shows a visible warning banner for both missing
pieces so you don't miss it.

## 8. New files inventory

**Frontend**:
- `frontend/app/globals.css` *(modified)* — new color tokens
- `frontend/components/Logo.tsx` *(modified)* — new fill + `variant` prop
- `frontend/content/copy.ts` *(modified)* — new secondary tag, hero, about
- `frontend/app/page.tsx` *(modified)* — new eyebrow + trust strip + rituals sub
- `frontend/app/about/page.tsx` *(rewritten)* — pillars + closing promise
- `frontend/components/footer/Footer.tsx` *(rewritten)* — brand block, no emojis
- `frontend/components/product/PDPHero.tsx` *(modified)* — brass SAR label
- `frontend/app/layout.tsx` *(modified)* — ClickTracker + theme color
- `frontend/app/icon.tsx` *(new)* — favicon
- `frontend/app/apple-icon.tsx` *(new)* — apple touch icon
- `frontend/components/ClickTracker.tsx` *(new)* — page view beacon

**Backend**:
- `backend/app/core/config.py` *(modified)* — admin + MaxMind + VPN envs
- `backend/app/models/click.py` *(new)* — PageClick model
- `backend/app/models/__init__.py` *(modified)* — export PageClick
- `backend/app/services/ip_intel.py` *(new)* — MaxMind + VPN providers
- `backend/app/api/routes/clicks.py` *(new)* — POST /api/track-click
- `backend/app/api/router.py` *(modified)* — register clicks router
- `backend/app/main.py` *(modified)* — mount admin router
- `backend/app/admin/__init__.py` *(new)*
- `backend/app/admin/auth.py` *(new)* — HTTP Basic Auth
- `backend/app/admin/queries.py` *(new)* — metrics aggregation
- `backend/app/admin/router.py` *(new)* — admin HTTP routes
- `backend/app/admin/templates/base.html` *(new)*
- `backend/app/admin/templates/dashboard.html` *(new)*
- `backend/app/admin/templates/orders.html` *(new)*
- `backend/app/admin/templates/order_detail.html` *(new)*
- `backend/alembic/versions/0002_page_clicks.py` *(new)*
- `backend/sql/0002_page_clicks.sql` *(new)* — raw SQL alternative
- `backend/.env.example` *(modified)* — all new env vars
- `backend/requirements.txt` *(modified)* — jinja2 + maxminddb

**Root**:
- `BRAND.md` *(new, from prior turn)* — brand identity & positioning
- `PRODUCT_IMAGE_PROMPTS.md` *(new)* — Gemini prompts for 3 products
- `DEPLOY_NOTES.md` *(this file)*
