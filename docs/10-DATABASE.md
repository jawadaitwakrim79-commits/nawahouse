# Database

Postgres database `nawahouse` on host `nawahouse_database`. The connection string the backend must accept is in [13-DEPLOYMENT-AND-ENV.md](13-DEPLOYMENT-AND-ENV.md). Alembic applies this schema on every container start before uvicorn listens.

## Tables

### products

| Column | Type | Notes |
|---|---|---|
| slug | text pk | `oud`, `shafaq`, `safa` |
| name_ar | text | نوا عود / نوا شفق / نوا صفاء |
| full_name_ar | text | the long product name |
| enemy_ar | text | the ضد line |
| price_sar | integer | always 199 |

### orders

| Column | Type | Notes |
|---|---|---|
| id | bigint pk | internal |
| public_id | text unique | `NAW-1001` |
| client_event_id | uuid unique | dedup key from the browser |
| customer_name | text | |
| phone_e164 | text | `+9665XXXXXXXX` |
| main_units | integer | |
| upsell_slug | text null | |
| total_sar | integer | |
| status | text | `new` until a person changes it |
| sheet_status | text | `sent`, `failed`, or `skipped` |
| page_url | text | |
| client_ip | text | |
| user_agent | text | |
| fbp | text null | |
| fbc | text null | |
| ttp | text null | |
| ttclid | text null | |
| sc_click_id | text null | |
| external_id | text null | raw `nawa_eid`, never hashed at rest |
| created_at | timestamptz | default `now()` |

Index `orders_phone_created_idx` on `(phone_e164, created_at)` for the daily limit.

### order_items

| Column | Type |
|---|---|
| id | bigint pk |
| order_id | bigint fk → orders.id |
| slug | text |
| quantity | integer |
| pricing | text | `main` or `upsell` |

### tracking_events

| Column | Type |
|---|---|
| id | bigint pk |
| event_id | uuid |
| event_name | text |
| platform | text | `meta`, `tiktok`, `snap` |
| http_status | integer null |
| ok | boolean |
| created_at | timestamptz |

Unique `(event_id, event_name, platform)`.

### contact_messages

| Column | Type |
|---|---|
| id | bigint pk |
| name | text |
| phone_e164 | text |
| message | text |
| created_at | timestamptz |

## Sequence

```sql
CREATE SEQUENCE order_public_seq START WITH 1001;
```

`public_id` is `'NAW-' || nextval('order_public_seq')`.

## Seed

Insert the three products in the same migration. Names and enemies are the ones in [03-PRODUCTS-AND-SCIENCE.md](03-PRODUCTS-AND-SCIENCE.md).

## Status values

The app only writes `new`. The sheet is where the operator moves an order through:

`new` → `no_answer` → `confirmed` → `shipped` → `delivered`

or `new` → `cancelled`.

Do not build an admin UI. Do not let the public API set status.
