# Orders, Google Sheet, and Confirmation

Postgres is the source of truth. The sheet is the call desk. The script to paste into the sheet is [sheet/google-apps-script.js](sheet/google-apps-script.js). The header row is [sheet/orders-template.csv](sheet/orders-template.csv).

## Webhook

Backend `POST`s JSON to `SHEET_WEBHOOK_URL` after the order commits. Body:

```json
{
  "secret": "SHEET_WEBHOOK_SECRET",
  "order_id": "NAW-1001",
  "created_at_riyadh": "2026-09-30 21:05",
  "status": "new",
  "customer_name": "نورة القحطاني",
  "phone_e164": "+966512345678",
  "phone_local": "0512345678",
  "items": "نوا عود × 2 | نوا شفق × 1 (upsell 99)",
  "main_units": 2,
  "upsell_accepted": "yes",
  "upsell_slug": "shafaq",
  "total_sar": 378,
  "currency": "SAR",
  "payment_method": "COD",
  "page_url": "https://nawahouse.shop/products/oud",
  "event_id": "uuid",
  "fbp": "",
  "fbc": "",
  "ttclid": "",
  "ttp": "",
  "sc_click_id": "",
  "client_ip": "",
  "user_agent": ""
}
```

`created_at_riyadh` is `Asia/Riyadh`, `YYYY-MM-DD HH:mm`. `phone_local` is `0` plus the 9-digit national number.

Apps Script web apps often drop custom headers. The secret is a field in the JSON, not a header. Deploy the web app as "Anyone" and treat the secret as the lock. Rotate it in Apps Script properties and in EasyPanel together.

If the script sees the same `order_id` already in column A, it returns `{ "ok": true, "duplicate": true }` and does not append.

The operator fills these empty columns during the call. The webhook leaves them blank:

`city`, `district`, `address`, `landmark`, `call_attempts`, `call_notes`, `confirmed_at`, `shipped_at`, `delivered_at`, `cancel_reason`

## Call script

Hours in the store copy are 4pm to 11pm Riyadh. Call from the number printed on the site.

1. «أهلين، معكِ نوا للبيت. أتصل أأكد طلب {الاسم} بقيمة {المجموع} ر.س، الدفع عند الاستلام.»
2. Read the items. If there is an upsell, mention it as part of the same total, not as a surprise.
3. Ask for المدينة، الحي، أقرب معلم، والعنوان. Write them in the sheet.
4. «المندوب بيتواصل قبل ما يوصل. إذا العنوان هذا، أأكد الطلب الحين.»
5. If she confirms, status `confirmed`. If she does not answer, status `no_answer`, increment `call_attempts`. Three attempts, then `cancelled` with reason `no_answer`. Do not ship `new` or `no_answer`.

That call is why the form only asks for name and phone. The address is taken from a person, so the courier is not sent to a guess.

## Thank-you alignment

The page says a call is coming and the order does not ship until she answers. The sheet starts at `new`. Those two sentences must stay true. Do not hand the row to a courier integration in the MVP.

## Replay

If `sheet_status` is `failed`, a manual `POST` of the same body is safe because the script dedupes on `order_id`.
