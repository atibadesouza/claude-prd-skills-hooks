---
name: image-slot
category: feature
dial_compatibility:
  variance: [1, 10]
  motion: [1, 10]
  density: [1, 10]
when_to_use: "Anywhere a real photograph belongs but may not exist yet - portraits, hands-on shots, venue/product photography. Renders the real image when supplied and an honest, clearly-labelled placeholder when not."
not_for: "Decorative or abstract imagery that has no 'real' version to wait for. Icons. Logos. If a generated or stock image is genuinely acceptable for the slot, this block is the wrong tool - it exists precisely to refuse that."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/PortraitPlaceholder.tsx", "colinrigney-site/components/PhotoSlot.tsx"]
---

# Image Slot

One component, two states: the real photograph, or an honest placeholder that says what is missing.

Both harvest sources wrote the same rule into a comment at the top of the file, independently:
**real likeness only, never AI-generated.** This block is how that rule survives contact with a
site that is not finished yet.

## 1. Visual sketch

```
  src supplied                    src absent
┌──────────────┐                ┌──────────────┐
│              │                │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  brand texture, CSS only
│  real photo  │                │      ▢       │  icon
│  object-cover│                │ [NEEDS] PHOTO│  unambiguous marker
│              │                │ who/what it  │  the label says what belongs here
└──────────────┘                └──────────────┘
   same box, same aspect ratio, same rounding - the layout does not move
```

The two states occupy identical space. Dropping the real photo in later must not reflow the page.

## 2. Props API

```ts
type ImageSlotProps = {
  label: string;        // doubles as alt text when real, and as the brief when placeholder
  src?: string;         // real, owner-supplied photo. absent => placeholder.
  ratio?: string;       // "3 / 4" | "4 / 5" | "16 / 9"
  priority?: boolean;   // true when this is the LCP image
  tone?: "ink" | "paper";
  className?: string;
};
```

**`label` doing double duty is the load-bearing decision.** It is the alt text when the photo is
real and the description of what is missing when it is not, so the slot can never exist without
someone having said what belongs in it. A separate optional `alt` would be left empty.

## 3. Code sketch

Server Component. No JS.

```tsx
import Image from "next/image";

export function ImageSlot({ label, src, ratio = "3 / 4", priority = false, className = "" }) {
  const box = `relative w-full overflow-hidden rounded-[--radius] border border-line ${className}`;

  if (src) {
    return (
      <div className={box} style={{ aspectRatio: ratio }}>
        <Image src={src} alt={label} fill priority={priority}
               sizes="(max-width: 1024px) 100vw, 42vw" className="object-cover" />
      </div>
    );
  }

  return (
    <div className={box} style={{ aspectRatio: ratio }} data-image-slot="placeholder">
      {/* brand texture - CSS only, never a generated likeness */}
      <div className="absolute inset-0 opacity-50 [background:var(--slot-texture)]" aria-hidden />
      <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 p-6 text-center">
        <span aria-hidden className="flex h-11 w-11 items-center justify-center
                                     rounded-full border border-line text-faint">
          <CameraIcon size={20} />
        </span>
        <span className="text-[0.72rem] font-medium uppercase tracking-[0.12em] text-faint">
          [NEEDS] real photo
        </span>
        <span className="max-w-[24ch] text-[0.74rem] leading-snug text-muted">{label}</span>
      </div>
    </div>
  );
}
```

`sizes="(max-width: 1024px) 100vw, 42vw"` is copied verbatim from both sources, which chose it
independently — it matches the near-half-width column this block usually sits in.

`priority` must be `true` for a hero portrait and `false` everywhere else. Every image marked
priority competes to be the LCP; marking several is the same as marking none.

## 4. Mobile fallback (`< 768px`)

- The box goes full-width and keeps its aspect ratio, so height follows from width. Never set a
  fixed pixel height — that is what causes the layout to jump when the real photo lands.
- Cap it: `max-w-[26rem] mx-auto`. A portrait at full 375px width becomes a 500px-tall slab that
  pushes everything below it off screen.
- The placeholder's three text lines stay legible: keep the label to ~24 characters per line and
  let it wrap. Do not shrink it below 11px to fit.
- Consider `4 / 5` instead of `3 / 4` on mobile — shorter, less scroll cost.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. |
| 4-7 | Fade + scale from `0.97` over ~1s on entry, delayed slightly behind the text beside it. |
| 8-10 | As 4-7. Do not parallax the image inside the box, and do not animate the placeholder — an animated placeholder reads as a real loading state and implies the photo is coming. |

Reduced motion: render at final state. The box must never animate its *size* — the reserved
space is the whole point.

## 6. Dark-mode notes

The `tone` prop exists because this block sits on both surfaces and its texture is not a token —
it is authored art. One source carries an ink and a paper gradient as two separate hand-written
backgrounds rather than one tinted value, which is the right call: a warm-cream texture darkened
programmatically reads as mud.

Per-mode values needed: the texture background, the border/ring colour (`ring-white/10` on ink,
`ring-black/10` on paper), and the placeholder's faint text, which is the most likely thing to
fall below WCAG AA in one of the two modes.

When a real photo renders, add the inset ring in both modes — it keeps a light photo from
bleeding into a light surface with no edge.

## 7. Anti-patterns

- **A generated or stock face.** The rule both sources wrote down. On an authority page a stock
  portrait inverts the purpose of the photograph.
- **A placeholder that looks like a real image.** A grey rectangle reads as a slow-loading photo.
  The `[NEEDS]` marker is not decoration — it is what stops a placeholder shipping unnoticed.
- **No reserved space** — omitting `aspectRatio` and letting the image define its own height
  causes a layout shift on load and wrecks CLS.
- **`priority` on every slot.** See section 3.
- **Empty `alt`, or `alt="portrait"`.** The `label` is the alt for a reason.
- **A hand-rolled decorative SVG icon.** One source inlines its own camera path; the other uses
  Phosphor. The checklist bans hand-rolled decorative SVGs and names the allowed icon sets, so
  the Phosphor version is the one to copy.
- **Removing the placeholder branch once the real photo exists.** Keep it — the next page needs it,
  and a slot that silently renders nothing when `src` is undefined is how a hole ships.
- **Text baked into the image.** It cannot be translated, selected, or read by a screen reader.

## 8. References

- `arianademers-site/src/components/PortraitPlaceholder.tsx` — radial gradient + diagonal hatch
  texture, `tone` prop for ink/paper, Phosphor `CameraIcon`, inset ring in both states.
- `colinrigney-site/components/PhotoSlot.tsx` — blueprint-grid texture, mono type, bordered box,
  `data-photo-slot` hook for tests, hand-rolled inline SVG (see anti-patterns).

Independently agreed: the `src`-present / `src`-absent branch, `aspectRatio` on a wrapper with
`overflow-hidden`, `fill` + `object-cover`, the identical `sizes` string, `priority` as a prop,
the label-as-alt decision, and a `[NEEDS…]` marker in the placeholder.
