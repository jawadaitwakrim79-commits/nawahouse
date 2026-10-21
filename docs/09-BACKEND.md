# Backend

## Stack

| Piece | Choice |
|---|---|
| Python | 3.12 |
| API | FastAPI |
| Server | uvicorn |
| Models | SQLAlchemy 2, typed |
| Migrations | Alembic |
| Schemas | Pydantic v2 |
| HTTP | httpx, timeouts 5 seconds |
| DB driver | asyncpg |

## Folder

```
backend/
  app/
    main.py
    core/config.py
    core/phone.py
    core/pricing.py
    core/hashing.py
    db/session.py
    db/base.py
    models/
    schemas/
    api/router.py
    api/routes/orders.py
    api/routes/events.py
    api/routes/contact.py
    api/routes/health.py
    services/orders.py
    services/sheets.py
    services/capi.py
  alembic/
  alembic.ini
  Dockerfile
  entrypoint.sh
  requirements.txt
  .env.example
  tests/test_pricing.py
  tests/test_phone.py
  tests/test_hashing.py
```

## Startup

`entrypoint.sh`:

```sh
#!/bin/sh
set -e
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The container command is this script, not a bare uvicorn, so a new deploy migrates before it serves.

## Database URL

The EasyPanel internal URL is:

```
postgres://nawahouse:nawahouse@nawahouse_database:5432/nawahouse?sslmode=disable
```

The name `namabeauty` does not exist on this server. Do not create it.

Normalize on boot:

- Replace the scheme `postgres://` or `postgresql://` with `postgresql+asyncpg://`.
- If `sslmode=disable` is present, remove it from the URL and pass `ssl=False` to asyncpg.
- If the host is `nawahouse_database`, SSL stays off. That hostname only exists on the Docker network.

## Routes

| Method | Path | Behavior |
|---|---|---|
| GET | `/health` | `{ "ok": true }` |
| POST | `/api/orders` | Validate, price, insert, sheet, CAPI purchase, return order |
| POST | `/api/events` | Forward a non-purchase event. Reject `Purchase`, `CompletePayment`, and `PURCHASE` |
| POST | `/api/contact` | Store a message. No pixel. |

CORS: `https://nawahouse.shop`. Allow headers `Content-Type`. Allow POST and GET. Credentials not required.

## POST /api/orders

Body:

```json
{
  "event_id": "uuid",
  "name": "نورة القحطاني",
  "phone": "0512345678",
  "lines": [
    { "slug": "oud", "quantity": 2, "pricing": "main" },
    { "slug": "shafaq", "quantity": 1, "pricing": "upsell" }
  ],
  "page_url": "https://nawahouse.shop/products/oud",
  "fbp": null,
  "fbc": null,
  "ttp": null,
  "ttclid": null,
  "sc_click_id": null,
  "external_id": "uuid-from-nawa_eid",
  "event_source_url": "https://nawahouse.shop/thank-you"
}
```

Rules:

- `event_id` is a UUID.
- At least one main line. Quantities are integers 1 through 6.
- At most one upsell line, quantity exactly 1.
- Slugs are only `oud`, `shafaq`, `safa`.
- Total is `order_total(main_units, upsell_units)` from [04-CRO-OFFERS-CHECKOUT.md](04-CRO-OFFERS-CHECKOUT.md). Ignore any total field if the client sends one.
- Phone must normalize. Store E.164 in `phone_e164`.
- Name trimmed, 2 to 60 characters, not digits only.
- Read client IP from `X-Forwarded-For` first hop, else the socket. Store it. Send it to CAPI unhashed.
- Read `User-Agent` and send it unhashed.

Response 201:

```json
{
  "order_id": "NAW-1001",
  "event_id": "same-uuid",
  "total_sar": 378,
  "currency": "SAR"
}
```

`NAW-` plus a zero-padded sequence from the database, starting at 1001.

If `event_id` already exists, return 200 with the original order and do nothing else.

## Sheet

After commit, POST the JSON described in [12-ORDERS-SHEET-AND-CONFIRMATION.md](12-ORDERS-SHEET-AND-CONFIRMATION.md) to `SHEET_WEBHOOK_URL` with a 5 second timeout. On failure, set `orders.sheet_status = "failed"` and continue. If the URL is empty, skip and set `sheet_status = "skipped"`.

## CAPI

`services/capi.py` sends Meta, TikTok, and Snap in parallel after the order commit. One platform failing does not cancel the others. Payloads, hashing, and event names are exactly [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md). Record each result on `tracking_events`.

`/api/events` uses the same sender for the upper-funnel events. It still hashes when a phone is present. AddToCart often has no phone; send IP, user agent, and click ids.

## Logging and tests

pytest for pricing, phone normalization (the five accepted shapes and a landline `0112345678` rejected), and hashing (known vectors in the tracking doc). No network in unit tests. CAPI calls are behind a function that tests can fake.

## Dependencies

Pin in `requirements.txt`:

```
fastapi
uvicorn[standard]
sqlalchemy>=2
alembic
asyncpg
pydantic>=2
pydantic-settings
httpx
python-multipart
```

Do not add Stripe, Celery, Redis, or an ORM admin.
