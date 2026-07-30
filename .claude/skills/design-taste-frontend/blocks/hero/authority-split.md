---
name: authority-split
category: hero
dial_compatibility:
  variance: [4, 8]
  motion: [1, 8]
  density: [2, 5]
when_to_use: "A named person or single-expert brand is the offer - consultant, physician, coach, solo practice, author. One strong message on the left, one real portrait on the right. The default hero when credibility is carried by a face."
not_for: "Product/SaaS launches where a UI screenshot is the asset (use a product hero). Editorial manifesto launches where the message IS the design and an image would dilute it. Brands with no real photography - this block collapses badly with a fake or stock portrait."
stack: ["react", "next", "tailwind", "motion"]
harvested_from: ["arianademers-site/src/components/Hero.tsx", "colinrigney-site/components/Hero.tsx"]
---

# Authority Split Hero

Message left, person right. Two shipped sites arrived at the *same* proportions independently
while looking nothing alike - which is the evidence for what belongs in this block and what does not.

## 1. Visual sketch

```
┌───────────────────────────────────────────────────────────┐
│  EYEBROW - who this is for / what it is                   │
│                                            ┌────────────┐ │
│  Headline that makes                       │            │ │
│  one specific claim                        │  PORTRAIT  │ │
│                                            │   3/4 or   │ │
│  One paragraph, <= 46ch, saying who        │    4/5     │ │
│  it is for and what changes.               │            │ │
│                                            └────────────┘ │
│  [ Primary CTA ]  [ Secondary ]                           │
└───────────────────────────────────────────────────────────┘
        1.05fr                    :              0.95fr
```

The near-equal split is deliberate and was independently chosen by both sources: the message
gets slightly more room than the face, but the face is not a garnish.

## 2. Props API

```ts
type AuthoritySplitHeroProps = {
  eyebrow: string;            // short. one line at 375px.
  headline: React.ReactNode;  // ReactNode so one phrase can carry emphasis
  subtext: string;            // <= 46ch enforced by max-w, not by trust
  primaryCta:   { href: string; label: string };
  secondaryCta?: { href: string; label: string };
  portrait: { src: string; alt: string; ratio?: "3 / 4" | "4 / 5" };
};
```

**Exactly four text slots, and no fifth.** Eyebrow, headline, subtext, CTAs. The API has no prop
for a tagline under the buttons because that is the single most common way this hero degrades -
see anti-patterns. Making it unrepresentable is cheaper than a rule nobody reads.

## 3. Code sketch

Server Component by default. The entrance animation is the only reason to reach for a client island.

```tsx
export function Hero({ eyebrow, headline, subtext, primaryCta, secondaryCta, portrait }) {
  return (
    <section id="top" className="relative overflow-hidden">
      {/* optional brand-owned ambient layer sits here, aria-hidden */}
      <div className="relative mx-auto grid w-full max-w-[1280px] grid-cols-1 items-center
                      gap-10 px-5 pb-16 pt-24 sm:px-8
                      lg:grid-cols-[1.05fr_0.95fr] lg:gap-14 lg:pb-24 lg:pt-24">
        <div className="max-w-[36rem]">
          <p className="mb-5 text-[0.72rem] font-semibold uppercase tracking-[0.18em] text-accent">
            {eyebrow}
          </p>
          <h1 className="text-balance text-[2.4rem] font-semibold leading-[1.05]
                         tracking-tight sm:text-5xl lg:text-[3.4rem]">
            {headline}
          </h1>
          <p className="mt-5 max-w-[46ch] text-[1.05rem] leading-relaxed text-muted">
            {subtext}
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
            <a href={primaryCta.href} className="inline-flex items-center justify-center gap-2
                 rounded-[--radius] bg-accent px-6 py-3.5 text-[0.95rem] font-semibold text-on-accent">
              {primaryCta.label}
            </a>
            {secondaryCta && (
              <a href={secondaryCta.href} className="inline-flex items-center justify-center
                   rounded-[--radius] border border-line px-6 py-3.5 text-[0.95rem] font-semibold">
                {secondaryCta.label}
              </a>
            )}
          </div>
        </div>
        <div className="relative mx-auto w-full max-w-[26rem] lg:max-w-none">
          <ImageSlot {...portrait} priority />
        </div>
      </div>
    </section>
  );
}
```

`priority` on the portrait is not optional - it is the LCP element.

**Use `min-h-[100dvh]` or nothing. Never `h-screen`** (hard-fail in the pre-flight check, and
`h-screen` is wrong on mobile browsers whose toolbars change the viewport). A full-height hero is
a brand decision: one source went full-height on a dark canvas, the other let content set the
height on a light one. Both pass.

## 4. Mobile fallback (`< 768px`)

- Grid collapses to one column; **portrait moves below the message**, never above it. The headline
  must be the first thing rendered.
- Portrait caps at `max-w-[26rem]` and centres, so it does not become a full-bleed slab.
- CTAs go `flex-col` full-width, primary first. Two side-by-side buttons at 375px wrap their labels,
  which the pre-flight check flags.
- Drop `pt-24` to about `pt-16`. Hero top padding above `pt-24` at desktop floats the content
  halfway down the viewport.
- Headline must survive a long unbroken word. Add `overflow-wrap: break-word` to the `h1` - the
  rendered pre-flight check injects a 26-character token here, and **both harvest sources fail it
  at 375px**, so this is an observed defect and not a hypothetical.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. Render as a Server Component, no client island at all. |
| 4-7 | Portrait fades + scales from `0.97` over ~1s, delayed ~0.25s. Text renders immediately. |
| 8-10 | Text children stagger in - `staggerChildren: 0.12, delayChildren: 0.1`, each item `y: 24 -> 0` over 0.8s with ease `[0.16, 1, 0.3, 1]`. Portrait as above. |

Reduced motion: pass `initial={false}` so every element renders at its final state. The hero is the
LCP element - a reduced-motion path that leaves it at `opacity: 0` is a blank page, not a
degraded animation.

**Never reveal the hero on scroll.** It is already in view; wrapping it in a scroll-reveal delays
LCP and hides the primary message if JS fails.

## 6. Dark-mode notes

This block is a strong candidate for a **locked** theme rather than a token-swapped one: it carries
a full-bleed background, and the two harvest sources committed opposite directions (dark ink canvas
vs light paper). If the page has a Theme Lock, the hero honours it - it must not be the one section
that flips.

Tokens that must exist in both modes: surface, ink/text, muted text, accent, on-accent, line.
The ambient background layer (gradient or pattern) is per-mode, not per-token - re-author it, do
not tint it.

Portrait shadows need different values per mode: a heavy warm shadow reads as dirt on a light
surface, and disappears entirely on a dark one.

## 7. Anti-patterns

- **A fifth text element.** A tiny tagline or pull-quote under the CTAs is the most common failure,
  and one harvest source does it (`colinrigney-site/components/Hero.tsx:49`, a mono pull-quote
  directly below the buttons). It reads as an afterthought and pushes the CTA out of first view.
  The pre-flight check bans it. This block's API has no slot for it on purpose.
- **A trust micro-strip in the hero** ("Trusted by 400 clinicians", logo row). It belongs under the
  hero, not inside it.
- **A fake or stock portrait.** This block is a credibility device; a stock face inverts its
  purpose. If there is no real photo, use an honest labelled image slot and say what is missing.
- **`h-screen`.** Hard-fail. Use `min-h-[100dvh]`.
- **Headline over two lines at desktop**, or subtext over ~4 lines / 20 words. Both push the CTA
  below the fold, which is the one thing this hero exists to prevent.
- **Two CTAs with the same intent** ("Get started" + "Let's talk"). The secondary must go somewhere
  genuinely different, usually deeper into the page.
- **Scroll cues** ("Scroll", down-arrows). Hard-fail in the pre-flight check.
- **An eyebrow that repeats the headline.** It should say who it is for or what category this is,
  not restate the claim.
- **Animating the whole hero as one block.** Stagger the children or animate nothing; a single
  fade of the entire section reads as a slow page rather than a designed entrance.

## 8. References

Both implementations in the harvest corpus, shipped and pre-flight-clean on checks 1-8:

- `arianademers-site/src/components/Hero.tsx` - dark ink canvas, radial ambient field, gold accent,
  pill CTAs, display serif with an italic emphasis span, staggered entrance.
- `colinrigney-site/components/Hero.tsx` - light paper canvas, blueprint-grid pattern, square-ish
  4px radii, mono eyebrow, no entrance animation. Also the source of the fifth-element anti-pattern
  above.

The two agreed, independently, on: `lg:grid-cols-[1.05fr_0.95fr]`, `max-w-[46ch]` subtext,
`px-5 sm:px-8`, portrait right with an explicit aspect ratio and a shadow, and eyebrow -> h1 ->
subtext -> CTA order. That agreement is why those specifics are in the block and the rest is not.
