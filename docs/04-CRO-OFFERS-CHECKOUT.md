# CRO, Offers, and Checkout

## Prices

Every main unit is the same product economically. The cart counts **main units**, any mix of slugs.

| Main units in the cart | Total SAR |
|---|---|
| 1 | 199 |
| 2 | 279 |
| 3 | 349 |
| Each unit after the third | +199 |

Examples:

- One نوا عود = 199
- Two نوا عود = 279
- نوا عود + نوا شفق = 279
- One of each of the three = 349
- Three نوا صفاء + one نوا عود = 349 + 199 = 548

The upsell unit is not a main unit. It is 99 SAR, one per order, and it does not change the ladder.

Server function, the only price authority:

```python
def main_total(units: int) -> int:
    if units <= 0:
        return 0
    if units == 1:
        return 199
    if units == 2:
        return 279
    if units == 3:
        return 349
    return 349 + 199 * (units - 3)

def order_total(main_units: int, upsell_units: int) -> int:
    if upsell_units not in (0, 1):
        raise ValueError("one upsell max")
    return main_total(main_units) + 99 * upsell_units
```

Reject the order if the client total differs. The client may display the total; it may not decide it.

## How the offer feels

Product cards, home, shop, cross-sells, and thank-you recommendations show **199 ر.س** only. No percent, no "was", no red sale chip, no word خصم or وفرّي.

The ladder is a sentence:

> قطعة ١٩٩ · قطعتان ٢٧٩ · ثلاث قطع ٣٤٩
> كلما اكتمل البيت، صار السعر سعر طقس، مو سعر قطعة.

On the PDP the visitor picks the offer before the CTA:

- قطعة واحدة — ١٩٩ ر.س
- قطعتان — ٢٧٩ ر.س
- الطقس الكامل، ثلاث قطع — ٣٤٩ ر.س

Default selection: قطعتان. That is the AOV default. She can switch to one or three. The CTA adds **that quantity of the current slug** and opens the cart drawer. It does not go to checkout by itself.

Copy on the picker never says "وفّري ١١٩". It says the three prices as the price of the ritual size.

## Cart drawer

Opens from the right edge toward the left in visual terms? In RTL the drawer slides in from the **left** of the screen (the end side), so it does not cover the logo. Full height. Focus trap. Close on the backdrop and on Escape.

Contents, top to bottom:

1. عنوان: سلتكِ
2. Lines. Each line: image, name, enemy in one short line, quantity stepper, line note «ضمن سعر السلة».
3. The stepper changes main-unit count and the server-mirrored total updates immediately on the client with the same function. Quantity minimum 1. Trash removes the line.
4. Ladder reminder, three quiet figures, the active tier marked with the brand color. No strike-through.
5. Total label: المجموع. One number. If she has 2 units, she sees 279, not 398.
6. Cross-sell. Products whose slug is absent. Each is a compact card: name, enemy, 199 ر.س, button «أضيفيها». Adding it increases main units by 1 and reprices the whole cart. If all three slugs are present, replace the block with «الطقس مكتمل. تقدرين تعدّلين الكمية من فوق.»
7. Trust row: الدفع عند الاستلام · نتصل قبل الشحن · ٣٠ يوم ترجيع
8. CTA: إتمام الطلب. Opens the checkout modal. Disabled if the cart is empty.

Do not put a coupon field. Do not put a discount code. Do not put WhatsApp checkout.

## Checkout modal

Opened only from the cart CTA. Mobile: full screen. Desktop: dialog, max-width 480px. The cart drawer stays underneath.

Blocks:

1. ملخص الطلب. Names, quantities, one total. Upsell is not in this summary yet.
2. One social line, no fake number: «الدفع عند الاستلام، ونتصل نأكّد العنوان قبل ما يطلع المندوب.»
3. Scarcity that is real: none, until she submits. Do not show "٣ قطع باقية".
4. Field, الاسم. Required. Trim. Minimum two letters, Arabic or Latin. Maximum 60. Reject digits-only.
5. Field, الجوال. `inputMode="tel"`, placeholder `05xxxxxxxx`. Accept only a Saudi mobile.
6. CTA: أكّدي الطلب بالدفع عند الاستلام. Disabled until both fields are valid. Inline errors under the fields, not an alert box at the top only.

### Saudi mobile

Accept these human inputs and normalize to E.164 `+9665XXXXXXXX`:

- `05XXXXXXXX`
- `5XXXXXXXX`
- `9665XXXXXXXX`
- `+9665XXXXXXXX`
- `009665XXXXXXXX`

After stripping spaces, dashes, and parentheses, the national number is `5` plus 8 digits. Landlines, short codes, and numbers that do not start with 5 are invalid. Use `libphonenumber-js` with default country `SA` and require type mobile, and keep the regex above as the explicit rule so a library quirk cannot accept a landline.

Show the error «اكتبي رقم جوال سعودي، مثل 05xxxxxxxx» only after blur or submit, not on the first keystroke.

## Upsell

When the CTA is pressed and both fields are valid, do **not** create the order yet. Replace the modal body with the upsell. Keep name and phone in memory.

- Duration: 15 seconds. A visible countdown. At 0, submit the order without the upsell.
- One product, chosen by the rule in [03-PRODUCTS-AND-SCIENCE.md](03-PRODUCTS-AND-SCIENCE.md).
- Price on this screen only: ١٩٩ next to ٩٩ ر.س. This is the only strike-through on the website. Label it «عرض التأكيد، ١٥ ثانية» so the timer is the reason, not a permanent sale.
- Primary button: أضيفيها بـ ٩٩
- Secondary: لا، ثبّتي طلبي مثل ما هو
- Both buttons submit immediately. The timer stops. A pending state «جاري تثبيت الطلب» replaces the buttons so she cannot double-submit.
- If the upsell UI throws, submit the base order anyway.

The 99 unit is stored as `pricing = "upsell"`, quantity 1, sku as chosen. It is not merged into a main line of the same sku.

## Thank-you

Route `/thank-you?order=NAW-1001`. If there is no order id in the session created by this browser, show a calm not-found state, not someone else's order.

Sections:

1. طلبكِ وصل. رقم الطلب.
2. المجموع، والدفع عند الاستلام.
3. The confirmation block, large: «بنتصل خلال ساعات العمل من رقمنا نأكّد الحي والعنوان. إذا ما رديتي، الطلب ما يطلع للتوصيل.» Hours: ٤ عصرًا إلى ١١ مساءً، بتوقيت الرياض.
4. What to prepare: الاسم، الحي، أقرب معلم، وقت يناسبها.
5. The products she did not buy, at 199, as links. Adding them starts a new cart. Do not silently edit the placed order.
6. No second upsell. No coupon.

## Confirmation rate, delivery rate, AOV

AOV: default the PDP picker to two pieces. Reprice the cart in front of her when she adds the cross-sell, so the second and third pieces are how the house gets finished. One upsell at the moment of highest intent.

Confirmation rate: two fields only. Tell her before she submits that a call is coming. Repeat it on the thank-you page in larger type than the order id. The sheet status starts at `new`. Nothing is marked shipped until a person sets `confirmed`.

Delivery rate: the call collects city, district, and address into the sheet. The courier is not called on `no_answer`. See [12-ORDERS-SHEET-AND-CONFIRMATION.md](12-ORDERS-SHEET-AND-CONFIRMATION.md).

## Events tied to this funnel

Fire tracking only at the moments in [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md). Purchase fires once, after the upsell decision, on the successful order response, with the **final** total including 99 if she accepted. A refresh of the thank-you page must not fire Purchase again.

## Empty, error, and slow states

- Empty cart CTA stays disabled.
- Order API error: stay on the upsell-or-form step she was on, show «ما ثبت الطلب. جرّبي مرة ثانية، طلبكِ ما انحسب.» Do not clear name and phone. Do not fire Purchase.
- Slow network: keep the pending label, ignore extra clicks, timeout the client at 20 seconds, then show the same error.
- Double click: one in-flight request. The button stays disabled until it settles.
