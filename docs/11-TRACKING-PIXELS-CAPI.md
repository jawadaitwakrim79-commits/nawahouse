# Tracking — Web Pixels and CAPI

Confirmed against Meta Conversions API, TikTok Events API 2.0, and Snap Conversions API v3.

Research notes checked during doc creation:

- Meta CAPI requires SHA-256 hashing for phone and country after normalization, while `fbp`, `fbc`, IP, and user agent stay unhashed. Pixel/CAPI dedup requires matching browser `eventID` and CAPI `event_id` with the same event name and pixel id inside the dedup window.
- TikTok Events API 2.0 requires phone normalized to E.164 with `+`, then SHA-256 hashed for server events. Dedup uses matching `event_source_id`, event name, and `event_id` between Pixel and Events API.
- Snap CAPI v3 requires normalized phone digits without `+` before hashing. Pixel `client_dedup_id` must match CAPI `event_id`; for `PURCHASE`, Pixel `transaction_id` should match CAPI `custom_data.order_id`.

## Rules that are easy to get wrong

1. The browser sends raw identifiers. It never SHA-256s them.
2. The backend SHA-256s phone, name, country, and external id before CAPI. It never hashes IP, user agent, `fbp`, `fbc`, `ttp`, `ttclid`, or Snap click id.
3. Do not hash an empty string. Omit the field.
4. Do not hash a value that is already a 64-char hex digest.
5. TikTok is the platform that keeps the `+`. Meta and Snap strip it.
6. The same `event_id` string is used on the pixel and on CAPI for that action. Purchase is deduped inside 48 hours.
7. Pixel scripts load with `next/script` `strategy="lazyOnload"`. They must not sit as blocking tags in `<head>`.
8. Purchase fires once, after the upsell decision, only if the order API returned success. The value is the amount she will pay, including 99 if she accepted.

## Phone normalization

Input example `0512345678`.

| Platform | String that gets hashed, or sent raw on the web | Plus sign |
|---|---|---|
| Meta web pixel `ph` | `966512345678` raw | no |
| Meta CAPI `user_data.ph` | SHA-256 of `966512345678` | no |
| TikTok web `ttq.identify({ phone_number })` | `+966512345678` raw | yes |
| TikTok Events API `user.phone` | SHA-256 of `+966512345678` | yes, the plus is inside the hashed string |
| Snap web `user_phone_number` | `966512345678` raw | no |
| Snap CAPI `user_data.ph` | SHA-256 of `966512345678` | no, Snap's rule deletes `+`, spaces, and dashes |

SHA-256 is UTF-8, lowercase hex. Known vectors the unit test must match:

| Input | Hex |
|---|---|
| `966512345678` | `211163de39c35e6ec1aeaa615e51b1bd275f48576ac0899d30898cef4abd5d1b` |
| `+966512345678` | `983174e91bb83244a50493aa8e1c60ac3e44e70f64af2f2ae1798cc07b7f0c14` |
| `sa` | `4cf6829aa93728e8f3c97df913fb1bfa95fe5810e2933a05943f8312a98d9cf2` |

TikTok's China exception (drop country code `86`) does not apply to `966`.

## What else is hashed

| Field | Web | CAPI |
|---|---|---|
| Phone | raw, formats above | hashed, formats above |
| First name | not sent | Meta only: lowercase trimmed first word, hashed. Arabic is unchanged by lowercase. |
| Country | Meta pixel may send `sa` raw | Meta: hash of `sa` |
| External id (`nawa_eid` UUID) | raw on the Meta and TikTok pixels, so their libraries hash it | SHA-256 of the trimmed UUID. Meta and TikTok. |
| IP, user agent | automatic on the pixel | raw |
| `fbp`, `fbc`, `ttp`, `ttclid`, Snap click id | cookie / query, raw | raw |

Omit last name if the customer typed one word. Do not copy the first name into the last name.

## Event map

One action, one id, three names. The name must match within a platform or dedup fails.

| Moment | Meta `event` / `event_name` | TikTok `event` | Snap `event_name` |
|---|---|---|---|
| Route view | `PageView` | `Pageview` | `PAGE_VIEW` |
| PDP | `ViewContent` | `ViewContent` | `VIEW_CONTENT` |
| Offer added, drawer opens | `AddToCart` | `AddToCart` | `ADD_CART` |
| Checkout modal opens | `InitiateCheckout` | `InitiateCheckout` | `START_CHECKOUT` |
| Order API 201 | `Purchase` | `CompletePayment` | `PURCHASE` |

Do not fire `AddPaymentInfo`. There is no card. Do not fire TikTok `Purchase` in addition to `CompletePayment`. One TikTok event, `CompletePayment`, on both pixel and server, so the names match.

`value` / `price` is the cart total after the action for AddToCart and InitiateCheckout, and the final charged total for Purchase. Currency is always `SAR`.

## Browser snippets

Meta. `eventID` is the fourth argument.

```js
fbq("init", META_PIXEL_ID, {
  ph: "966512345678",
  country: "sa",
  external_id: externalIdRaw,
})

fbq("track", "Purchase", {
  value: 378,
  currency: "SAR",
  content_ids: ["oud", "shafaq"],
  content_type: "product",
  contents: [
    { id: "oud", quantity: 2, item_price: 199 },
    { id: "shafaq", quantity: 1, item_price: 99 },
  ],
  num_items: 3,
}, { eventID: eventId })
```

Pass `ph` only after the number is valid. `init` without user data is fine for PageView.

TikTok. Plaintext phone includes `+`. Do not also pass `sha256_phone_number`.

```js
ttq.identify({
  phone_number: "+966512345678",
  external_id: externalIdRaw,
})

ttq.track("CompletePayment", {
  contents: [
    { content_id: "oud", content_name: "نوا عود", quantity: 2, price: 199, brand: "Nawa House" },
    { content_id: "shafaq", content_name: "نوا شفق", quantity: 1, price: 99, brand: "Nawa House" },
  ],
  content_type: "product",
  value: 378,
  currency: "SAR",
}, { event_id: eventId })
```

Snap. If you omit `client_dedup_id`, the pixel invents an id that starts with `@-` and the server can never match it. Always set it.

```js
snaptr("init", SNAP_PIXEL_ID, {
  user_phone_number: "966512345678",
})

snaptr("track", "PURCHASE", {
  client_dedup_id: eventId,
  transaction_id: "NAW-1001",
  price: 378,
  currency: "SAR",
  item_ids: ["oud", "shafaq"],
  number_items: 3,
})
```

## Meta CAPI

`POST https://graph.facebook.com/v21.0/{PIXEL_ID}/events?access_token={TOKEN}`

```json
{
  "data": [
    {
      "event_name": "Purchase",
      "event_time": 1710000000,
      "event_id": "EVENT_UUID",
      "event_source_url": "https://nawahouse.shop/products/oud",
      "action_source": "website",
      "user_data": {
        "ph": ["211163de39c35e6ec1aeaa615e51b1bd275f48576ac0899d30898cef4abd5d1b"],
        "country": ["4cf6829aa93728e8f3c97df913fb1bfa95fe5810e2933a05943f8312a98d9cf2"],
        "external_id": ["SHA256_OF_UUID"],
        "client_ip_address": "RAW_IP",
        "client_user_agent": "RAW_UA",
        "fbp": "fb.1.RAW",
        "fbc": "fb.1.TIMESTAMP.FBCLID"
      },
      "custom_data": {
        "currency": "SAR",
        "value": 378,
        "content_ids": ["oud", "shafaq"],
        "content_type": "product",
        "contents": [
          { "id": "oud", "quantity": 2, "item_price": 199 },
          { "id": "shafaq", "quantity": 1, "item_price": 99 }
        ],
        "num_items": 3,
        "order_id": "NAW-1001"
      }
    }
  ]
}
```

Dedup: pixel `event` + `eventID` equals CAPI `event_name` + `event_id`, same pixel id, within 48 hours. `fbc` format is `fb.1.{creationTimeMs}.{fbclid}`.

Add `test_event_code` at the root only when `META_TEST_EVENT_CODE` is set.

## TikTok Events API 2.0

`POST https://business-api.tiktok.com/open_api/v1.3/event/track/`

Header: `Access-Token: {TIKTOK_ACCESS_TOKEN}`

```json
{
  "event_source": "web",
  "event_source_id": "PIXEL_CODE",
  "data": [
    {
      "event": "CompletePayment",
      "event_time": 1710000000,
      "event_id": "EVENT_UUID",
      "user": {
        "phone": "983174e91bb83244a50493aa8e1c60ac3e44e70f64af2f2ae1798cc07b7f0c14",
        "external_id": "SHA256_OF_UUID",
        "ip": "RAW_IP",
        "user_agent": "RAW_UA",
        "ttclid": "RAW_TTCLID",
        "ttp": "RAW_TTP"
      },
      "page": {
        "url": "https://nawahouse.shop/products/oud"
      },
      "properties": {
        "currency": "SAR",
        "value": 378.0,
        "content_type": "product",
        "contents": [
          {
            "content_id": "oud",
            "content_name": "نوا عود",
            "quantity": 2,
            "price": 199,
            "brand": "Nawa House"
          }
        ]
      }
    }
  ]
}
```

`event_time` is seconds, not milliseconds. Dedup key is pixel code + `event` + `event_id`. Phone hash includes the `+`. `value` is a number.

Add `test_event_code` at the root only when `TIKTOK_TEST_EVENT_CODE` is set.

## Snap CAPI v3

`POST https://tr.snapchat.com/v3/{PIXEL_ID}/events?access_token={TOKEN}`

```json
{
  "data": [
    {
      "event_name": "PURCHASE",
      "event_time": 1710000000,
      "event_id": "EVENT_UUID",
      "action_source": "WEB",
      "event_source_url": "https://nawahouse.shop/products/oud",
      "user_data": {
        "ph": ["211163de39c35e6ec1aeaa615e51b1bd275f48576ac0899d30898cef4abd5d1b"],
        "client_ip_address": "RAW_IP",
        "client_user_agent": "RAW_UA",
        "sc_click_id": "RAW_SC_CID"
      },
      "custom_data": {
        "currency": "SAR",
        "value": 378,
        "order_id": "NAW-1001",
        "content_ids": ["oud", "shafaq"],
        "num_items": 3
      }
    }
  ]
}
```

Pixel `client_dedup_id` must equal CAPI `event_id`. Pixel `transaction_id` must equal CAPI `custom_data.order_id`. The first pair dedupes for 48 hours. The order pair is the fallback for purchases, up to 30 days. Send IP and user agent raw on v3. Do not use the legacy `hashed_ip_address` field.

`sc_click_id` is the `ScCid` query value captured on landing.

Add `test_event_code` on the event only when `SNAP_TEST_EVENT_CODE` is set.

## Deferred loading

```tsx
<Script id="meta-pixel" strategy="lazyOnload" />
<Script id="tiktok-pixel" strategy="lazyOnload" />
<Script id="snap-pixel" strategy="lazyOnload" />
```

`lazyOnload` waits for the window load event, so the hero is not competing with pixel JavaScript.

Until `fbq` / `ttq` / `snaptr` exist, push `{ platform, name, payload, eventId }` into `window.__nawaPixelQueue` and flush on load. The order request must not wait for that flush.

PageView on the first load is queued the same way, then flushed. A second PageView is sent on App Router path changes with a new event id.

## Purchase guard

```ts
const key = `nawa_purchase_fired_${orderId}`
if (sessionStorage.getItem(key)) return
sessionStorage.setItem(key, "1")
firePurchasePixels()
```

The server guard is the unique `client_event_id`. Both are required. Closing the tab after 201 but before the pixel still leaves the CAPI purchase in place. Refreshing thank-you does not create another one.
