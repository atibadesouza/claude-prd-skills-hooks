---
name: mobile-responsive
description: Transform front-end pages into world-class mobile-friendly, responsive designs and high-performing mobile experiences. Use when making pages responsive, fixing mobile layouts, improving mobile PageSpeed/Lighthouse scores, optimizing touch interactions, reducing mobile LCP/FCP, or ensuring pages work flawlessly on all devices. Triggers on requests like "make this mobile-friendly", "fix mobile layout", "responsive design", "works on phone", "mobile PageSpeed", or "mobile optimization".
---

# Mobile Responsive Design

Transform pages into world-class mobile experiences following modern responsive design principles.

## Core Principles

### Mobile-First Approach
Write base styles for mobile, then enhance for larger screens:

```css
/* Base: Mobile (320px+) */
.container { padding: 1rem; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { padding: 3rem; max-width: 1200px; }
}
```

### Standard Breakpoints
```css
/* Mobile-first breakpoints */
--breakpoint-sm: 640px;   /* Large phones */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktops */
--breakpoint-2xl: 1536px; /* Large screens */
```

## Essential Requirements

### 1. Viewport Meta Tag
Always include in `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Never use `maximum-scale=1` or `user-scalable=no` - these harm accessibility.

### 2. Fluid Typography
```css
/* Fluid type scale */
html {
  font-size: clamp(16px, 1vw + 14px, 20px);
}

h1 { font-size: clamp(2rem, 5vw + 1rem, 3.5rem); }
h2 { font-size: clamp(1.5rem, 3vw + 1rem, 2.5rem); }
h3 { font-size: clamp(1.25rem, 2vw + 1rem, 1.75rem); }

/* Body text: minimum 16px for readability */
body {
  font-size: 1rem;
  line-height: 1.6;
}
```

### 3. Touch Targets
Minimum 44×44px (Apple) or 48×48px (Google) for all interactive elements:

```css
button, a, input, select, textarea {
  min-height: 44px;
  min-width: 44px;
}

/* Adequate spacing between targets */
.nav-links a {
  padding: 12px 16px;
  margin: 4px;
}
```

### 4. Flexible Images
```css
img, video, iframe {
  max-width: 100%;
  height: auto;
}

/* Prevent layout shift */
img {
  aspect-ratio: 16 / 9; /* or actual ratio */
}
```

### 5. No Horizontal Scroll
```css
html, body {
  overflow-x: hidden;
}

/* Use max-width instead of fixed widths */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
```

## Layout Patterns

### Responsive Grid
```css
.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}

/* Auto-fit for truly fluid grids */
.auto-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
}
```

### Flexbox Patterns
```css
/* Stack on mobile, row on desktop */
.flex-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .flex-stack {
    flex-direction: row;
    align-items: center;
  }
}

/* Wrap gracefully */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-wrap > * {
  flex: 1 1 300px; /* Grow, shrink, min-width */
}
```

## Component Patterns

### Mobile Navigation
```css
/* Hamburger menu for mobile */
.nav-toggle {
  display: block;
  background: none;
  border: none;
  padding: 12px;
  cursor: pointer;
}

.nav-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 100;
  padding: 5rem 2rem 2rem;
}

.nav-menu.is-open {
  transform: translateX(0);
}

.nav-menu a {
  display: block;
  padding: 1rem 0;
  font-size: 1.25rem;
  border-bottom: 1px solid #eee;
}

@media (min-width: 768px) {
  .nav-toggle { display: none; }

  .nav-menu {
    position: static;
    transform: none;
    display: flex;
    gap: 2rem;
    padding: 0;
    background: transparent;
  }

  .nav-menu a {
    padding: 0.5rem 0;
    font-size: 1rem;
    border: none;
  }
}
```

### Responsive Tables
```css
/* Card-style on mobile */
@media (max-width: 767px) {
  table, thead, tbody, tr, th, td {
    display: block;
  }

  thead { display: none; }

  tr {
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
  }

  td {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
  }

  td::before {
    content: attr(data-label);
    font-weight: 600;
  }

  td:last-child { border-bottom: none; }
}
```

### Mobile Forms
```css
input, select, textarea {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px; /* Prevents iOS zoom */
  border: 1px solid #ccc;
  border-radius: 8px;
  -webkit-appearance: none;
}

/* Stack labels on mobile */
.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

/* Full-width buttons on mobile */
button[type="submit"] {
  width: 100%;
  padding: 16px;
  font-size: 1rem;
  font-weight: 600;
}

@media (min-width: 768px) {
  button[type="submit"] {
    width: auto;
    min-width: 200px;
  }
}
```

## Performance for Mobile

Mobile optimization means visual quality and load performance. Do not stop after the page merely looks good on a phone. When the user asks for mobile optimization, include a PageSpeed/Lighthouse pass unless they explicitly scope the request to layout only.

### Baseline First

Before changing performance-sensitive code, capture the current mobile bottlenecks:

- Run the repo's normal checks/build commands so you know the framework output shape.
- Use PageSpeed Insights, Lighthouse, or an equivalent local lab run to record mobile score, FCP, LCP, TBT, CLS, Speed Index, and the main opportunities.
- Compare desktop too, especially when touching shared fonts, CSS, routing, or assets.
- Identify the actual LCP element before optimizing. Do not guess.

Good target gates:

- Mobile Performance: 75+ target, 85+ stretch.
- LCP: below 4.5s target, below 2.5s stretch.
- CLS: keep at 0 or near 0.
- TBT: do not regress meaningfully.
- Desktop Performance: keep 90+ unless the user accepts a tradeoff.

### LCP Discovery and Hero Images

For hero/LCP images, the browser must discover the right mobile asset early:

```html
<link
  rel="preload"
  as="image"
  href="/images/hero-mobile.jpg"
  imagesrcset="/images/hero-mobile.webp 430w"
  imagesizes="100vw"
  media="(max-width: 767px)"
  fetchpriority="high"
>

<picture>
  <source media="(max-width: 767px)" type="image/webp" srcset="/images/hero-mobile.webp">
  <source media="(max-width: 767px)" type="image/jpeg" srcset="/images/hero-mobile.jpg">
  <source type="image/webp" srcset="/images/hero-840.webp 840w, /images/hero-1280.webp 1280w" sizes="100vw">
  <img
    src="/images/hero.png"
    width="1680"
    height="936"
    loading="eager"
    fetchpriority="high"
    decoding="async"
    alt=""
  >
</picture>
```

Rules:

- Generate a mobile WebP/AVIF when the current mobile LCP image is JPEG/PNG and savings are meaningful.
- Keep a JPG/PNG fallback for compatibility.
- Set explicit `width`, `height`, or stable aspect-ratio constraints to avoid CLS.
- Use `loading="eager"` and `fetchpriority="high"` only for the likely LCP image, not for below-fold images.
- If the app is client-rendered, consider a lightweight prerender/static fallback shell for the above-fold hero so crawlers and browsers can discover the LCP asset before hydration.
- Preserve visual guardrails. If mobile copy placement exists to reveal a product, person, or featured image, optimize around that rule rather than moving the design casually.

### Fonts and Render Blocking

External font CSS is a common mobile render blocker.

- Remove unused Google Font links and unused preconnects.
- Avoid `@import url(...)` font loading in CSS.
- Self-host only the font families, weights, styles, and subsets actually used.
- Prefer latin variable WOFF2 files when appropriate.
- Define `@font-face` with `font-display: swap`.
- Keep existing font-family tokens/design-system names unchanged when possible so the visual design remains stable.

Example:

```css
@import "tailwindcss";

@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url("/fonts/inter-latin-variable.woff2") format("woff2");
}
```

### Cache Headers

Long-lived static assets help repeat mobile visits and PageSpeed diagnostics.

Use the hosting platform's native header config where possible:

- Hashed build assets: `public, max-age=31536000, immutable`
- Images and fonts: `public, max-age=2592000, stale-while-revalidate=86400`
- Sitemap and frequently regenerated XML/JSON: quickly revalidatable, not immutable

Verify live headers after deploy:

```bash
curl -I https://example.com/assets/app.HASH.js
curl -I https://example.com/images/hero-mobile.webp
curl -I https://example.com/fonts/inter-latin-variable.woff2
curl -I https://example.com/sitemap.xml
```

### Below-Fold JavaScript

Do not ship heavy below-fold code in the first mobile route bundle when it is not needed for the first viewport.

Good candidates for lazy loading:

- Maps, charts, carousels, embeds, modals, large testimonials, admin widgets, and long below-fold sales-letter sections.
- Exit-intent or lead-capture modals, loaded after browser idle.
- Components that depend on heavy libraries such as maps, data visualization, video embeds, or rich animation packages.

Pattern:

```tsx
const HeavySection = lazy(() => import("./HeavySection"));

function LazyHeavySection() {
  const ref = useRef<HTMLDivElement>(null);
  const [shouldLoad, setShouldLoad] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node || !("IntersectionObserver" in window)) {
      setShouldLoad(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setShouldLoad(true);
          observer.disconnect();
        }
      },
      { rootMargin: "600px 0px" },
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref}>
      {shouldLoad ? (
        <Suspense fallback={<ReservedHeightFallback />}>
          <HeavySection />
        </Suspense>
      ) : (
        <ReservedHeightFallback />
      )}
    </div>
  );
}
```

Rules:

- Reserve enough height for lazy sections to avoid CLS.
- Use a root margin around 400px-800px when the section should be ready before the user reaches it.
- Do not lazy-load the header, hero, first CTA, first trust/proof block, or any content needed to understand the first viewport.
- For idle-loaded modals, keep shared event constants in a tiny module so importing the event does not pull in the modal code. If a manual open event fires before idle loading, load immediately and preserve the open action.

### Lazy Loading
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

### Responsive Images
```html
<picture>
  <source media="(max-width: 767px)" srcset="image-mobile.webp">
  <source media="(min-width: 768px)" srcset="image-desktop.webp">
  <img src="image-fallback.jpg" alt="Description">
</picture>

<!-- Or with srcset -->
<img
  srcset="image-320.jpg 320w,
          image-640.jpg 640w,
          image-1024.jpg 1024w"
  sizes="(max-width: 640px) 100vw, 50vw"
  src="image-640.jpg"
  alt="Description"
>
```

### Critical CSS
Inline critical above-fold CSS, defer the rest:
```html
<style>/* Critical CSS here */</style>
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

Use critical CSS carefully:

- Inline only what is required for the first viewport.
- Keep the fallback shell visually close enough that hydration does not produce a jarring jump.
- Do not inline large chunks of the entire stylesheet.

## Testing Checklist

Before shipping, verify:
- [ ] Works at 320px width (smallest phones)
- [ ] Works at 390px and 430px common modern phone widths
- [ ] No horizontal scrolling at any size
- [ ] Text readable without zooming
- [ ] Touch targets 44px+ with adequate spacing
- [ ] Forms usable with mobile keyboards
- [ ] Navigation accessible on mobile
- [ ] Images scale properly
- [ ] Mobile hero/LCP asset is the expected mobile WebP/AVIF/JPG in `currentSrc`
- [ ] LCP image is discovered early through preload or prerendered/static HTML when appropriate
- [ ] Above-fold content does not depend on below-fold lazy chunks
- [ ] Lazy-loaded sections reserve height and do not introduce CLS
- [ ] External font render blockers are removed or justified
- [ ] Static asset cache headers are correct after deploy
- [ ] Mobile Lighthouse/PageSpeed score improves or the remaining bottleneck is documented
- [ ] Desktop score does not regress below the agreed threshold
- [ ] Performance acceptable on slow mobile throttling

## Mobile Performance Case Pattern

When a mobile score is low but desktop is high, prioritize in this order:

1. LCP discovery: preload the real mobile LCP asset, use `fetchpriority="high"`, and add a prerender/static above-fold shell for CSR apps.
2. Image delivery: generate smaller mobile WebP/AVIF variants and keep fallbacks.
3. Font blocking: remove unused external font links and self-host the active WOFF2 font subsets with `font-display: swap`.
4. Below-fold JavaScript: split maps, modals, embeds, and long sections with IntersectionObserver or idle loading.
5. Cache policy: ensure assets, images, and fonts have useful cache headers; keep sitemap/XML revalidatable.
6. Verification: run build/lint, responsive screenshots, local Lighthouse, and live header checks after deploy.

## References

For detailed patterns and examples, see:
- [references/css-patterns.md](references/css-patterns.md) - Complete CSS snippets for common components
- [references/testing-guide.md](references/testing-guide.md) - Device testing and debugging guide
