---
name: anchor-nav
category: navigation
dial_compatibility:
  variance: [2, 8]
  motion: [1, 7]
  density: [1, 4]
when_to_use: "One-page sites: personal authority pages, single-offer landing pages, launch pages. Wordmark left, 3-5 anchor links right, exactly one CTA."
not_for: "Multi-level product navigation, mega-menus, or any site with more than about 6 destinations - this block has no dropdown and should not grow one."
stack: ["react", "next", "tailwind", "motion"]
harvested_from: ["arianademers-site/src/components/Nav.tsx", "colinrigney-site/components/Nav.tsx"]
---

# Anchor Nav

A one-line bar: wordmark, a short set of in-page anchors, one action.

## 1. Visual sketch

```
┌──────────────────────────────────────────────────────────────┐
│  Wordmark, Suffix        About  Results  Latest   [ CTA ]    │  64-68px
└──────────────────────────────────────────────────────────────┘
   < 768px:
┌──────────────────────────────────────────────────────────────┐
│  Wordmark                                    [CTA] or [ ≡ ]  │
└──────────────────────────────────────────────────────────────┘
```

## 2. Props API

```ts
type AnchorNavProps = {
  wordmark: React.ReactNode;                  // ReactNode: the suffix is often accent-coloured
  links: { href: string; label: string }[];   // 3-5. more than 6 means this is the wrong block.
  cta: { href: string; label: string };       // exactly one
  mobile?: "menu" | "cta-only";               // see section 4 - a real decision, not a default
  variant?: "solid" | "overlay";              // overlay starts transparent over a full-bleed hero
};
```

## 3. Code sketch

Server Component when `variant="solid"` and `mobile="cta-only"`. That combination needs no JS at
all, and is the right default for a short one-page site.

```tsx
export function Nav({ wordmark, links, cta }) {
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-surface/85 backdrop-blur-md">
      <nav aria-label="Primary"
           className="mx-auto flex h-16 max-w-[1280px] items-center justify-between gap-4 px-5 sm:px-8">
        <a href="#top" className="text-lg font-semibold tracking-tight no-underline">{wordmark}</a>

        <div className="hidden items-center gap-7 md:flex">
          {links.map((l) => (
            <a key={l.href} href={l.href}
               className="text-[0.9rem] font-medium text-muted transition-colors hover:text-ink">
              {l.label}
            </a>
          ))}
          <a href={cta.href}
             className="rounded-[--radius] bg-accent px-3.5 py-2 text-[0.85rem] font-semibold text-on-accent">
            {cta.label}
          </a>
        </div>

        {/* mobile: one primary action, no hamburger */}
        <a href={cta.href}
           className="rounded-[--radius] bg-accent px-3 py-1.5 text-[0.8rem] font-semibold text-on-accent md:hidden">
          {cta.label}
        </a>
      </nav>
    </header>
  );
}
```

**The `overlay` variant** starts transparent over a full-bleed hero and turns solid past a
threshold. Do it with a discrete toggle off the render loop - never per-frame React state:

```tsx
const { scrollY } = useScroll();
useMotionValueEvent(scrollY, "change", (y) => {
  const next = y > 64;
  setScrolled((prev) => (prev === next ? prev : next));   // only re-render on the crossing
});
```

`window.addEventListener('scroll')` for this is a hard-fail in the pre-flight check. `useScroll`,
`ScrollTrigger`, or `IntersectionObserver` are the sanctioned mechanisms.

## 4. Mobile fallback (`< 768px`)

Two legitimate answers, and this is a real decision rather than a default:

- **`cta-only`** - hide the links, keep one action. Correct for a short one-page site where every
  link is reachable by scrolling anyway. Ships zero JS. One harvest source does exactly this and
  says so in a comment.
- **`menu`** - a hamburger opening a full-width panel. Correct once there are 4+ links or any
  destination that is not reachable by scrolling.

If you ship `menu`, the toggle needs `aria-label`, `aria-expanded`, a hit area of at least 44px,
and every link must close the panel on click. All four are easy to miss and all four are bugs.

Nav height stays 64-68px and **one line** at every width - the pre-flight check caps it at 80px.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Solid from the start. No transitions. |
| 4-7 | `overlay` variant: background and text colours cross-fade over ~500ms at the threshold. |
| 8-10 | As above; optionally translate the wordmark suffix in on first load. Do **not** hide the nav on scroll-down and reveal on scroll-up - it is disorienting on a one-page site whose links are anchors. |

Reduced motion: drop the colour transition duration to 0. The nav must never animate its
*height* - that reflows the whole page.

## 6. Dark-mode notes

Needs `surface`, `ink`, `muted`, `accent`, `on-accent`, `line`. The translucent background
(`bg-surface/85 backdrop-blur-md`) must be re-checked in both modes: an 85% white over dark
content reads as fog, and 85% dark over light content can drop link contrast below AA.

The `overlay` variant has a second, easier-to-miss requirement: in its transparent state the
link colour is set by the *hero* behind it, not by the page theme. That is a hero-coupled token
(`on-hero`), and it needs a value for every hero the nav can sit over.

## 7. Anti-patterns

- **A scroll listener** for the solid/transparent toggle. Hard-fail.
- **Per-frame React state** from scroll position. Toggle on threshold crossing only.
- **Two lines at desktop**, or a nav taller than 80px. Both fail the pre-flight check.
- **More than one CTA.** Two actions in a nav means neither is the action.
- **A hamburger for three anchors.** An extra tap to reach something a thumb-flick would have
  reached anyway.
- **A mobile panel that does not close on navigation** - the anchor scrolls behind an open menu.
- **Dropdowns.** If you need one, this is the wrong block.
- **Animating nav height on scroll.** Reflows the page and shifts every anchor target.
- **`fixed` without reserving space** when the hero is not full-bleed: the nav covers the first
  60px of content. Use `sticky` unless the hero is deliberately underneath.

## 8. References

- `arianademers-site/src/components/Nav.tsx` - `overlay` variant: fixed, transparent over a
  full-height dark hero, solid past 64px via `useScroll` + `useMotionValueEvent`, hamburger panel.
- `colinrigney-site/components/Nav.tsx` - `solid` variant: sticky, always opaque, no JS, mobile
  `cta-only` with the reasoning in a comment.

Independently agreed: `<header>` wrapping a labelled `<nav>`, `max-w` container with
`px-5 sm:px-8`, 64-68px single-line height, wordmark left / links+CTA right, links `hidden md:flex`,
and in-page anchor hrefs throughout.
