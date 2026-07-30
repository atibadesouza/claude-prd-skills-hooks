---
name: anchor-footer
category: footer
dial_compatibility:
  variance: [2, 7]
  motion: [1, 3]
  density: [2, 5]
when_to_use: "One-page and small-site footers. Identity block + a short link column + a legal/disclaimer rule. Optionally opens with a final CTA when the page has no other closing action."
not_for: "Large multi-column sitemap footers (5+ columns, product/company/resources/legal). This block is deliberately 2-3 columns and should not grow into a sitemap."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/Footer.tsx", "colinrigney-site/components/Footer.tsx"]
---

# Anchor Footer

Who this is, where to go, and the legal line. Optionally one last ask on top.

## 1. Visual sketch

```
┌──────────────────────────────────────────────────────────────┐
│  Closing ask (optional)                        [ CTA ]       │
│  one line of support copy                                    │
│ ─────────────────────────────────────────────────────────────│
│  WORDMARK, suffix          EXPLORE          CONTACT          │
│  2-3 lines on who this     Approach         email            │
│  is and what it does.      How it works     booking          │
│                            Library          location         │
│                            About                             │
│ ─────────────────────────────────────────────────────────────│
│  (c) 2026 Name. All rights reserved.   disclaimer / status   │
└──────────────────────────────────────────────────────────────┘
```

Three horizontal bands, two rules. Both harvest sources use exactly this skeleton.

## 2. Props API

```ts
type AnchorFooterProps = {
  wordmark: React.ReactNode;
  blurb: string;                                   // <= ~40ch wide. who this is, not a pitch.
  columns: { heading: string; items: React.ReactNode[] }[];  // 1-2 columns. not 5.
  closingCta?: { heading: string; support: string; href: string; label: string };
  legal: string;                                   // copyright line
  disclaimer?: string;                             // regulated-industry or build-status line
};
```

`items` is `ReactNode[]`, not `{href,label}[]`, because one harvest source's contact column holds
placeholder markers rather than links. Forcing them to be links would have meant faking hrefs.

## 3. Code sketch

Pure Server Component. This block needs no JS.

```tsx
export function Footer({ wordmark, blurb, columns, closingCta, legal, disclaimer }) {
  const year = new Date().getFullYear();
  return (
    <footer id="contact" className="bg-surface-alt text-ink">
      <div className="mx-auto max-w-[1280px] px-5 py-14 sm:px-8 lg:py-20">

        {closingCta && (
          <div className="flex flex-col items-start justify-between gap-6 border-b border-line pb-12
                          sm:flex-row sm:items-end">
            <div>
              <h2 className="max-w-[18ch] text-2xl font-semibold leading-tight tracking-tight sm:text-3xl">
                {closingCta.heading}
              </h2>
              <p className="mt-3 max-w-[44ch] text-[0.95rem] leading-relaxed text-muted">
                {closingCta.support}
              </p>
            </div>
            <a href={closingCta.href}
               className="inline-flex shrink-0 items-center gap-2 rounded-[--radius] bg-accent
                          px-5 py-3 text-[0.95rem] font-semibold text-on-accent">
              {closingCta.label}
            </a>
          </div>
        )}

        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-[1.4fr_1fr_1fr]">
          <div>
            <p className="text-lg font-semibold tracking-tight">{wordmark}</p>
            <p className="mt-2 max-w-[36ch] text-[0.9rem] leading-relaxed text-muted">{blurb}</p>
          </div>
          {columns.map((col) => (
            <div key={col.heading}>
              <p className="mb-3 text-[0.72rem] uppercase tracking-[0.14em] text-faint">
                {col.heading}
              </p>
              <ul className="space-y-2 text-[0.9rem] text-muted">
                {col.items.map((it, i) => <li key={i}>{it}</li>)}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col gap-2 border-t border-line pt-6 text-[0.8rem] text-faint
                        sm:flex-row sm:items-center sm:justify-between">
          <p>&copy; {year} {legal}</p>
          {disclaimer && <p className="max-w-[52ch] leading-relaxed">{disclaimer}</p>}
        </div>
      </div>
    </footer>
  );
}
```

The year is computed, never hardcoded. A stale copyright year is the cheapest possible signal that
a site is abandoned.

**The `1.4fr` identity column is not arbitrary** - both sources chose it independently. The blurb
needs roughly 40% more width than a link list to reach a readable measure.

## 4. Mobile fallback (`< 768px`)

- Grid collapses to one column, identity first, then each link column. Do not reorder to put links
  first - the identity block is what a footer is for.
- The closing-CTA row stacks: heading, support copy, then a full-width button.
- The legal row stacks vertically with `gap-2`; the disclaimer must not sit beside the copyright at
  375px or both truncate.
- Vertical padding drops from `py-20` to about `py-14`.
- Column headings keep their uppercase tracking treatment. **They are not eyebrows** - they sit
  above a list, not above a heading, so they do not count toward the eyebrow ratio. Both sources
  confirm this: their footer labels are correctly ignored by the mechanical check.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Static. |
| 4-7 | Wrap the whole footer in one scroll-reveal. Do **not** stagger the link columns. |
| 8-10 | Same as 4-7. The footer is the wrong place to spend a motion budget - a reader who reached it is looking for a specific link, not a performance. |

Reduced motion: static, no exceptions.

## 6. Dark-mode notes

Both sources make the same structural choice worth copying: **the footer runs on the alternate
surface**. On a light page the footer is the dark band that closes it; on a dark page it is a
deeper shade of the same ink. Either way it is `surface-alt`, not `surface`.

That means the footer often carries an inverted token set relative to the body, which is the one
place where a page-level Theme Lock legitimately bends - a closing band is read as a boundary,
not as a section that flipped.

Contrast to re-check per mode: `muted` and `faint` text on `surface-alt`. Faint text on an
alternate surface is the most common place a page drops below WCAG AA, because it is styled once
and then never looked at again.

## 7. Anti-patterns

- **A hardcoded copyright year.**
- **Sitemap sprawl.** Five columns of links in a footer for a one-page site is cargo-culted from
  SaaS marketing sites.
- **Version footers** (`v1.4.2`, `Build 0048`). Banned by the pre-flight check on marketing pages.
- **Social icon rows with no real accounts** - placeholder icons linking to `#` are worse than no
  icons.
- **Repeating the full nav.** The footer link column is a short subset, not a mirror.
- **A second CTA with a different intent** from the closing ask. One closing action.
- **Faint-on-alternate-surface text below AA.** See dark-mode notes.
- **Hiding a required disclaimer at 10px.** In regulated fields (medical, financial, legal) the
  disclaimer is load-bearing content - one source carries an explicit not-medical-advice line and
  an attribution statement. Style it quietly, do not bury it.
- **Dropping the identity blurb on mobile.** It is the part that says who this is.

## 8. References

- `arianademers-site/src/components/Footer.tsx` - two columns (`1.4fr 1fr`), dark ink band under a
  dark page, regulated-industry disclaimer, honest `[NEEDS:]` placeholder for unverified contact
  details.
- `colinrigney-site/components/Footer.tsx` - three columns (`1.4fr 1fr 1fr`), opens with a closing
  CTA row, build-status line in place of a disclaimer, placeholder markers as list items.

Independently agreed: computed year, `1.4fr` identity column, `max-w` container with
`px-5 sm:px-8`, uppercase tracked column headings, a top rule before the legal row, and the legal
row going `flex-col` -> `sm:flex-row` with `justify-between`.
