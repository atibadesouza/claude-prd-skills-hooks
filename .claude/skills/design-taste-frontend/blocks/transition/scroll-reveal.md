---
name: scroll-reveal
category: transition
dial_compatibility:
  variance: [1, 10]
  motion: [3, 7]
  density: [1, 10]
when_to_use: "Any page where content should enter as it reaches the viewport, to communicate reading sequence. The default motion primitive - wrap sections in it rather than animating each section by hand."
not_for: "MOTION_INTENSITY <= 2 (ship static). Above-the-fold hero content that must be visible on first paint - revealing the hero delays LCP and can leave it invisible if JS fails."
stack: ["react", "next", "tailwind", "motion"]
harvested_from: ["arianademers-site/src/components/Reveal.tsx", "colinrigney-site/components/Reveal.tsx"]
---

# Scroll Reveal

A single measured fade-up as an element enters the viewport, once, never repeating.

Harvested from two shipped sites that solved this the same way structurally and differently
mechanically - which is what makes the structural part trustworthy and the mechanism a real choice.

## 1. Visual sketch

```
   viewport edge
   ─────────────────────────────
                                   element sits 20-24px low, opacity 0
   ─────────────────────────────
   [ element crosses ~15-25% in ]  ->  rises to y:0, opacity 1, ~0.6-0.7s
                                       observer disconnects, never fires again
```

## 2. Props API

```ts
type RevealProps = {
  children: React.ReactNode;
  as?: "div" | "section" | "li" | "figure";  // polymorphic: keeps semantics correct
  delay?: number;                             // stagger siblings; ms or s per mechanism
  className?: string;                         // passthrough, never swallowed
};
```

`as` exists so the wrapper does not force a `<div>` into a `<ul>` or replace a `<section>`.
Both shipped implementations have it. A reveal wrapper that breaks list or landmark semantics
to get an animation is a bad trade.

## 3. Code sketch

Two mechanisms. Both are correct; pick per the stack, not per taste.

**A - Motion library** (use when `motion` is already a dependency):

```tsx
"use client";
import { motion, useReducedMotion, type Variants } from "motion/react";

export function Reveal({ children, className, delay = 0, as = "div" }) {
  const reduce = useReducedMotion();
  const MotionTag = motion[as];
  const variants: Variants = {
    hidden: { opacity: 0, y: 22 },
    show: { opacity: 1, y: 0, transition: { duration: 0.7, delay, ease: [0.16, 1, 0.3, 1] } },
  };
  return (
    <MotionTag
      className={className}
      variants={variants}
      initial={reduce ? false : "hidden"}
      {...(reduce
        ? { animate: "show" }
        : { whileInView: "show", viewport: { once: true, amount: 0.25 } })}
    >
      {children}
    </MotionTag>
  );
}
```

**B - IntersectionObserver + CSS** (use when you do not want a motion dependency):

```tsx
"use client";
import { useEffect, useRef, useState } from "react";

export function Reveal({ children, as: Tag = "div", delay = 0, className = "" }) {
  const ref = useRef<HTMLElement | null>(null);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { setShown(true); io.disconnect(); } });
    }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  const Component = Tag as any;
  return (
    <Component ref={ref} className={`reveal ${className}`} data-shown={shown}
      style={delay ? { transitionDelay: `${delay}ms` } : undefined}>
      {children}
    </Component>
  );
}
```

```css
.reveal { opacity: 0; transform: translateY(22px); transition: opacity .6s, transform .6s; }
.reveal[data-shown="true"] { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
}
```

Both disconnect the observer / set `once: true`. **Neither uses a scroll listener** - that is a
hard-fail in the pre-flight check and there is no reason to reach for one here.

## 4. Mobile fallback (`< 768px`)

No change in behaviour, but reduce the travel: `y: 22` -> `y: 12`. A 22px rise on a 375px-wide
viewport reads as a jolt rather than a reveal. Do **not** disable reveal on mobile - it is where
reading sequence matters most.

Never let the wrapper add horizontal width. `translateY` only; a `translateX` reveal is the most
common cause of a page that scrolls sideways on a phone, which the rendered pre-flight check flags.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | Do not use this block. Ship static. |
| 4-7 | The canonical form above: `y: 22`, ~0.6-0.7s, ease `[0.16, 1, 0.3, 1]`, once. `delay` staggers siblings by 60-90ms. |
| 8-10 | Same entry, plus optional per-child stagger via a parent `staggerChildren: 0.06`. Do **not** add scale, rotation, or blur - the block stays a fade-up; more expressive motion belongs in a different block. |

**Reduced motion is not a nicety here, it is a correctness requirement.** The failure mode is
specific and both sites guard it: the hidden state is server-rendered as `opacity: 0`, so if you
honour `prefers-reduced-motion` by *skipping the animation*, the content stays permanently
invisible. Skip the *transition*, not the *destination* - render at the shown state
(mechanism A: `initial={false}` + `animate="show"`; mechanism B: the CSS media query above).

## 6. Dark-mode notes

The block is token-free by design - it animates opacity and transform only, and inherits every
colour from its children. That is deliberate: a motion primitive that carries colour tokens has to
be re-themed, and this one never does. Nothing to change between modes.

Only caveat: if a child animates `box-shadow`, the shadow token differs per mode. Keep shadows on
the child, not the wrapper.

## 7. Anti-patterns

- **Reduced motion leaving content invisible.** The single most likely bug. See section 5.
- **Wrapping the hero.** Delays LCP and hides the primary message if JS fails or is slow. Both
  shipped sites reveal content *below* the fold and render the hero immediately.
- **Re-firing on every scroll.** Without `once: true` / `io.disconnect()` the page twitches
  whenever the user scrolls back up.
- **A scroll listener.** `window.addEventListener('scroll')` for this is a hard-fail in the
  pre-flight check; IntersectionObserver exists for exactly this.
- **Wrapping every element.** Reveal sections, not paragraphs. A page where all 40 elements
  fade in individually feels broken, not designed.
- **Losing semantics** by forcing a `<div>` where a `<section>` or `<li>` belongs - that is what
  `as` is for.
- **Stagger delays over ~150ms.** The last item arrives after the reader has already looked at it.

## 8. References

Both implementations in this repo's harvest corpus, shipped and pre-flight-clean:

- `arianademers-site/src/components/Reveal.tsx` - Motion variants, `whileInView`, `useReducedMotion`.
- `colinrigney-site/components/Reveal.tsx` - IntersectionObserver, `data-shown`, CSS transition.

Background: MDN IntersectionObserver API; Motion `whileInView` / `viewport` docs; WCAG 2.3.3
Animation from Interactions (the reduced-motion requirement).
