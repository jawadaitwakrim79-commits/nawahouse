# Design System

## Feel

A Riyadh evening, not a clinic and not a marketplace. Warm paper, oud brown, a little twilight. Lots of margin. One brand color used rarely: the N circle, links on hover, the selected offer, the active ladder tier.

## Color

| Token | Hex | Use |
|---|---|---|
| `paper` | `#FBF7F2` | Page background |
| `ivory` | `#F3EDE4` | Cards, header when scrolled |
| `sand` | `#E7D9CC` | Hairlines, quiet fills |
| `ink` | `#1C1612` | Text |
| `muted` | `#8A7568` | Secondary text |
| `brand` | `#8C4A32` | The N circle, selected border, one underline |
| `brand-deep` | `#5C3424` | Button fill |
| `on-brand` | `#F3EDE4` | Text on brand-deep buttons |
| `twilight` | `#243044` | شفق sections only, as a deep band |
| `line` | `#E4D8CC` | Borders |

Buttons are `brand-deep` with ivory text. Not red. Not a gradient. Radius 999px for buttons, 20px for cards.

Do not use pure black or pure white.

## Type

Load with `next/font`:

- Amiri — wordmark and H1 only
- IBM Plex Sans Arabic — everything else in Arabic
- Outfit — the English line "Nawa House" and order IDs

H1 around 40px mobile / 64px desktop, tight line height, Amiri. Body 17px, line height 1.7. Never justify Arabic text. Align start.

## Logo

Inline SVG component `Logo`. Circle 36px mobile / 44px desktop, fill `#8C4A32`. The letter N is Outfit 600, fill `#F3EDE4`, centered. To the left of the circle in screen space (beside it, toward the center of the header), the two-line wordmark:

- نوا للبيت — Amiri 22px / 28px
- Nawa House — Outfit 11px, tracking 0.12em, color `muted`

The lockup is a link to `/`.

## Header behavior

Sticky. Transparent over the hero for the first 20px of scroll, then `ivory` with a bottom hairline. Height 64px mobile, 80px desktop. The announcement bar is above it and not sticky.

## Layout rhythm

Page gutter 20px mobile, 48px desktop, max content width 1120px.

Alternating media sections, desktop:

- Odd section: first column in the DOM is the text. In RTL it sits on the right. Image on the left.
- Even section: first column is the image, so the image sits on the right and the text on the left.

Implement with CSS grid, two columns, `gap: 48px`, and `direction: rtl` inherited. Do not use `order` hacks unless a breakpoint needs them. Mobile: one column, and the DOM order for mobile must be text then image. Use two DOM orders via grid areas:

```css
.band { display: grid; gap: 24px; }
.band .copy { grid-area: copy; }
.band .media { grid-area: media; }
.band { grid-template-areas: "copy" "media"; }
@media (min-width: 1024px) {
  .band { grid-template-columns: 1fr 1fr; grid-template-areas: "media copy"; }
  .band.flip { grid-template-areas: "copy media"; }
}
```

Because the page is RTL, `media copy` places copy on the right. `.flip` places copy on the left. First story band is not flipped. Second is flipped. Third is not.

## Product card and gallery

Image ratio 4 / 5. `object-fit: cover`. Background `sand` while loading. No price badge overlapping the photo.

## Motion

Almost none. The drawer and modal transition 200ms. Respect `prefers-reduced-motion`. No parallax. No countdown animation except the upsell number changing once per second.

## Breakpoints

Build mobile first. Check 390, 768, and 1280. Touch targets at least 44px. The sticky PDP bar must not cover the footer links; hide it when the footer is on screen.

## Sample images

Generate photographic samples, WebP, no words in the image, no watermark, no logo. A Saudi home at dusk: warm plaster, low seating, wood, cream textiles. Women, if shown, are modest and not the subject; prefer the room. No European loft, no neon, no medical lab.

| File | What |
|---|---|
| `frontend/public/images/hero-majlis.webp` | Wide evening majlis, empty of faces, a low table, warm light. 1600×1200. |
| `frontend/public/images/story-oud.webp` | A small dark burner and a piece of oud on a brass tray, smoke absent. 1200×1500. |
| `frontend/public/images/story-shafaq.webp` | Ceiling washed with dusk pink and amber, the projector barely in frame. 1200×1500. |
| `frontend/public/images/story-safa.webp` | A quiet purifier in a bright dusty-beige Riyadh living room, window light. 1200×1500. |
| `frontend/public/images/about-room.webp` | Corner of the same house, evening. 1200×1500. |
| `frontend/public/images/products/{oud,shafaq,safa}-{1,2,3,4}.webp` | As named in the sitemap doc. 1200×1500. |

These are stand-ins. Real photography replaces the files later without changing components. Do not hotlink external images.

## Accessibility

Focus rings in `brand`. Form errors are text, not color alone. The countdown is text. Modal has `aria-modal` and returns focus to the cart button on close.
