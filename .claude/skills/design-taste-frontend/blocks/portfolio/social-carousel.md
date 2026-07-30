---
name: social-carousel
category: portfolio
dial_compatibility:
  variance: [3, 8]
  motion: [2, 7]
  density: [3, 7]
when_to_use: "A horizontally scrollable strip of published work - videos, talks, episodes, case studies - usually paired with a row of links to where that work lives. Swipe on mobile, buttons on desktop."
not_for: "Primary navigation. Anything the reader must see all of (a horizontal strip hides most of its contents by design). Image galleries where a grid would show everything at once."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/SocialCarousel.tsx", "colinrigney-site/components/SocialCarousel.tsx"]
---

# Social Carousel

A swipeable strip of published work, plus the links to where it lives.

## 1. Visual sketch

```
  EYEBROW  Teaching library                          [ ← ] [ → ]   desktop only
  Section heading

  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────
  │  thumb     │ │  thumb     │ │  thumb     │ │  thu…     scroll-snap,
  │  REGION    │ │  REGION    │ │  REGION    │ │  REG…     overflow-x inside
  │  Title of  │ │  Title of  │ │  Title of  │ │  Tit…     ITS OWN container
  │  the video │ │  the video │ │  the video │ │       │
  └────────────┘ └────────────┘ └────────────┘ └───────
        ↑ swipe is the primary interaction on mobile

  ▸ YouTube   ▸ LinkedIn   ▸ Podcast   ▸ Website
```

## 2. Props API

```ts
type Item = { id: string; region?: string; title: string; href?: string };
type SocialLink = { label: string; href: string; glyph: string };

type SocialCarouselProps = {
  eyebrow?: string;
  heading: string;
  items: Item[];             // 4+. fewer than 4 does not need a carousel - use a row.
  socials?: SocialLink[];
  ariaLabel?: string;        // names the scroll region for screen readers
};
```

## 3. Code sketch

Client island — it needs a ref and click handlers. The cards themselves are static markup.

```tsx
"use client";
import { useCallback, useRef, useState } from "react";

export function SocialCarousel({ eyebrow, heading, items, socials }) {
  const trackRef = useRef<HTMLUListElement>(null);
  const [atStart, setAtStart] = useState(true);
  const [atEnd, setAtEnd] = useState(false);

  const updateEdges = useCallback(() => {
    const el = trackRef.current;
    if (!el) return;
    const max = el.scrollWidth - el.clientWidth;
    setAtStart(el.scrollLeft <= 2);
    setAtEnd(el.scrollLeft >= max - 2);
  }, []);

  function scrollByDir(dir: 1 | -1) {
    const el = trackRef.current;
    if (!el) return;
    // Step by one card, not by an arbitrary pixel amount.
    const first = el.querySelector<HTMLElement>("li");
    const step = first ? first.getBoundingClientRect().width + 16 : el.clientWidth * 0.8;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    el.scrollBy({ left: dir * step, behavior: reduce ? "auto" : "smooth" });
  }

  return (
    <section id="library" className="scroll-mt-16 py-16 lg:py-24">
      <div className="mx-auto max-w-[1280px] px-5 sm:px-8">
        <div className="flex items-end justify-between gap-4">
          <div>
            {eyebrow && (
              <p className="mb-3 text-[0.72rem] uppercase tracking-[0.16em] text-accent">{eyebrow}</p>
            )}
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">{heading}</h2>
          </div>
          <div className="hidden gap-2 md:flex">
            <button type="button" onClick={() => scrollByDir(-1)} disabled={atStart}
                    aria-label="Show previous items"
                    className="grid h-11 w-11 place-items-center rounded-full border border-line
                               disabled:opacity-40">←</button>
            <button type="button" onClick={() => scrollByDir(1)} disabled={atEnd}
                    aria-label="Show next items"
                    className="grid h-11 w-11 place-items-center rounded-full border border-line
                               disabled:opacity-40">→</button>
          </div>
        </div>

        {/* The strip scrolls inside ITS OWN overflow container, so the PAGE never
            scrolls sideways. -mx-5 px-5 lets cards bleed to the edge without
            widening the document. */}
        <ul ref={trackRef} onScroll={updateEdges} tabIndex={0}
            aria-label="Scrollable list of published work"
            className="-mx-5 mt-8 flex snap-x snap-mandatory gap-4 overflow-x-auto px-5 pb-4
                       [scrollbar-width:none] sm:-mx-8 sm:px-8">
          {items.map((it) => (
            <li key={it.id} className="w-[260px] shrink-0 snap-start sm:w-[300px]">
              {/* thumb, region label, h3 title */}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
```

**The one non-negotiable line** is the overflow containment. One source states it outright in a
file comment: *the strip scrolls inside its own overflow container, so the page never scrolls
sideways.* The `-mx-5 px-5` pairing is what lets cards bleed to the viewport edge without widening
the document — the rendered pre-flight check measures exactly this, at 375 / 768 / 1440.

**Two accessibility requirements**, one from each source, and you want both:
- `tabIndex={0}` + `aria-label` on the strip, so keyboard users can scroll it and hear what it is.
- Prev/next as real `<button>`s with `aria-label`, `disabled` at the edges. A div with an onClick
  is not reachable by keyboard.

Reduced motion is handled in the *handler*, not in CSS: `behavior: reduce ? "auto" : "smooth"`.
A smooth-scroll API call ignores the CSS media query entirely, so this is the only place it works.

## 4. Mobile fallback (`< 768px`)

- **Swipe is the primary interaction.** Buttons are `hidden md:flex` — native touch scrolling is
  better than any button on a phone.
- Cards go `w-[260px] shrink-0`. Fixed width, never percentage — a percentage card in a flex
  scroller collapses.
- Show a *partial* next card at the right edge. A strip whose last visible card ends flush looks
  like a grid and nobody swipes it.
- `snap-x snap-mandatory` with `snap-start` on each card, so a swipe lands cleanly.
- Hide the scrollbar (`[scrollbar-width:none]`) but never remove the ability to scroll.
- Keep `pb-4` so focus rings on cards are not clipped by the overflow container.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Buttons jump (`behavior: "auto"`). No reveal. |
| 4-7 | Smooth button scroll; the section reveals once on entry as a whole. |
| 8-10 | As 4-7, plus a subtle lift on card hover. **Never auto-advance.** |

Reduced motion: `behavior: "auto"` — see section 3.

**Auto-advancing carousels are banned, not discouraged.** They move content out from under the
reader, are a documented accessibility failure, and on a page like this they compete with the
section the reader was actually reading.

## 6. Dark-mode notes

Needs `surface`, `line`, `accent`, `muted`, plus a card surface distinguishable from the section
background in both modes — a strip of cards that matches its background reads as one grey block.

The arrow buttons' `disabled:opacity-40` is the trap: 40% of a light border on a light surface is
invisible, so at the strip's start the control looks broken rather than disabled. Set a real
disabled token per mode instead of relying on opacity.

If cards carry video thumbnails, they need a subtle border or inset ring in dark mode, or dark
thumbnails bleed into the background with no edge.

## 7. Anti-patterns

- **Letting the strip widen the page.** The failure this block is most likely to cause, and the
  rendered pre-flight check exists partly to catch it. Contain the overflow.
- **Auto-advance.** See section 5.
- **Divs with onClick instead of buttons.** Not keyboard reachable, not announced.
- **No `disabled` state at the edges**, so the arrows look live when they do nothing.
- **A percentage card width** in a flex scroller.
- **CSS-only reduced motion.** `scrollBy({behavior:"smooth"})` ignores it — handle it in JS.
- **Card-internal `h3` labels styled like section eyebrows.** They are card labels, not eyebrows;
  the mechanical eyebrow check correctly excludes them, and styling them identically to a real
  section eyebrow blurs a distinction the page relies on.
- **Fewer than four items.** Use a row; a carousel implies more beyond the edge.
- **Hiding the scroll affordance entirely** — no partial card, no arrows, no scrollbar. The strip
  then looks like a truncated grid.
- **Linking to social profiles that do not exist yet.** Ship the real URLs or leave the row out.

## 8. References

- `arianademers-site/src/components/SocialCarousel.tsx` — `atStart`/`atEnd` edge state disabling
  the arrows, `scrollBy` amount of `max(clientWidth * 0.8, 280)`, Phosphor brand glyphs.
- `colinrigney-site/components/SocialCarousel.tsx` — step sized to the first card's real width plus
  the gap, `prefers-reduced-motion` checked in the scroll handler, focusable strip for keyboard
  users, and a file comment stating the page-must-not-scroll-sideways rule outright.

Independently agreed: a `<ul>` strip with `overflow-x-auto` + CSS scroll-snap, swipe as the
primary mobile interaction, desktop-only prev/next as real `aria-label`led buttons, `scrollBy`
with smooth behaviour, fixed-width `shrink-0` cards, and a socials link row beneath the strip.
