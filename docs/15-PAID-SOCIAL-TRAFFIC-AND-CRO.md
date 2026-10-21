# Paid Social Traffic and CRO Handoff

This store is built for cold traffic from Snapchat and TikTok first, then Meta. The page must feel like the continuation of a Saudi UGC video, not like a marketplace listing.

## Traffic promise

Every ad should land on the product shown in the video. Do not send a product-specific ad to the homepage unless the video sells all three rituals together.

| Ad angle | Landing page | First fold must repeat |
|---|---|---|
| Oud smell / majlis guest moment | `/products/oud` | رائحة البيت الباهتة، عود بلا فحم |
| Bedroom / evening transformation | `/products/shafaq` | جو الغرفة الممل، شفق على السقف |
| Riyadh dust / heavy air | `/products/safa` | غبار الرياض، فلتر HEPA-13 والعطر منفصل |
| Full home ritual / bundle | `/shop` or `/` | ريحة، ضوء، وهواء |

Never use a generic landing page for a specific pain. The first headline on the page must make the visitor feel she arrived at the same promise the video made.

## URL parameters

Preserve all ad click parameters through the first page load and include them in `/api/events` and `/api/orders` where relevant.

- `fbclid` creates `_fbc` if Meta did not already set it.
- `ttclid` is copied to the first-party cookie `nawa_ttclid` for 28 days.
- `ScCid` is copied to `nawa_sc_cid` for Snap CAPI as `sc_click_id`.
- `utm_source`, `utm_campaign`, `utm_adset`, `utm_ad`, and `utm_content` should be stored in session storage and sent to the order sheet if the backend schema includes optional fields later. Do not block MVP on extra UTM columns.

The tracking IDs above are not secrets and are not hashed. Phone and external IDs are hashed only in server CAPI, as specified in [11-TRACKING-PIXELS-CAPI.md](11-TRACKING-PIXELS-CAPI.md).

## Creative-to-page hooks

The coder should expose these lines as reusable copy blocks so landing sections can mirror the ad.

### نوا عود

- Hook: «بيتكِ نظيف... بس الريحة واقفة؟»
- Proof: «بدون فحم. حرارة الجهاز تطلّع العود بدل ما تحرقه.»
- Emotion: «أول ما ينفتح الباب، البيت يستقبل قبل الكلام.»
- CTA: «أضيفي طقس الاستقبال»

### نوا شفق

- Hook: «طفّي اللمبة البيضاء وشوفي الغرفة كيف تهدأ.»
- Proof: «مشهد شفق على السقف والجدار، مو لعبة أطفال ولا إضاءة شغل.»
- Emotion: «السهرة تحتاج جو، مو إضاءة أقوى.»
- CTA: «أضيفي طقس السهرة»

### نوا صفاء

- Hook: «غبار الرياض يرجع حتى بعد المسح؟»
- Proof: «فلتر HEPA-13 يمسك الغبار. العطر خانة ثانية وما يتظاهر أنه ينقّي.»
- Emotion: «هواء أخف في المجلس، وريحه اختيارية بعد التنقية.»
- CTA: «أضيفي طقس الهواء»

## Above-the-fold requirements for cold traffic

Every PDP hero must show, without scrolling on a 390px phone:

- Product name and enemy line.
- One safe proof point.
- The selected offer price, defaulting to two pieces.
- COD trust line: «الدفع عند الاستلام · نتصل قبل الشحن».
- Primary CTA.

The hero should not start with a long brand story. Cold traffic wants to know: is this the same thing from the video, can I trust it, and how do I order without paying now?

## Confirmation and delivery copy

The site should pre-frame the confirmation call before the form and after the order:

- Before submit: «بعدها يجيكِ عرض تأكيد سريع، ثم نثبت الطلب ونتصل نأكّد العنوان.»
- On thank-you: «إذا ما رديتي، الطلب ما يطلع للتوصيل.»

This is not only copy. It improves COD confirmation and prevents wasted delivery attempts.

## AOV rules for paid traffic

The default PDP picker is two pieces because cold traffic often came for one product, but the store sells a finished home ritual.

- Do not call the 2-piece default a discount.
- Cart cross-sells should be visually quiet and emotionally specific: «كمّلي الريحة بالضوء» beats «منتج مقترح».
- If the visitor has one unit, the drawer should make the second unit feel like the natural next step.
- If she has two units, the drawer should make the third unit feel like completing the house.
- The 99 SAR upsell appears only after valid name and Saudi phone because that is the highest-intent moment.

## Fake-trust guardrails

Paid traffic will convert worse if it smells fake. Do not add:

- Countdown timers before checkout.
- Random stock counters.
- "الأكثر مبيعًا" unless real order data is later wired.
- Influencer photos or UGC screenshots unless the media file and permission are provided.
- Certificates, lab badges, or compliance logos unless the certificate file exists in the repo.

Use the trust we can prove: COD, confirmation call, return window, clear specs, Saudi Arabic, and one focused brand.

## Analytics checks after launch

The coder should leave enough event structure so the marketer can inspect:

- PDP view to AddToCart by product.
- AddToCart to checkout modal open.
- Checkout form valid to upsell shown.
- Upsell accept rate.
- Order success rate.
- Main unit count distribution: 1, 2, 3, 4+.
- Pixel vs CAPI dedup health in each platform.

Do not add a third-party analytics package in MVP unless requested. The ad platforms, database rows, and sheet are enough for launch.
