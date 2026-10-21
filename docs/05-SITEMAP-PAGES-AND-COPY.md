# Sitemap, Pages, and Copy

Paste this copy. Do not rewrite the tone. Prices in sentences use Arabic-Indic digits. Form fields and order IDs use Western digits.

Global chrome is on every page except the thank-you page hides the announcement ticker so the confirmation instruction wins.

## Announcement bar

Rotates every 4 seconds. One line visible. Height fixed so it does not shift the header.

- شحن لكل مناطق المملكة
- الدفع عند الاستلام، بدون تحويل
- بنتصل نأكّد العنوان قبل الشحن

## Header

Right to left: logo lockup, then nav, then the cart on the far left.

Nav:

- الرئيسية → `/`
- الطقوس → `/shop`
- نوا عود → `/products/oud`
- نوا شفق → `/products/shafaq`
- نوا صفاء → `/products/safa`
- حكاية نوا → `/about`
- تواصلي → `/contact`

Mobile: logo centered, menu button on the right, cart on the left. The menu is a full-height panel with the same links plus the policy links.

Cart icon shows the count of main units plus the upsell unit if one is in the cart. Click opens the drawer. Never navigate to `/cart`. There is no `/cart` route.

## Footer

Four columns on desktop, accordion on mobile.

| الطقوس | نوا | المساعدة | تواصلي |
|---|---|---|---|
| نوا عود | حكاية نوا | الشحن | رقم الجوال من الإعدادات |
| نوا شفق | الطقوس الثلاث | الترجيع | الإيميل من الإعدادات |
| نوا صفاء | الأسئلة | الخصوصية | ساعات العمل: ٤ عصرًا – ١١ مساءً |
| كل الطقوس |  | الشروط | الرياض |

Bottom line: `© 2026 نوا للبيت · Nawa House · الدفع عند الاستلام`

No fake payment logos. One text badge: الدفع عند الاستلام. No SASO mark.

Phone and email come from `NEXT_PUBLIC_CONTACT_PHONE` and `NEXT_PUBLIC_CONTACT_EMAIL`. If empty, hide that line. Do not invent a number.

## Homepage `/`

Goal in one screen: she understands this is a Saudi house brand with three rituals, and she can see the first product.

### 1. Hero

Desktop: text column on the right, image on the left. Image file `public/images/hero-majlis.webp`.

Eyebrow: طقوس البيت

Headline: خلي بيتك يستقبلكِ

Sub: ثلاث قطع ضد ثلاثة أشياء: ريحة باهتة، جو ممل، وغبار يخنق الغرفة.

CTA: شوفي الطقوس الثلاث → `#rituals`

Second line under the CTA, small: الدفع عند الاستلام · بنتصل قبل الشحن

### 2. The three enemies `#rituals`

Title: ما نبيع أجهزة. نكمّل البيت.

Three cards, linking to the PDPs:

| | نوا عود | نوا شفق | نوا صفاء |
|---|---|---|---|
| Enemy | ضد رائحة البيت الباهتة | ضد جو الغرفة الممل | ضد غبار الرياض وكتمة البيت |
| Line | عود كمبودي بحرارة الجهاز، بلا فحم | ضوء شفق على السقف بدل اللمبة البيضاء | فلتر HEPA-13 للغبار، والعطر في خانة وحده |
| Price | ١٩٩ ر.س | ١٩٩ ر.س | ١٩٩ ر.س |
| CTA | تعرّفي على نوا عود | تعرّفي على نوا شفق | تعرّفي على نوا صفاء |

### 3. Product cards

Same component as the shop. Spec below.

### 4. Alternating stories

Three bands. Odd bands: text right, image left. Even bands: image right, text left. On mobile every band is text then image.

Band A, image `public/images/story-oud.webp`

- Title: الريحة أول ما يفتح الباب
- Body: المجلس يكون مرتب، والريحة واقفة. الفحم يدخّن أكثر مما يطيّب. نوا عود يدفّي قطعة العود الكمبودي ويطلع الريحة بدون جمر.
- Link: طقس الاستقبال

Band B, image `public/images/story-shafaq.webp`

- Title: السهرة ما تحتاج لمبة أقوى
- Body: الضوء الأبيض يخلي الغرفة مثل أي غرفة. نوا شفق يفرش مشهد الشفق على السقف، والجو يتغير قبل ما يجي أحد.
- Link: طقس السهرة

Band C, image `public/images/story-safa.webp`

- Title: الغبار يرجع حتى بعد ما تمسحين
- Body: في الرياض الغبرة خفيفة وتعلق. المعطّر يغطي الكتمة وما يمسك الغبار. نوا صفاء يمرّر الهواء على فلتر HEPA-13، وإذا تبين ريحة فهي في خانة ثانية.
- Link: طقس الهواء

### 5. Ladder

Title: سعر الطقس، مو سعر الخصم

Three columns:

- قطعة واحدة — ١٩٩ ر.س
- قطعتان — ٢٧٩ ر.س — marker: الأنسب للبيت
- ثلاث قطع — ٣٤٩ ر.س

Sub: كلما اكتمل البيت، صار السعر سعر طقس. ما فيه كود، وما فيه نسبة.

CTA: ابدئي من الطقوس → `/shop`

### 6. Trust

Four items, no logos we do not own:

- الدفع عند الباب
- مكالمة تأكيد قبل الشحن
- ٣٠ يوم ترجيع إذا القطعة سليمة وكاملة
- فلتر بفئة H13 حسب EN 1822، على نوا صفاء فقط

### 7. Voices

Title: من البيوت

Render the three sample lines from [03-PRODUCTS-AND-SCIENCE.md](03-PRODUCTS-AND-SCIENCE.md). Stars on the quote, no number beside them, no badge.

### 8. FAQ

- كيف أدفع؟ عند الاستلام. ما فيه تحويل ولا بطاقة.
- ليش بتكلموني؟ عشان نأكد الحي والعنوان، والطلب ما يطلع إلا بعد ما تردين.
- كم يوصل؟ بعد التأكيد، عادة من يومين إلى خمسة أيام داخل المملكة.
- أقدر أرجع؟ خلال ٣٠ يوم إذا القطعة ما استُخدمت وكرتونها موجود.
- هل الأسعار فيها خصم؟ لا. ١٩٩ للقطعة، ٢٧٩ لقطعتين، ٣٤٩ لثلاث. المكان الوحيد اللي فيه سعر ٩٩ هو عرض ١٥ ثانية بعد ما تثبتين بياناتكِ.
- وين تشتغلون؟ نوصّل لكل مناطق المملكة.

### 9. Close

Title: ثلاث طقوس، وبيت أهدى

CTA: اختاري طقسكِ → `/shop`

## Shop `/shop`

Title: الطقوس الثلاث

Sub: كل قطعة ضد شيء واحد في البيت.

No filters that hide products. Three chips are anchors, not filters: الكل · الريحة · الضوء · الهواء. They scroll to the card.

Grid: 1 column mobile, 3 columns from 1024px.

Under the grid, repeat the ladder banner from the homepage.

## Product card

Used on home, shop, PDP cross-sell, cart cross-sell, thank-you.

```
image
نوا عود                          ← heading
ضد رائحة البيت الباهتة           ← subheading
★★★★★                            ← stars, no (127), no 4.9
١٩٩ ر.س
قطعة ١٩٩ · قطعتان ٢٧٩ · ثلاث ٣٤٩  ← quiet, not a sale badge
[ أضيفي للسلة ]                  ← adds quantity 1 and opens the drawer
[ التفاصيل ]
```

The star row has no count. Do not write "الأكثر مبيعًا" or "باقي ٣".

The PDP is where she chooses 1, 2, or 3. The card's primary button adds one unit so the drawer can teach the ladder. Label the button أضيفي للسلة.

## PDP

Route `/products/[slug]`. Blocks are in [03-PRODUCTS-AND-SCIENCE.md](03-PRODUCTS-AND-SCIENCE.md).

Hero, desktop: copy on the right, gallery on the left. Gallery has 4 sample images per product.

Offer picker under the price. Default: قطعتان. The selected tier uses a 2px brand border. Badge on the middle tier: الأنسب للبيت. That badge is our recommendation, not a sales statistic.

Sticky mobile bar after the hero scrolls away: name, selected price, button أضيفي الطقس للسلة.

CTA behavior: add the selected quantity of this slug, open the drawer, do not leave the page.

Gallery files:

- `public/images/products/oud-1.webp` through `oud-4.webp`
- `public/images/products/shafaq-1.webp` through `shafaq-4.webp`
- `public/images/products/safa-1.webp` through `safa-4.webp`

Image 1 is the product on a warm surface. Image 2 is the product in a majlis. Image 3 is a detail. Image 4 is the enemy contrast without being disgusting: a dull corner versus the ritual, split quietly, no red arrows, no English text baked into the picture.

## About `/about`

Title: ليش نوا للبيت

Paragraphs:

نوا للبيت طلعت من مجالس الرياض. البيت يكون نظيف، وبرضه الريحة باهتة، والضوء أبيض، والهواء ثقيل من الغبار.

ما بغينا متجر أجهزة. بغينا ثلاث طقوس، كل طقس ضد شيء واحد: نوا عود للاستقبال، نوا شفق للسهرة، ونوا صفاء للهواء.

ندفع عند الاستلام لأن الثقة تتبنى بالمكالمة وبالصندوق، مو بالجملة الكبيرة. وإذا القطعة ما ناسبتكِ وهي سليمة، ترجعينها خلال ٣٠ يوم.

Side image on the left: `public/images/about-room.webp`. Text on the right.

Do not add a portrait, a fake name of a founder, or a diploma.

## Contact `/contact`

Title: تواصلي

Body: الطلبات تتأكد بالمكالمة. إذا عندكِ سؤال قبلها، اكتبي لنا.

Show phone and email from env, and the hours. A form posts to `POST /api/contact`, which only stores a row and returns success. Fields: name, Saudi phone, message. This form does not create an order and does not fire Purchase.

No map embed required.

## Thank-you `/thank-you`

Copy is specified in [04-CRO-OFFERS-CHECKOUT.md](04-CRO-OFFERS-CHECKOUT.md). Add the order number in Latin digits: `NAW-1001`.

## Policies

Short pages, Arabic, linked from the footer. These are operational rules, not a law firm memo.

### `/policies/shipping`

نوصّل لكل مدن المملكة. الطلب ما يطلع للمندوب إلا بعد مكالمة التأكيد. بعد التأكيد، التوصيل غالبًا خلال ٢ إلى ٥ أيام عمل. الشحن داخل سعر الطلب، ما نضيف رسوم توصيل على السلة. إذا ما ردّيتي على ثلاث محاولات اتصال، الطلب يتوقف وما ينشحن.

### `/policies/returns`

٣٠ يوم من يوم الاستلام. القطعة ترجع غير مستخدمة، كاملة، مع الكرتون. ترجيع القطعة اللي انفتحت أو تستخدم فيها العود أو الفلتر ما ينقبل إلا إذا وصلت تالفة. تكلفة إرجاع القطعة السليمة على العميلة. إذا وصل عيب، نتحمل الإرجاع أو نبدل.

### `/policies/privacy`

نجمع الاسم ورقم الجوال عشان نتصل ونوصّل. الطلب ينحفظ عندنا ويترسل نسخة لجدول الطلبات. أحداث الإعلان (ميتا، تيك توك، سناب) تُرسل من المتصفح ومن السيرفر عشان القياس، ورقم الجوال في الإرسال للسيرفرات الإعلانية يكون مشفّرًا SHA-256 بعد التطبيع. ما نبيع البيانات. للاستفسار يُستخدم إيميل التواصل.

### `/policies/terms`

المتجر يبيع ثلاث منتجات بالدفع عند الاستلام داخل السعودية. إكمال النموذج يعني إنكِ تطلبين اتصال تأكيد، مو خصمًا من بطاقة. سعر السلة يحسبه النظام: ١٩٩، ٢٧٩، ٣٤٩، ثم ١٩٩ لكل قطعة بعد الثالثة. سعر ٩٩ يظهر مرة واحدة بعد التحقق من النموذج، لمدة ١٥ ثانية، وعلى قطعة واحدة. إلغاء الطلب يتم بالرد على المكالمة أو قبل التسليم.

## SEO

`lang="ar"` and `dir="rtl"` on `<html>`. Title pattern: `{page} · نوا للبيت`. Homepage title: `نوا للبيت · ريحة، ضوء، وهواء`. Meta description homepage: `ثلاث طقوس للبيت السعودي: عود بلا فحم، شفق للغرفة، ومنقّي HEPA-13. الدفع عند الاستلام.`

Canonical host: `https://nawahouse.shop`.
