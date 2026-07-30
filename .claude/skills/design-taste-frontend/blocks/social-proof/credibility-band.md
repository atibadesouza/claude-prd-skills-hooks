---
name: credibility-band
category: social-proof
dial_compatibility:
  variance: [3, 8]
  motion: [1, 7]
  density: [3, 6]
when_to_use: "Establishing authority with numbers and credentials, especially in regulated or evidence-sensitive fields - medical, financial, legal, scientific. Handles the case where the real figures are not confirmed yet without lying or leaving a hole."
not_for: "Logo walls (that is a different block). Testimonial grids. Consumer social proof where the claim is volume rather than credentials - 'join 40,000 members' does not need attribution machinery."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/ProofBand.tsx", "colinrigney-site/components/Credibility.tsx"]
---

# Credibility Band

A claim, the numbers behind it, and — non-negotiably — where each number came from.

Both harvest sources open with the same rule written into a comment, arrived at independently:
**no clinical or outcome claim is asserted in the site's generic voice; every figure is attributed
to a named person or source, and stays an explicit placeholder until a publishable number is
confirmed.** That rule is the block.

## 1. Visual sketch

```
  THE CLAIM (h2, <= 2 lines)
  One paragraph of support, <= 52ch.

  ┌───────────┬───────────┬───────────┐   hairline grid, no card shadows
  │  FIGURE   │  FIGURE   │  FIGURE   │
  │  what it  │  what it  │  what it  │
  │  measures │  measures │  measures │
  │  Source:  │  Source:  │  Source:  │   <- attribution, per figure, always
  │  [NEEDS…] │  [NEEDS…] │  [NEEDS…] │   <- visible until confirmed
  └───────────┴───────────┴───────────┘

  │ "A quote, attributed."          OR   credentials block, named and specific
  │ — Name, Role
```

## 2. Props API

```ts
type Stat = {
  figure: string;        // the number, OR an explicit "[NEEDS: figure]" marker
  label: string;         // what it measures, in the reader's words
  source: string;        // REQUIRED. "Source: X registry, reported by Dr. Y"
  note?: string;         // what still needs confirming, shown until it is
};

type CredibilityBandProps = {
  claim: string;                  // the h2
  support: string;                // <= 52ch measure
  stats: Stat[];                  // 2-3. four starts to read as a dashboard.
  quote?: { text: string; cite: string; role: string; note?: string };
  credentials?: { name: string; body: string; note?: string };
};
```

**`source` is required, not optional.** That is the whole design. An optional attribution field is
an attribution that gets skipped on the busy page, and the busy page is exactly where an
unattributed clinical claim does damage. If there is no source, there is no stat.

## 3. Code sketch

Server Component.

```tsx
export function CredibilityBand({ claim, support, stats, quote }) {
  return (
    <section id="results" className="bg-surface py-20 sm:py-28">
      <div className="mx-auto max-w-[1280px] px-5 sm:px-8">
        <Reveal className="max-w-2xl">
          <h2 className="text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
            {claim}
          </h2>
          <p className="mt-5 max-w-[52ch] text-base leading-relaxed text-muted">{support}</p>
        </Reveal>

        {/* hairline grid: 1px gaps over a line-coloured background - no card shadows */}
        <div className="mt-14 grid grid-cols-1 gap-px overflow-hidden rounded-[--radius]
                        border border-line bg-line md:grid-cols-3">
          {stats.map((s, i) => (
            <Reveal key={s.label} delay={i * 0.08} className="flex flex-col bg-surface p-7 sm:p-8">
              <span className="text-4xl font-semibold leading-none text-accent sm:text-5xl">
                {s.figure}
              </span>
              <span className="mt-5 text-[15px] font-semibold leading-snug">{s.label}</span>
              <span className="mt-3 text-xs leading-relaxed text-muted">{s.source}</span>
              {s.note && (
                <span className="mt-auto pt-4 text-[11px] uppercase tracking-[0.12em] text-accent/70">
                  {s.note}
                </span>
              )}
            </Reveal>
          ))}
        </div>

        {quote && (
          <Reveal className="mt-16 border-l-2 border-accent pl-6 sm:mt-20 sm:pl-9">
            <blockquote className="max-w-[40ch] text-2xl font-medium italic leading-[1.35] sm:text-3xl">
              &ldquo;{quote.text}&rdquo;
            </blockquote>
            <div className="mt-6 flex flex-col gap-1">
              <cite className="not-italic text-sm font-semibold tracking-wide">{quote.cite}</cite>
              <span className="text-xs text-muted">{quote.role}</span>
            </div>
          </Reveal>
        )}
      </div>
    </section>
  );
}
```

The **hairline grid** — `gap-px` over a line-coloured background, with each cell painting its own
surface — was chosen independently by both sources. It gives crisp 1px dividers with no borders to
double up at the seams, and no card shadows. Copy the technique.

Use `&ldquo;` / `&rdquo;` for the quote marks, never an em-dash before the attribution: the
pre-flight check hard-fails em-dashes anywhere on the page, attribution lines included.

## 4. Mobile fallback (`< 768px`)

- Stat grid collapses to one column. The hairline technique still works — the `gap-px` becomes
  horizontal rules between stacked cells.
- Figures drop from `text-5xl` to `text-4xl`. A five-character placeholder like `[NEEDS: figure]`
  at `text-5xl` wraps on a 375px screen and looks broken rather than pending.
- The quote drops to `text-xl`, and the left rule from `pl-9` to `pl-6`.
- Keep the source line at full size. It is the first thing shrunk to make things fit and the last
  thing that should be — an unreadable attribution is an absent attribution.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. |
| 4-7 | Heading reveals, then the stat cells stagger at ~80ms each. |
| 8-10 | As 4-7, plus an optional count-up on the figures — **only when they are real numbers.** Never animate a `[NEEDS: figure]` placeholder; counting up to a placeholder is absurd. |

Reduced motion: everything static, and no count-up. A number that only becomes readable after an
animation is unreadable to someone who has turned animation off.

## 6. Dark-mode notes

The hairline grid needs a `line` token that is visible on both surfaces — a value tuned as a
hairline on light paper usually vanishes on dark ink. Pick per mode, not one alpha.

The figure colour is the accent, and it must clear WCAG AA against the cell surface in both modes.
A brass or ochre accent that reads well on cream commonly fails on dark.

The `note` marker (`text-accent/70`) is intentionally quiet, which makes it the most likely element
to fall below AA in one mode. Check it specifically — a "needs confirming" flag nobody can read
defeats its purpose.

## 7. Anti-patterns

- **An unattributed statistic.** The rule both sources wrote down. In a regulated field this is the
  difference between a claim and a liability.
- **A clinical or outcome claim in the site's own voice.** Attribute it to a named person or a cited
  source, or cut it.
- **Inventing a plausible number** because the real one is not confirmed. Ship the `[NEEDS: figure]`
  marker — one source ships *all three* figures as placeholders rather than guess, which is the
  right call.
- **Hiding the placeholder** in a comment or a lighter colour so it "looks finished". The whole
  point is that it is visible until resolved.
- **Four or more stats.** It stops being proof and starts being a dashboard.
- **Vanity metrics with no denominator** ("10,000+ hours"). If the label does not say what it
  measures, the figure is decoration.
- **An em-dash before the quote attribution.** Hard-fails the pre-flight check.
- **Card shadows on the stat cells.** The hairline grid exists so they are not needed.
- **A quote with no role.** "Dr. Smith" is not attribution; "Dr. Smith, Founder, X Institute" is.

## 8. References

- `arianademers-site/src/components/ProofBand.tsx` — full-width band, 3-across hairline stat grid,
  every figure a placeholder pending confirmation, per-stat `Source:` line, closing pull quote with
  `<cite>` and its own confirmation marker.
- `colinrigney-site/components/Credibility.tsx` — two-column layout with a sticky claim, 2-across
  stat grid, three tenets as divided rows rather than cards, and a named credentials block
  (`OCS, 2013`, `RMSK, APCA`) in place of a quote.

Independently agreed: the governing attribution rule written as a file-top comment, the `gap-px`
hairline grid technique, figure → label → source ordering, visible unresolved-figure markers, and
a `max-w` measure of roughly 42-52 characters on the support paragraph.
