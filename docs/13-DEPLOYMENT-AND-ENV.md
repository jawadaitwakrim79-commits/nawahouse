# Deployment and Environment

Two EasyPanel apps from one GitHub repo, plus the Postgres database that is already installed.

| App | Domain | Dockerfile |
|---|---|---|
| `frontend/` | `nawahouse.shop` | `frontend/Dockerfile` |
| `backend/` | `api.nawahouse.shop` | `backend/Dockerfile` |

The database hostname `nawahouse_database` only resolves inside EasyPanel's network. The backend service must be attached to that network. The public internet must not reach port 5432.

## Backend environment

Create `backend/.env.example` with this content. In EasyPanel, fill the same keys. The database URL below is the internal URL for this project. Copy it as-is.

```
DATABASE_URL=postgres://nawahouse:nawahouse@nawahouse_database:5432/nawahouse?sslmode=disable
CORS_ORIGINS=https://nawahouse.shop
PUBLIC_SITE_URL=https://nawahouse.shop
SHEET_WEBHOOK_URL=
SHEET_WEBHOOK_SECRET=
META_PIXEL_ID=
META_CAPI_ACCESS_TOKEN=
META_TEST_EVENT_CODE=
TIKTOK_PIXEL_CODE=
TIKTOK_ACCESS_TOKEN=
TIKTOK_TEST_EVENT_CODE=
SNAP_PIXEL_ID=
SNAP_CAPI_ACCESS_TOKEN=
SNAP_TEST_EVENT_CODE=
```

Leave test event codes empty in production. A non-empty test code marks events as tests and they will not optimize ads.

## Frontend environment

Create `frontend/.env.example`:

```
NEXT_PUBLIC_SITE_URL=https://nawahouse.shop
NEXT_PUBLIC_API_URL=https://api.nawahouse.shop
NEXT_PUBLIC_META_PIXEL_ID=
NEXT_PUBLIC_TIKTOK_PIXEL_ID=
NEXT_PUBLIC_SNAP_PIXEL_ID=
NEXT_PUBLIC_CONTACT_PHONE=
NEXT_PUBLIC_CONTACT_EMAIL=
```

Pixel ids are public by nature. Tokens are not. Tokens stay on the backend.

`NEXT_PUBLIC_API_URL` has no trailing slash.

## Docker

Backend image: `python:3.12-slim`. Install `requirements.txt`. Copy the app and `alembic.ini`. `ENV PYTHONUNBUFFERED=1`. Expose 8000. Entrypoint `entrypoint.sh` runs `alembic upgrade head` then uvicorn. If the migration fails, the container must exit. Do not start uvicorn anyway.

Frontend image: `node:22-alpine`, multi-stage, Next standalone, expose 3000. Build args must pass the `NEXT_PUBLIC_*` values, because Next inlines them at build time. Set those build args in EasyPanel to the same values as the runtime env, or the browser will call the wrong API.

Both Dockerfiles have a `.dockerignore` that excludes `.env`, `.git`, and `node_modules` / `__pycache__`.

## GitHub

Repo root contains `frontend/`, `backend/`, and `docs/`. Do not commit `.env`. Do commit `.env.example`.

Suggested `.gitignore`:

```
.env
.env.local
node_modules
.next
__pycache__
.venv
*.pyc
.pytest_cache
```

EasyPanel builds from the Dockerfile path, not from a compose file. Still add `docker-compose.yml` at the root for local use:

- service `db` image `postgres:16`, database `nawahouse`, user `nawahouse`, password `nawahouse`, port 5432
- service `backend` build `./backend`, depends on db, env `DATABASE_URL=postgres://nawahouse:nawahouse@db:5432/nawahouse?sslmode=disable`
- service `frontend` build `./frontend`, env `NEXT_PUBLIC_API_URL=http://localhost:8000`

Local compose is for the coder's machine. Production uses the existing EasyPanel database, not a second Postgres.

## Domains

- `https://nawahouse.shop` → frontend port 3000
- `https://api.nawahouse.shop` → backend port 8000
- EasyPanel terminates TLS. The app itself can speak HTTP inside the network.

## Health

EasyPanel health check for the backend: `GET /health`.

## Sheet deploy

1. Create a Google Sheet. File → Import `docs/sheet/orders-template.csv`, or paste the header row into row 1.
2. Extensions → Apps Script. Replace the default file with `docs/sheet/google-apps-script.js`.
3. Project settings → Script properties → `WEBHOOK_SECRET` = the same value as `SHEET_WEBHOOK_SECRET`.
4. Deploy → New deployment → Web app. Execute as Me. Who has access: Anyone.
5. Copy the `/exec` URL into `SHEET_WEBHOOK_URL`.

## First boot check

After deploy:

1. `GET https://api.nawahouse.shop/health` returns ok.
2. The `products` table has three rows. Alembic version is applied.
3. A test order with phone `0512345678` writes one database row and one sheet row.
4. Repeating the same `event_id` does not write a second row.
5. With test event codes set, Meta, TikTok, and Snap test tools show one Purchase / CompletePayment / PURCHASE, not two.
