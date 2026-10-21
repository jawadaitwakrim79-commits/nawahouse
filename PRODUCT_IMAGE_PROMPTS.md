# Nawa House — Gemini Image Prompts

**Usage**: upload the raw Alibaba product image to Gemini (or Nano Banana / Imagen),
paste the prompt below as the instruction. One prompt per product.

**Shared style directives (apply to all three)**:
- Clean editorial product shot, white seamless cycloramic background.
- Soft, directional daylight from upper-left; subtle contact shadow beneath the product.
- Composition centered, 1:1 aspect ratio (works for both collection grid and PDP).
- Palette: creamy ivory, warm paper, deep olive accent, muted brass.
  **No pink, no bright primary colors, no neon, no gradient backgrounds.**
- Premium catalog aesthetic (Aesop / Byredo / Diptyque reference quality).
- **Remove every logo, OEM mark, Chinese text, barcode, or supplier name from the device itself.**
  The device surface must be clean — no branding visible.
- Keep the product's real geometry, materials, buttons, and proportions intact.
  Do not invent features that aren't in the source photo.

---

## 1. نوا عود — Electric Oud Bakhoor Burner

> **Prompt for Gemini (paste as-is):**

```
Editorial product photograph of the electric oud bakhoor burner shown in the
reference image, on a seamless warm-ivory background (#F3EDE4). Keep the device's
exact shape, lid, buttons, charging port, and material. REMOVE any brand name,
OEM logo, Chinese characters, or printed text from the device body — the surface
must be completely clean and unbranded.

Styling props arranged beside the burner on the surface:
- 2–3 raw oud wood chips (dark reddish-brown Cambodian oud, irregular organic
  shape, visible wood grain)
- A small shallow brass dish holding one oud chip
- A single wisp of soft, barely-visible aromatic smoke rising from the device
- Optional: a folded cream linen napkin at the edge of the frame for texture

Lighting: soft daylight from upper-left, gentle contact shadow underneath, warm
color temperature (3800K). The device is the hero — props sit lower and smaller
in the composition.

Mood: calm, considered, apothecary-grade. Think a Saudi majlis the hour before
guests arrive. No clutter, no excessive props, no decorative Arabic calligraphy
in the frame.

Final look: premium catalog, 1:1 square, high resolution, sharp focus on the
device, slight depth-of-field blur on background props. Suitable for a luxury
home-fragrance brand's collection page.
```

**Why this works**: oud chips are the native "ingredient" (not fruit). The brass
dish ties into the Nawa House brass accent color. The wisp of smoke is the only
subtle "lifestyle" element — otherwise pure product.

---

## 2. نوا شفق — Sunset Projection Lamp

> **Prompt for Gemini (paste as-is):**

```
Editorial product photograph of the sunset projection lamp shown in the
reference image, on a seamless warm-ivory background (#F3EDE4), transitioning
very subtly to a soft peach-amber glow on the upper portion of the wall (as if
the lamp itself is softly projecting). Keep the device's exact shape, cylindrical
body, lens, base, cables, and control buttons intact. REMOVE any brand name, OEM
logo, model number, Chinese text, or supplier marks from the device — surface
must be clean and unbranded.

Styling props beside the lamp:
- A folded cream-colored linen throw or blanket at the edge of the frame
- A small ceramic coffee cup in matte olive-green (#2C3A2E)
- Optional: a closed hardcover book with a plain muted linen cover
- A single dried pampas-grass stem leaning out of the frame (soft texture)

Lighting: the primary device is lit cleanly from the upper-left with soft
daylight, so its physical form reads clearly. A secondary warm amber glow washes
subtly over the background from the lamp's output direction, suggesting the
sunset effect without overwhelming the shot.

Mood: Riyadh evening, 7 PM, a woman's bedroom after a long day. Calm, warm,
cinematic. No bright colors, no RGB rainbow, no busy backgrounds.

Final look: premium catalog, 1:1 square, high resolution, sharp focus on the
device, soft bokeh on the far background wall glow. The lamp should feel like
an object of design, not a tech gadget.
```

**Why this works**: the subtle amber wash shows what the product *does* without
turning it into a party gadget. Olive cup + brass tones = Nawa House palette.

---

## 3. نوا صفاء — HEPA-13 Air Purifier

> **Prompt for Gemini (paste as-is):**

```
Editorial product photograph of the HEPA-13 air purifier shown in the reference
image, on a seamless warm-paper background (#FBF7F2). Keep the device's exact
tower shape, air inlets, control panel, display, and dimensions intact. REMOVE
any brand name, OEM logo, model number, Chinese text, or supplier watermarks
from the device body — the surface must be completely clean and unbranded.

Styling props arranged beside the purifier:
- One small sprig of fresh green eucalyptus leaves on the surface near the base
- A single clear glass carafe of water with a slim neck
- A small flat ceramic dish (matte warm sand color, #E7DCCC) holding a few
  loose dried lavender stems
- Optional: a thin brass-rimmed round tray underneath the arrangement for
  grounding

Lighting: bright, clean, slightly cooler than the oud/lamp shots (4500K) to
convey "fresh air" and clinical cleanliness without feeling cold. Soft daylight
from upper-left, crisp contact shadow, no harsh highlights.

Mood: clean modern Saudi apartment, morning light after cleaning, air feels
weightless. Apothecary-clean, pharmaceutical precision — but warm, not sterile.
No lab imagery, no doctors, no medical crosses, no clouds/mist.

Final look: premium catalog, 1:1 square, high resolution, sharp focus on the
device, props sit lower in the frame to let the purifier dominate. Suitable
for a brand that competes on honesty: this is a filter, not a cure.
```

**Why this works**: eucalyptus + lavender + glass of water = "clean air" and
"botanical" signals — honest to the product (which has a *perfume slot*, not a
medical claim). The slightly cooler light + brass tray = apothecary-pharmacy
feel without crossing into medical device.

---

## Post-generation checklist (before putting the image on the site)

Before replacing `/public/images/products/{oud,shafaq,safa}-1.webp`, verify:

- [ ] No supplier/OEM text or logos remain visible on the device.
- [ ] No Chinese characters, barcodes, model stickers, or QR codes present.
- [ ] Background is clean warm ivory/paper — no gradient, no color spill.
- [ ] Props don't crowd the device (device = ~60% of the vertical frame).
- [ ] Image is 1200x1200 minimum, exported as WebP, quality ~85.
- [ ] Each of the 4 slots (`-1`, `-2`, `-3`, `-4.webp`) gets a different
      angle/crop of the same prompt (front hero, 3/4, detail, lifestyle).

## Prop list — quick reference by product

| Product | Props (shared palette: ivory + olive + brass) |
|---|---|
| نوا عود | 2–3 raw oud chips · brass dish · optional single wisp of smoke · cream linen |
| نوا شفق | folded cream linen · olive ceramic cup · plain hardcover book · one pampas stem · subtle amber wall glow |
| نوا صفاء | eucalyptus sprig · glass water carafe · ceramic dish with lavender · optional brass tray |
