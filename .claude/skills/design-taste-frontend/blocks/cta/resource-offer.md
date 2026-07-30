---
name: resource-offer
category: cta
dial_compatibility:
  variance: [4, 9]
  motion: [1, 7]
  density: [3, 6]
when_to_use: "The lead magnet section - a guide, playbook, checklist or field guide offered in exchange for an email. The one place on the page where a deliberate inverted colour band is justified."
not_for: "Paid-product CTAs (pricing is a different block). A second lead magnet on the same page - one offer per page, or neither converts."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/ResourceCTA.tsx", "colinrigney-site/components/Resource.tsx"]
---

# Resource Offer

The free thing, what is inside it, and the ask — on the page's one inverted band.

## 1. Visual sketch

```
┌─ inverted band / card ─────────────────────────────────────────┐
│  EYEBROW: Free resource                                        │
│                                    ┌────────────────────────┐  │
│  The Asset's Actual Name           │                        │  │
│                                    │  cover mockup          │  │
│  One paragraph, <= 48ch, saying    │       OR               │  │
│  who it is for and what it does.   │  the capture form      │  │
│                                    │                        │  │
│  INSIDE THE GUIDE                  └────────────────────────┘  │
│  ✓ specific thing one                                          │
│  ✓ specific thing two                                          │
│  ✓ specific thing three                                        │
│                                                                │
│  [ Get the guide ]   no spam, ever.                            │
└────────────────────────────────────────────────────────────────┘
```

## 2. Props API

```ts
type ResourceOfferProps = {
  eyebrow?: string;                  // "Free resource"
  title: string;                     // the asset's real name, not "Free Guide"
  support: string;                   // <= 48ch measure
  inside: string[];                  // exactly 3. see anti-patterns.
  cta: { href: string; label: string } | { form: React.ReactNode };
  reassurance?: string;              // "No spam, ever." / "In production."
  pending?: string;                  // visible [NEEDS] marker while the asset is unfinished
};
```

`cta` is a union on purpose: the offer either **links** to a capture page or **embeds** the form
directly. Both sources ship one of each. Making it a union stops a page shipping both a button and
a form, which splits the action.

## 3. Code sketch

Server Component (the embedded-form variant delegates its client island to the form block).

```tsx
export function ResourceOffer({ eyebrow, title, support, inside, cta, reassurance, pending }) {
  return (
    <section id="resource" className="scroll-mt-16" style={{ backgroundColor: BAND }}>
      <div className="mx-auto grid max-w-[1280px] grid-cols-1 gap-10 px-5 py-16 sm:px-8
                      lg:grid-cols-[1.1fr_0.9fr] lg:gap-16 lg:py-24">
        <div>
          {eyebrow && (
            <p className="mb-4 text-[0.72rem] uppercase tracking-[0.18em]"
               style={{ color: BAND_ACCENT }}>{eyebrow}</p>
          )}
          <h2 className="text-3xl font-semibold leading-tight tracking-tight text-white sm:text-4xl">
            {title}
          </h2>
          {pending && (
            <p className="mt-3 text-[11px] uppercase tracking-[0.14em] text-white/60">{pending}</p>
          )}
          <p className="mt-5 max-w-[48ch] text-[1.02rem] leading-relaxed text-white/80">{support}</p>

          <div className="mt-7">
            <p className="mb-3 text-[0.72rem] uppercase tracking-[0.14em] text-white/55">
              Inside the guide
            </p>
            <ul className="space-y-2.5">
              {inside.map((item) => (
                <li key={item} className="flex items-start gap-3 text-[0.95rem] text-white/85">
                  <CheckIcon size={15} weight="bold" className="mt-1 shrink-0"
                             style={{ color: BAND_ACCENT }} />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="lg:pt-2">
          {"form" in cta ? cta.form : (
            <a href={cta.href} className="inline-flex items-center gap-2 rounded-[--radius]
                 bg-accent px-7 py-4 text-[15px] font-semibold text-on-accent">
              {cta.label}
            </a>
          )}
          {reassurance && <p className="mt-3 text-xs text-white/70">{reassurance}</p>}
        </div>
      </div>
    </section>
  );
}
```

**Why fixed hex values instead of tokens here.** One source spells this out in a comment: this is a
*deliberate single colour-block band*, allowed once per page by the Page Theme Lock rule, and its
colours are pinned so the band reads identically in light and dark mode. That is the correct
reading of the lock — it forbids sections *flipping* with the theme, not one intentional branded
band. Any theme-aware child inside it (a form card) stays theme-aware.

Note the section carries `scroll-mt-16` because the nav is sticky and this is an anchor target.

## 4. Mobile fallback (`< 768px`)

- Collapses to one column, **offer first, capture second**. The reader must know what they are
  giving an email for before they see the field.
- Padding drops from `lg:py-24` to `py-16`, and card padding from `lg:p-14` to `p-8`.
- The `inside` list keeps its icons — they are the scan anchors at small sizes.
- The CTA goes full width. The reassurance line moves below it rather than beside it.
- If the right column is a decorative cover mockup rather than a form, give it a
  `min-h-[16rem]` so it does not collapse to a sliver, or drop it entirely.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. |
| 4-7 | The whole band reveals once on entry. Do not stagger the `inside` items — three lines arriving one at a time reads as a slideshow. |
| 8-10 | As 4-7, plus a hover translate on the CTA arrow (`group-hover:translate-x-1`). |

Reduced motion: static. Never animate the band's background colour on entry — a large area
changing colour is the most nausea-inducing motion on a page.

## 6. Dark-mode notes

This block is the documented exception to the Theme Lock: **it is pinned, not themed.** The band
keeps its colour in both modes, so its internal contrasts are authored once and do not need a
second pass — but they must be authored properly, because `text-white/55` on a mid-slate band is
exactly the kind of value that passes by eye and fails WCAG AA.

Two things that are *not* pinned: an embedded form card (stays theme-aware, so it reads as a
surface floating on the band), and the section's outer border, which meets the page's surface and
must match the page's line token per mode.

If the page theme is already dark, do not use the same dark for the band — it stops reading as a
band. Shift it (deeper, or to the accent's dark neighbour) so the boundary survives.

## 7. Anti-patterns

- **A generic title.** "Free Guide" is not the asset's name. Both sources use the real title.
- **More than three `inside` items.** Past three it becomes a table of contents, and the reader
  stops reading rather than starts wanting.
- **Vague `inside` items.** "Actionable insights" is filler. "Where placement goes wrong, and the
  scan that catches it first" is an item.
- **A button *and* a form.** Two ways to say yes is one way too many.
- **Hiding that the asset does not exist yet.** One source ships a visible
  `[NEEDS: real resource asset]` marker and a link to a status page rather than implying a finished
  PDF. Do that. Collecting emails for a thing you cannot send is the fastest way to burn a list.
- **A second inverted band elsewhere on the page.** The Theme Lock allows one.
- **A fake product screenshot as the right-hand visual.** A *labelled* CSS cover mockup is honest
  when it is marked as pending art; an unlabelled one imitating a real cover is the div-based fake
  the rules ban — and the rendered pre-flight check now looks for that shape.
- **An em-dash anywhere in the copy.** Hard-fails the pre-flight check.
- **No reassurance line** next to an email field. "No spam, ever." costs one line and removes the
  main objection.

## 8. References

- `arianademers-site/src/components/ResourceCTA.tsx` — dark rounded card floating on a light
  section, pill eyebrow with an icon, Phosphor check icons, CSS cover mockup on the right marked
  `[NEEDS: real cover art]`, link CTA to a status page, "No spam, ever."
- `colinrigney-site/components/Resource.tsx` — full-bleed band with pinned hex colours and the
  Theme-Lock reasoning in a comment, embedded lead form on the right, dashed `[NEEDS]` block
  carrying a `data-needs` hook so the e2e suite can assert the gap marker has not silently vanished.

Independently agreed: eyebrow → title → support (`max-w-[48ch]` in both) → a three-item "inside"
list with check icons → capture, a two-column split at `lg`, an inverted surface, and visible
`[NEEDS]` markers rather than a polished-looking placeholder.
