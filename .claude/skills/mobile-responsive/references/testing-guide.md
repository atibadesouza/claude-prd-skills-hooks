# Mobile Testing Guide

Comprehensive guide for testing responsive designs across devices.

## Table of Contents
1. [Device Breakpoints](#device-breakpoints)
2. [Browser DevTools Testing](#browser-devtools-testing)
3. [Real Device Testing](#real-device-testing)
4. [Common Issues & Fixes](#common-issues--fixes)
5. [Performance Testing](#performance-testing)
6. [Accessibility Testing](#accessibility-testing)

---

## Device Breakpoints

### Priority Test Widths

| Width | Device Category | Example Devices |
|-------|-----------------|-----------------|
| 320px | Small phone | iPhone SE, older Android |
| 375px | Standard phone | iPhone 12/13/14, Pixel |
| 414px | Large phone | iPhone Plus/Max, Galaxy S |
| 768px | Tablet portrait | iPad, Galaxy Tab |
| 1024px | Tablet landscape / Laptop | iPad Pro, small laptops |
| 1280px | Desktop | Standard monitors |
| 1440px | Large desktop | Large monitors |

### Must-Pass Widths
At minimum, test these three widths:
1. **320px** - Smallest supported viewport
2. **768px** - Tablet/desktop transition
3. **1024px** - Full desktop

---

## Browser DevTools Testing

### Chrome DevTools

1. Open DevTools: `Cmd+Option+I` (Mac) or `F12` (Windows)
2. Toggle device toolbar: `Cmd+Shift+M` (Mac) or `Ctrl+Shift+M` (Windows)

**Essential features:**
- Device presets dropdown (iPhone, Pixel, iPad, etc.)
- Responsive mode for custom widths
- Throttling for network/CPU simulation
- Touch simulation

**Pro tips:**
- Use "Responsive" mode and drag edges manually
- Test both portrait and landscape orientations
- Enable "Show media queries" to see breakpoint bars

### Firefox DevTools

1. Open DevTools: `Cmd+Option+I` (Mac) or `F12` (Windows)
2. Toggle responsive design mode: `Cmd+Option+M` (Mac) or `Ctrl+Shift+M` (Windows)

**Unique features:**
- Touch event simulation
- DPR (Device Pixel Ratio) testing
- Screenshot tool for each viewport

### Safari DevTools

1. Enable Develop menu: Safari → Preferences → Advanced → "Show Develop menu"
2. Open inspector: `Cmd+Option+I`
3. Enter responsive mode: Develop → Enter Responsive Design Mode

**Best for:**
- Testing iOS-specific issues
- Safari rendering bugs
- WebKit-only features

---

## Real Device Testing

### Why Real Devices Matter

DevTools emulation misses:
- Actual touch behavior and gestures
- Real performance characteristics
- Browser-specific rendering
- Hardware keyboard interactions
- Safe area insets (notches)

### Testing Checklist

**Touch Interactions:**
- [ ] Tap targets are easy to hit
- [ ] No accidental taps on adjacent elements
- [ ] Swipe gestures work naturally
- [ ] Long-press doesn't trigger unexpected actions
- [ ] Scroll is smooth, not janky

**Text Input:**
- [ ] Keyboard doesn't cover input fields
- [ ] Form auto-zoom is prevented (font-size: 16px+)
- [ ] Autocomplete works correctly
- [ ] Password fields trigger password keyboard

**Orientation:**
- [ ] Portrait layout works
- [ ] Landscape layout works
- [ ] Transition between orientations is smooth
- [ ] No content gets cut off

**Safe Areas (for notched devices):**
```css
/* Account for notch and home indicator */
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

### Cloud Testing Services

For testing without physical devices:
- **BrowserStack** - Real device cloud
- **Sauce Labs** - Cross-browser testing
- **LambdaTest** - Budget-friendly option

---

## Common Issues & Fixes

### Horizontal Scroll

**Symptom:** Page scrolls left/right unexpectedly

**Causes & Fixes:**

```css
/* 1. Element wider than viewport */
/* Find the culprit in DevTools: */
* { outline: 1px solid red; }

/* 2. Fixed width on container */
/* Bad: */
.container { width: 1200px; }
/* Good: */
.container { width: 100%; max-width: 1200px; }

/* 3. Negative margins without overflow hidden */
.parent { overflow-x: hidden; }

/* 4. 100vw includes scrollbar width */
/* Bad: */
.full-width { width: 100vw; }
/* Good: */
.full-width { width: 100%; }

/* 5. Nuclear option (use sparingly) */
html, body { overflow-x: hidden; }
```

### iOS Input Zoom

**Symptom:** Page zooms in when focusing form fields

**Fix:** Ensure input font-size is 16px or larger:
```css
input, select, textarea {
  font-size: 16px; /* Prevents iOS zoom */
}
```

### iOS Momentum Scrolling

**Symptom:** Scrollable areas feel choppy on iOS

**Fix:**
```css
.scrollable {
  -webkit-overflow-scrolling: touch;
  overflow-y: auto;
}
```

### Fixed Position Issues on iOS

**Symptom:** Fixed elements jump when keyboard opens

**Fix:**
```css
/* Use position: sticky instead when possible */
.header {
  position: sticky;
  top: 0;
}

/* For true fixed positioning, use visual viewport API */
```

### Tap Highlight on Mobile

**Symptom:** Blue/gray flash when tapping elements

**Fix:**
```css
button, a {
  -webkit-tap-highlight-color: transparent;
}

/* Or style it intentionally */
button, a {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
}
```

### Text Too Small

**Symptom:** Browser complains about tap target/text size

**Fix:**
```css
body {
  font-size: 16px; /* Minimum for body text */
  line-height: 1.5;
}

small, .text-small {
  font-size: 14px; /* Minimum for any text */
}
```

### Images Not Scaling

**Symptom:** Images overflow container or distort

**Fix:**
```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* With aspect ratio preservation */
img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

### Flexbox Overflow

**Symptom:** Flex children don't shrink and overflow

**Fix:**
```css
.flex-child {
  min-width: 0; /* Allow shrinking below content size */
}

/* For text overflow */
.flex-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

---

## Performance Testing

### Lighthouse Mobile Audit

1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Select "Mobile" device
4. Check "Performance" category
5. Run audit

**Target scores:**
- Performance: 90+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

### Core Web Vitals

Test with PageSpeed Insights or web-vitals library:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |

### Network Throttling

Test with slow connections:
1. DevTools → Network tab → Throttling dropdown
2. Select "Slow 3G" or "Fast 3G"
3. Reload and observe load times

**Performance budget:**
- Initial HTML: < 14 KB (fits in first TCP roundtrip)
- Total page weight: < 500 KB on 3G
- Time to Interactive: < 5s on 3G

---

## Accessibility Testing

### Keyboard Navigation

Test without mouse/touch:
- [ ] All interactive elements reachable via Tab
- [ ] Focus order is logical
- [ ] Focus indicator visible
- [ ] No keyboard traps
- [ ] Escape closes modals

### Screen Reader Testing

**VoiceOver (Mac/iOS):**
- Enable: `Cmd+F5` (Mac) or Settings → Accessibility → VoiceOver (iOS)
- Navigate: Swipe or arrow keys
- Activate: Double-tap or `Ctrl+Option+Space`

**TalkBack (Android):**
- Enable: Settings → Accessibility → TalkBack
- Navigate: Swipe gestures
- Activate: Double-tap

**Test for:**
- [ ] Images have descriptive alt text
- [ ] Headings announce correctly
- [ ] Links/buttons describe their purpose
- [ ] Form labels are associated
- [ ] Dynamic content announces changes

### Color Contrast

Use browser extensions or DevTools:
- WCAG AA minimum: 4.5:1 for normal text, 3:1 for large text
- WCAG AAA target: 7:1 for normal text, 4.5:1 for large text

**Chrome DevTools:**
1. Inspect element
2. Click color swatch
3. See contrast ratio and suggestions

### Touch Target Size

Minimum sizes:
- Apple: 44×44 CSS pixels
- Google: 48×48 CSS pixels
- Spacing between targets: 8px minimum

```css
/* Ensure minimum target size */
button, a, input, select {
  min-height: 44px;
  min-width: 44px;
  padding: 12px;
}
```

---

## Quick Testing Script

Run through this checklist for every page:

```
[ ] 320px - No horizontal scroll
[ ] 320px - All content visible
[ ] 320px - Text readable (16px+ body)
[ ] 320px - Touch targets 44px+
[ ] 768px - Layout transitions correctly
[ ] 768px - Navigation works
[ ] 1024px - Desktop layout displays
[ ] Forms - No zoom on focus (iOS)
[ ] Forms - Keyboard doesn't cover inputs
[ ] Images - All scale properly
[ ] Performance - LCP < 2.5s
[ ] Accessibility - Keyboard navigable
```
