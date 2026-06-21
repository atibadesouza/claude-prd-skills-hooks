# CSS Patterns for Mobile-Responsive Design

Complete CSS snippets for common responsive components.

## Table of Contents
1. [Base Reset](#base-reset)
2. [Container System](#container-system)
3. [Typography Scale](#typography-scale)
4. [Navigation Patterns](#navigation-patterns)
5. [Hero Sections](#hero-sections)
6. [Card Layouts](#card-layouts)
7. [Forms](#forms)
8. [Buttons](#buttons)
9. [Modals & Overlays](#modals--overlays)
10. [Footer](#footer)
11. [Utilities](#utilities)

---

## Base Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
}

body {
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
  height: auto;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}
```

---

## Container System

```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 768px) {
  .container { max-width: 768px; }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

@media (min-width: 1280px) {
  .container { max-width: 1200px; }
}

/* Full-bleed container */
.container-fluid {
  width: 100%;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 768px) {
  .container-fluid {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

/* Section spacing */
.section {
  padding-top: 3rem;
  padding-bottom: 3rem;
}

@media (min-width: 768px) {
  .section {
    padding-top: 5rem;
    padding-bottom: 5rem;
  }
}

@media (min-width: 1024px) {
  .section {
    padding-top: 6rem;
    padding-bottom: 6rem;
  }
}
```

---

## Typography Scale

```css
:root {
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, monospace;
}

html {
  font-size: 16px;
}

@media (min-width: 1024px) {
  html { font-size: 18px; }
}

body {
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.7;
  color: #1a1a1a;
}

/* Fluid headings */
h1 {
  font-size: clamp(2rem, 6vw, 3.5rem);
  line-height: 1.1;
  font-weight: 800;
  letter-spacing: -0.02em;
}

h2 {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -0.01em;
}

h3 {
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  line-height: 1.3;
  font-weight: 600;
}

h4 {
  font-size: clamp(1.125rem, 2vw, 1.375rem);
  line-height: 1.4;
  font-weight: 600;
}

/* Paragraph spacing */
p + p { margin-top: 1.5em; }

/* Large lead text */
.lead {
  font-size: clamp(1.125rem, 2vw, 1.375rem);
  line-height: 1.6;
  color: #4a4a4a;
}

/* Small text */
.text-sm { font-size: 0.875rem; }
.text-xs { font-size: 0.75rem; }
```

---

## Navigation Patterns

### Mobile-First Header

```css
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  .header-inner {
    height: 72px;
    padding: 0 2rem;
  }
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: inherit;
  text-decoration: none;
}

/* Hamburger button */
.menu-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
}

.menu-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background: currentColor;
  position: relative;
}

.menu-toggle span::before,
.menu-toggle span::after {
  content: '';
  position: absolute;
  left: 0;
  width: 24px;
  height: 2px;
  background: currentColor;
}

.menu-toggle span::before { top: -8px; }
.menu-toggle span::after { top: 8px; }

@media (min-width: 768px) {
  .menu-toggle { display: none; }
}

/* Mobile menu */
.nav-mobile {
  position: fixed;
  inset: 0;
  background: white;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 100;
  padding: 80px 2rem 2rem;
  overflow-y: auto;
}

.nav-mobile.is-open {
  transform: translateX(0);
}

.nav-mobile a {
  display: block;
  padding: 1rem 0;
  font-size: 1.25rem;
  font-weight: 500;
  color: inherit;
  text-decoration: none;
  border-bottom: 1px solid #eee;
}

.nav-mobile a:hover { color: #0066cc; }

/* Desktop nav */
.nav-desktop {
  display: none;
}

@media (min-width: 768px) {
  .nav-desktop {
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .nav-desktop a {
    font-size: 0.9375rem;
    font-weight: 500;
    color: #4a4a4a;
    text-decoration: none;
    transition: color 0.2s;
  }

  .nav-desktop a:hover { color: #0066cc; }
}

/* Close button for mobile nav */
.nav-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

@media (min-width: 768px) {
  .nav-close { display: none; }
}
```

---

## Hero Sections

```css
.hero {
  min-height: 80vh;
  display: flex;
  align-items: center;
  padding: 4rem 0;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .hero { min-height: 90vh; }

  .hero-content {
    text-align: left;
  }
}

.hero-title {
  margin-bottom: 1.5rem;
}

.hero-description {
  margin-bottom: 2rem;
  color: #666;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 640px) {
  .hero-actions {
    flex-direction: row;
    justify-content: center;
  }
}

@media (min-width: 768px) {
  .hero-actions {
    justify-content: flex-start;
  }
}

/* Hero with background image */
.hero-image {
  position: relative;
  background-size: cover;
  background-position: center;
}

.hero-image::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.hero-image .hero-content {
  position: relative;
  color: white;
}

/* Split hero */
.hero-split {
  display: grid;
  gap: 2rem;
  align-items: center;
}

@media (min-width: 768px) {
  .hero-split {
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
  }
}

.hero-split .hero-media {
  order: -1;
}

@media (min-width: 768px) {
  .hero-split .hero-media {
    order: 1;
  }
}
```

---

## Card Layouts

```css
.cards {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 640px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .cards { grid-template-columns: repeat(3, 1fr); }
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-image {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  width: 100%;
}

.card-body {
  padding: 1.5rem;
}

@media (min-width: 768px) {
  .card-body { padding: 2rem; }
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
}

.card-text {
  color: #666;
  margin-bottom: 1rem;
}

/* Horizontal card on larger screens */
.card-horizontal {
  display: grid;
}

@media (min-width: 768px) {
  .card-horizontal {
    grid-template-columns: 300px 1fr;
  }

  .card-horizontal .card-image {
    aspect-ratio: 1;
    height: 100%;
  }
}
```

---

## Forms

```css
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.9375rem;
}

.form-input,
.form-select,
.form-textarea {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #1a1a1a;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  transition: border-color 0.2s, box-shadow 0.2s;
  -webkit-appearance: none;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.15);
}

.form-input::placeholder {
  color: #9ca3af;
}

/* Prevent iOS zoom on focus */
@media (max-width: 767px) {
  .form-input,
  .form-select,
  .form-textarea {
    font-size: 16px;
  }
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

/* Select arrow */
.form-select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

/* Checkbox & Radio */
.form-check {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  min-height: 44px;
}

.form-check-input {
  width: 20px;
  height: 20px;
  margin-top: 0.125rem;
  flex-shrink: 0;
  accent-color: #0066cc;
}

.form-check-label {
  font-size: 0.9375rem;
  line-height: 1.5;
}

/* Error state */
.form-input.is-invalid {
  border-color: #dc2626;
}

.form-error {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #dc2626;
}

/* Form layout */
.form-row {
  display: grid;
  gap: 1rem;
}

@media (min-width: 640px) {
  .form-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5;
  text-decoration: none;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 44px;
}

/* Full width on mobile */
.btn-block {
  display: flex;
  width: 100%;
}

@media (min-width: 640px) {
  .btn-block {
    display: inline-flex;
    width: auto;
  }
}

/* Primary */
.btn-primary {
  background: #0066cc;
  color: white;
}

.btn-primary:hover {
  background: #0052a3;
}

/* Secondary */
.btn-secondary {
  background: #f3f4f6;
  color: #1a1a1a;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* Outline */
.btn-outline {
  background: transparent;
  border: 2px solid currentColor;
  color: #0066cc;
}

.btn-outline:hover {
  background: #0066cc;
  color: white;
}

/* Sizes */
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  min-height: 36px;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.125rem;
  min-height: 52px;
}

/* Button group - stack on mobile */
.btn-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .btn-group {
    flex-direction: row;
  }
}
```

---

## Modals & Overlays

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.modal-backdrop.is-open {
  opacity: 1;
  visibility: visible;
}

.modal {
  position: fixed;
  z-index: 201;
  background: white;
  overflow-y: auto;

  /* Mobile: full screen */
  inset: 0;
  border-radius: 0;
}

@media (min-width: 640px) {
  .modal {
    /* Tablet+: centered dialog */
    top: 50%;
    left: 50%;
    right: auto;
    bottom: auto;
    transform: translate(-50%, -50%);
    max-width: 500px;
    width: calc(100% - 2rem);
    max-height: calc(100vh - 4rem);
    border-radius: 16px;
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e5e5e5;
  position: sticky;
  top: 0;
  background: white;
}

@media (min-width: 640px) {
  .modal-header {
    padding: 1.5rem;
  }
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 8px;
}

.modal-close:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 1rem;
}

@media (min-width: 640px) {
  .modal-body { padding: 1.5rem; }
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .modal-footer {
    padding: 1.5rem;
    flex-direction: row;
    justify-content: flex-end;
  }
}
```

---

## Footer

```css
.footer {
  background: #1a1a1a;
  color: #a3a3a3;
  padding: 3rem 0 1.5rem;
}

@media (min-width: 768px) {
  .footer { padding: 4rem 0 2rem; }
}

.footer-grid {
  display: grid;
  gap: 2rem;
}

@media (min-width: 640px) {
  .footer-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .footer-grid { grid-template-columns: 2fr repeat(3, 1fr); }
}

.footer-brand {
  margin-bottom: 1rem;
}

.footer-logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.footer-description {
  margin-top: 1rem;
  line-height: 1.6;
}

.footer-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.footer-links {
  list-style: none;
}

.footer-links li { margin-bottom: 0.75rem; }

.footer-links a {
  color: #a3a3a3;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover { color: white; }

.footer-bottom {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid #333;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: center;
}

@media (min-width: 768px) {
  .footer-bottom {
    flex-direction: row;
    justify-content: space-between;
    text-align: left;
  }
}

.footer-social {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@media (min-width: 768px) {
  .footer-social { justify-content: flex-start; }
}

.footer-social a {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #333;
  color: white;
  transition: background 0.2s;
}

.footer-social a:hover { background: #0066cc; }
```

---

## Utilities

```css
/* Visibility */
.hide-mobile {
  display: none !important;
}

@media (min-width: 768px) {
  .hide-mobile { display: block !important; }
  .hide-desktop { display: none !important; }
}

/* Text alignment */
.text-center { text-align: center; }

@media (min-width: 768px) {
  .md-text-left { text-align: left; }
}

/* Spacing */
.mt-auto { margin-top: auto; }
.mb-0 { margin-bottom: 0; }

/* Flex utilities */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-1 { gap: 0.5rem; }
.gap-2 { gap: 1rem; }
.gap-3 { gap: 1.5rem; }

/* Screen reader only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```
