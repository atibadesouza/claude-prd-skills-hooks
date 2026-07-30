---
name: bio-narrative
category: feature
dial_compatibility:
  variance: [3, 8]
  motion: [1, 7]
  density: [2, 5]
when_to_use: "The about section of a personal-authority page. A portrait, the story in the person's own terms, and the credentials that back it. Works for consultants, clinicians, coaches, founders, authors."
not_for: "Team pages with multiple people (that is a grid, not a narrative). Company about pages with no single protagonist. Any bio short enough to fit in a hero."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/About.tsx", "colinrigney-site/components/About.tsx"]
---

# Bio Narrative

Portrait one side, story the other. The story is wider than the portrait, and that is on purpose.

## 1. Visual sketch

```
┌────────────┬──────────────────────────────────────┐
│            │  THE POSITION, IN ONE LINE           │
│  PORTRAIT  │                                      │
│   4 / 5    │  Two or three paragraphs of prose.   │
│            │  Written as sentences, not bullets.  │
│  sticky    │                                      │
│            │  The credentials paragraph: names,   │
│  creds     │  bodies, dates. Specific.            │
│  caption   │                                      │
└────────────┴──────────────────────────────────────┘
    0.85fr                    1.15fr
```

Both harvest sources chose `lg:grid-cols-[0.85fr_1.15fr]` independently. The story gets more room
than the face — this section is read, not looked at.

## 2. Props API

```ts
type BioNarrativeProps = {
  portrait: { src?: string; label: string; ratio?: string };
  caption?: string;             // credentials under the portrait, in one dense line
  heading: React.ReactNode;     // ReactNode so one phrase can carry emphasis
  story: string[];              // 2-3 paragraphs. prose, not bullets.
  credentials?: string;         // the formal paragraph: titles, bodies, dates
  pillars?: { icon: React.ComponentType; title: string; body: string }[];  // optional, exactly 3
  pending?: string[];           // visible markers for what is still missing
};
```

`story` is an array of strings rather than one blob so the paragraph rhythm is structural. Both
sources use `space-y-5` between paragraphs, and both keep the ethos paragraphs separate from the
formal credentials paragraph — different voices, deliberately not merged.

## 3. Code sketch

Server Component.

```tsx
export function BioNarrative({ portrait, caption, heading, story, credentials, pending }) {
  return (
    <section id="about" className="bg-surface-alt py-16 sm:py-20 lg:py-24">
      <div className="mx-auto grid max-w-[1280px] grid-cols-1 items-start gap-10 px-5 sm:px-8
                      lg:grid-cols-[0.85fr_1.15fr] lg:gap-16">

        {/* order-2 on mobile: the heading must be the first thing read */}
        <Reveal className="order-2 lg:order-1">
          <div className="mx-auto w-full max-w-[24rem] lg:sticky lg:top-24">
            <ImageSlot {...portrait} ratio={portrait.ratio ?? "4 / 5"} />
            {caption && (
              <p className="mt-4 text-[11px] uppercase tracking-[0.14em] text-faint">{caption}</p>
            )}
          </div>
        </Reveal>

        <Reveal className="order-1 lg:order-2" delay={0.08}>
          <h2 className="text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
            {heading}
          </h2>
          <div className="mt-6 space-y-5 text-[1.02rem] leading-relaxed text-muted">
            {story.map((p, i) => <p key={i}>{p}</p>)}
          </div>
          {credentials && (
            <div className="mt-6 space-y-5 text-[1.02rem] leading-relaxed text-muted">
              <p>{credentials}</p>
            </div>
          )}
          {pending?.length > 0 && (
            <div className="mt-8 space-y-2.5">
              <p className="text-[0.72rem] uppercase tracking-[0.14em] text-faint">
                To complete this section
              </p>
              {pending.map((n, i) => <NeedsBlock key={i}>{n}</NeedsBlock>)}
            </div>
          )}
        </Reveal>
      </div>
    </section>
  );
}
```

`lg:sticky lg:top-24` on the portrait column is the detail that makes this section feel considered:
the face stays with you while the story scrolls. `items-start` on the grid is required for sticky
to work — `items-center` silently kills it.

The `top-24` value must clear the sticky nav. If the nav is 64px, `top-24` (96px) leaves 32px of
breathing room; anything less and the portrait tucks under the bar.

## 4. Mobile fallback (`< 768px`)

- One column, and **the heading comes first**. Use `order-1 lg:order-2` on the story and
  `order-2 lg:order-1` on the portrait. One source does this and the other does not — the ordered
  one is right. Landing on a face with no context makes the reader scroll to find out who it is.
- Portrait caps at `max-w-[24rem]` and centres. A 4/5 portrait at full 375px width is a 470px slab.
- `lg:sticky` is inert at this width, which is correct — sticky on a one-column mobile layout
  pins the portrait over the text.
- Credentials caption stays at 11px uppercase but must be allowed to wrap to three lines. Do not
  truncate credentials.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. |
| 4-7 | Both columns reveal, the story delayed ~80ms behind the portrait. |
| 8-10 | As 4-7. Optionally stagger the `pillars` if present. Do not stagger the story paragraphs — text arriving line by line is unreadable, not dramatic. |

Reduced motion: static. The portrait is often a `priority` image; never let a reveal delay it.

## 6. Dark-mode notes

This section usually runs on `surface-alt` — the alternate band that separates it from the hero
above and the proof below. Both sources do this, on opposite base themes.

The credentials caption is the risk: small, uppercase, wide-tracked, and deliberately quiet
(`text-faint`). At 11px it needs *more* contrast than body text, not less, and it is the element
most likely to fall below WCAG AA in one of the two modes. Check it in both.

The portrait's inset ring flips (`ring-black/10` on light, `ring-white/10` on dark) — without it a
light photo bleeds into a light surface.

## 7. Anti-patterns

- **Portrait first on mobile.** See section 4.
- **Bullet points instead of prose.** This is the one section on the page that earns paragraphs.
  A bulleted bio reads as a résumé and kills the voice.
- **Merging ethos and credentials into one paragraph.** They are different registers: the story is
  in the person's voice, the credentials are formal and checkable. Both sources keep them apart.
- **Vague credentials.** "Award-winning, internationally recognised" is noise. "Board-certified
  Orthopaedic Clinical Specialist (OCS, 2013)" is a credential.
- **`items-center` on the grid**, which silently disables the sticky column.
- **A sticky `top` smaller than the nav height** — the portrait slides under the bar.
- **Third person that never says the name.** "With over a decade of experience…" — whose?
- **More than three paragraphs.** Past that it is a biography page, not an about section.
- **Hiding an unfinished bio.** One source ships a visible "To complete this section" list naming
  exactly what is missing (an origin line, a verified figure) rather than padding with adjectives.
- **A stock portrait.** See the image-slot block — this is the section where that does most damage.

## 8. References

- `arianademers-site/src/components/About.tsx` — mobile order swap so the heading leads, dense
  credentials caption under the portrait, three icon pillars, display serif heading with an italic
  emphasis span, `lg:top-28`.
- `colinrigney-site/components/About.tsx` — portrait sticky at `lg:top-24`, ethos paragraphs kept
  separate from the formal credentials paragraph, explicit "To complete this section" block naming
  two specific gaps.

Independently agreed: `lg:grid-cols-[0.85fr_1.15fr]`, portrait left / story right at desktop,
`4 / 5` portrait ratio, `lg:sticky` portrait column with `items-start`, `space-y-5` paragraph
rhythm, a separate formal credentials paragraph, and visible markers for what is still missing.
