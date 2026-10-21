# Products and Science

Three products. Same ladder price. No fourth SKU in the MVP. Seed them with these slugs. Routes are `/products/oud`, `/products/shafaq`, `/products/safa`.

## Catalog

### نوا عود · slug `oud`

- Full name: مبخرة عود كمبودي ذكية
- Enemy: رائحة البيت الباهتة
- Ritual: طقس الاستقبال
- One line: تطلّع ريحة العود الكمبودي بدون فحم وبدون ما تحرق القطعة.
- Card heading: نوا عود
- Card subheading: ضد رائحة البيت الباهتة
- What she buys: an electric bakhoor burner made to warm Cambodian oud, not a charcoal pan and not a plug-in oil.

### نوا شفق · slug `shafaq`

- Full name: بروجكتر شفق سينمائي
- Enemy: جو الغرفة الممل
- Ritual: طقس السهرة
- One line: يفرش ضوء الشفق على السقف ويغيّر جو الغرفة من لمبة بيضاء.
- Card heading: نوا شفق
- Card subheading: ضد جو الغرفة الممل
- What she buys: a twilight projector for the ceiling and wall. Mood and scene, not a TV and not a kids' galaxy toy in the copy.

### نوا صفاء · slug `safa`

- Full name: منقّي هواء HEPA-13 بالعطر
- Enemy: غبار الرياض وكتمة البيت
- Ritual: طقس الهواء
- One line: فلتر HEPA-13 يمسك غبار الرياض، والعطر يجي في خانة وحده.
- Card heading: نوا صفاء
- Card subheading: ضد غبار الرياض وكتمة البيت
- What she buys: a purifier whose dust job is the filter, plus a separate scent. Never describe the perfume as the thing that cleans the air.

## How to use them everywhere

The same three names appear in the header menu, the home grid, the shop, the cart, the upsell, the footer, and the sheet. Do not translate them differently per page. Do not add shade names or bundles as new products. A "pack of 2" is a quantity of one slug, not a new slug.

## Claims gate

Ship a sentence only if its row says Ship. Rows marked Sheet wait for a supplier spec file dropped in `frontend/content/specs/` later. Until that file exists, use the safe line in the last column. Forbidden lines never ship.

| Claim | Status | Safe line if the spec sheet is missing |
|---|---|---|
| Electric heat instead of charcoal, so the oud is warmed rather than burned | Ship | تطلع الريحة بحرارة الجهاز، مو على جمر. |
| A precise °C such as 190 | Sheet | Do not print a number. |
| "Cambodian oud included in the box" | Sheet | Say مبخرة للعود الكمبودي. Do not claim a gift wood chip unless it is in the box. |
| Timer steps (1h / 3h / 6h) | Sheet | Say استخدام هادي للمجلس. Do not invent durations. |
| HEPA-13 / H13, EN 1822, at least 99.95% at the most penetrating particle size | Ship only as a class statement | الفلتر من فئة HEPA-13 (H13): المعيار الأوروبي EN 1822 يطلب التقاط 99.95٪ على الأقل عند أصعب حجم جسيم. |
| "Removes viruses, treats asthma, medical grade air" | Forbidden | — |
| "SASO approved" badge | Forbidden until a PDF is in the repo | Hide the badge component. |
| Scent capsule is separate from the filter | Ship | الغبار يمسكه الفلتر. العطر خانة ثانية، ما يغطي على الغبار. |
| Projector is dimmable / warm | Sheet | ضوء شفق دافي، مو إضاءة بيضاء قاسية. |
| Helps sleep, treats insomnia, circadian therapy | Forbidden | — |
| Stars, review counts, "verified purchase" | Forbidden until a row in the sheet is a real delivered order | Quotes may render as brand lines with no count and no badge. |

H13 note for copy writers: HEPA class H13 in EN 1822 means a minimum efficiency of 99.95% at the most penetrating particle size, which sits around 0.1 to 0.3 micrometres. Do not write "kills". Write "يمسك" / "يلتقط".

Riyadh dust note: the city is dusty (construction, dry wind, fine indoor dust). Do not attach a fake PM2.5 statistic. The enemy line "غبار الرياض" is enough.

Oud note: Cambodian agarwood is a real trade origin. Charcoal burns the chip and fills the room with smoke. A heated chamber is the honest contrast. Do not name a lab, a grade of oud, or a region inside Cambodia.

Projector note: sell atmosphere. A dim warm scene on the ceiling changes a boring white room. Do not promise cinema resolution, lumens, or a brand of lamp unless the spec sheet has the number.

## PDP blocks, same skeleton, different words

Use this order on every product page. Alternate media side each block, starting with copy on the right.

1. Hero. Name, enemy subheading, price 199 ر.س, offer picker, CTA, COD / call / 30-day row.
2. The enemy, full width, one sharp sentence and a short paragraph.
3. Three proof points. Only claims from the Ship column, or the safe line.
4. Materials table. Columns: الشيء · وش يسوي · ليش يهم بيتكِ. Unknown cells say «يتأكد مع مواصفات القطعة» rather than a invented material.
5. The ritual, four short steps.
6. The other two products, at 199 ر.س, no bundle math on the card.
7. FAQ, six questions.
8. Final CTA repeating the offer picker.

### نوا عود — proof points

- بدون فحم. الريحة تطلع والدخان ما يخنق المجلس.
- حرارة الجهاز تشتغل على القطعة، ما تحرقها على جمر.
- للمجلس ولحظة الدخول، مو عطر حمام قوي.

Ritual steps:

1. حطّي قطعة العود في المكان المخصص.
2. شغّلي الجهاز واتركيه يدفّي.
3. أغلقي الباب دقايق عشان الريحة تهدأ في المجلس.
4. استقبلي ضيوفكِ، أو اجلسي أنتِ أول وحدة.

FAQ seeds:

- هل تحتاج فحم؟ لا.
- هل الريحة تبقى في الستارة؟ العود يعلق أخف من الفحم، والتهوية بعد المجلس تخففه.
- هل ينفع لشقة؟ نعم، لأنه ما فيه جمر.
- وش أحط فيه؟ عود. لا حطّي بخور مجهول أو زيت في مكان القطعة إلا إذا مواصفات الجهاز قالت ذلك.
- الدفع؟ عند الاستلام، ونتصل نأكّد العنوان.
- إذا ما عجبتني؟ ٣٠ يوم والقطعة سليمة.

### نوا شفق — proof points

- يغيّر السقف والجدار، فالغرفة ما تبقى لمبة وحدة.
- الضوء دافي، مناسب للسهرة مو لشغل الظهر.
- هادي. الجو يجي من المشهد، مو من صوت جهاز.

Ritual steps:

1. حطّيه مقابل السقف أو الجدار الفاضي.
2. طفّي اللمبة البيضاء.
3. اختاري مشهد الشفق الأهدى.
4. اجلسي. الغرفة صارت غير.

FAQ seeds:

- هل هو تلفزيون؟ لا. مشهد ضوئي للغرفة.
- هل ينفع في غرفة نوم؟ نعم، على مشهد هادي، ويبعد عن العين مباشرة.
- هل يأثر على النوم؟ ما نعد بعلاج. هو جو مساء، والغرف اللي تبي ضوء شغل تخليه مطفّي.
- الصوت؟ المطلوب جهاز هادي. إذا المواصفات فيها ديسيبل، نكتب الرقم من ورقة المصنّع فقط.
- مع العود؟ هذا أقوى استخدام: ريحة وضوء مع بعض.
- الضمان في الكلام؟ ٣٠ يوم ترجيع إذا القطعة كاملة.

### نوا صفاء — proof points

- فلتر HEPA-13 يمسك الغبار الناعم اللي تلمّينه كل يوم.
- العطر منفصل. ما نقول إن الريحة هي اللي تنقّي.
- لبيت الرياض: غبرة وكتمة، مو ادعاء طبّي.

Ritual steps:

1. شغّليه في المجلس أو غرفة الجلوس، مو مخبّى في الممر.
2. خلّي الباب والشباك على وضعكِ المعتاد، والجهاز يشتغل بهدوء.
3. إذا تبين ريحة، حطّي العطر في خانته، مو على الفلتر.
4. نظّفي أو بدّلي الفلتر لما المؤشر أو المدة في كرت الجهاز تقول ذلك.

FAQ seeds:

- هل يغني عن التكييف؟ لا. يمسك الغبار في هواء الغرفة.
- هل يعالج الحساسية أو الربو؟ لا. إذا عندها حالة، تسأل طبيبتها. إحنا نبيع فلتر وغبار.
- وش معنى HEPA-13؟ فئة H13 في EN 1822: التقاط 99.95٪ على الأقل عند أصعب حجم جسيم.
- العطر إجباري؟ لا. الفلتر يشتغل بدونه.
- صوت؟ نكتب الرقم فقط إذا موجود في ورقة الجهاز.
- الأطفال والحيوانات؟ الجهاز الكهربائي ينحط في مكان ثابت وما ينغطّى.

## Materials tables (honest blanks)

### نوا عود

| الشيء | وش يسوي | ليش يهم بيتكِ |
|---|---|---|
| حجرة التسخين | تدفّي قطعة العود بدل الجمر | ريحة أنظف ومجلس بلا دخان فحم |
| الجسم الخارجي | يعزل الحرارة عن اليد | استخدام هادي قدام الضيوف |
| مكان القطعة | يثبت العود داخل الجهاز | ما ينسكب على الطاولة |
| الخامة الدقيقة والموديل | من كرت المواصفات | ما نختلق رقم |

### نوا شفق

| الشيء | وش يسوي | ليش يهم بيتكِ |
|---|---|---|
| وحدة الإسقاط | ترسم مشهد الشفق على سطح الغرفة | السقف ما يبقى فاضي |
| عدسة / غطاء | يوزّع الضوء بدالى بقعة حادة | الجو يعم الغرفة |
| إضاءة دافية | تبعد عن الأبيض القاسي | السهرة تصير ألين |
| اللومن والواط | من كرت المواصفات | ما نختلق رقم |

### نوا صفاء

| الشيء | وش يسوي | ليش يهم بيتكِ |
|---|---|---|
| فلتر HEPA-13 (H13) | يمسك الجسيمات الدقيقة حسب EN 1822 | غبار الرياض ما يبقى في الهواء |
| مدخل الهواء ومخرجه | يحرّك هواء الغرفة عبر الفلتر | الكتمة تخف لأن الهواء يتحرك ويتصفّى |
| خانة العطر | ريحة خفيفة بعد التنقية | ما نخلط العطر بوظيفة الفلتر |
| مؤشر الفلتر إن وجد | يقول متى يتغير | الأداء ما يموت بصمت |

## Sample reviews

Do not ship these as verified purchases. There is no badge and no `(127)`. They exist so layout and tone are real. Component prop `verified` stays `false`.

- «المجلس كان نظيف وريحته واقفة. العود على الجهاز غير الفحم.» — نورة، الرياض
- «طفيت اللمبة وحطيت الشفق. الغرفة صارت سهرة.» — منى، جدة
- «الغبرة ترجع بعد الظهر. الجهاز ما سوّى معجزة، بس الطاولة ما تعبّي مثل أول.» — أمل، الرياض

## Cross-sell pairs

| If she is on | Suggest first |
|---|---|
| oud | shafaq, then safa |
| shafaq | oud, then safa |
| safa | oud, then shafaq |

Upsell priority when the form is valid: first missing product in order oud → shafaq → safa. If all three are already in the cart, upsell one extra unit of `oud` with the line «نسخة ثانية لمجلس ثاني», still at 99 SAR, still a single unit, still excluded from the 199/279/349 count.
