# Technical SEO Checklist

Complete checklist for auditing page SEO. Use this for comprehensive audits.

## Table of Contents
1. [Indexability & Crawling](#indexability--crawling)
2. [On-Page SEO](#on-page-seo)
3. [Core Web Vitals](#core-web-vitals)
4. [Mobile Optimization](#mobile-optimization)
5. [Security](#security)
6. [International SEO](#international-seo)
7. [E-E-A-T Signals](#e-e-a-t-signals)

---

## Indexability & Crawling

### Critical Checks
- [ ] Page returns 200 status code
- [ ] No `noindex` meta tag or HTTP header
- [ ] No `nofollow` on important internal links
- [ ] Canonical URL points to correct page
- [ ] Page is accessible to Googlebot (test with URL Inspection)

### robots.txt
- [ ] robots.txt exists at /robots.txt
- [ ] Important pages not blocked
- [ ] Sitemap location declared
- [ ] No wildcard blocks affecting important content

### XML Sitemap
- [ ] Sitemap exists and is valid XML
- [ ] All important pages included
- [ ] No 404s or redirects in sitemap
- [ ] Lastmod dates are accurate
- [ ] Sitemap submitted to Google Search Console

### URL Structure
- [ ] URLs are clean and readable
- [ ] No excessive parameters
- [ ] Hyphens used as word separators
- [ ] Lowercase URLs
- [ ] No session IDs in URLs
- [ ] Reasonable URL length (under 100 chars)

---

## On-Page SEO

### Title Tag
- [ ] Present on page
- [ ] 50-60 characters (displays fully in SERP)
- [ ] Primary keyword included
- [ ] Keyword near beginning
- [ ] Unique across site
- [ ] Brand name included (usually at end)
- [ ] Compelling for CTR

### Meta Description
- [ ] Present on page
- [ ] 150-160 characters
- [ ] Contains primary keyword
- [ ] Unique across site
- [ ] Includes call-to-action
- [ ] Accurately describes content

### Heading Structure
- [ ] Single H1 tag
- [ ] H1 contains primary keyword
- [ ] H1 is different from title tag (related but not duplicate)
- [ ] Logical heading hierarchy (no skipping levels)
- [ ] H2s outline main sections
- [ ] Keywords in subheadings (natural, not stuffed)

### Content
- [ ] Adequate word count for topic (check competitors)
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1-2% (natural usage)
- [ ] LSI/related keywords used
- [ ] Original content (not duplicated)
- [ ] Updated/fresh content where relevant
- [ ] No thin content (substantial value)
- [ ] No keyword stuffing

### Internal Links
- [ ] Descriptive anchor text
- [ ] Links to relevant related content
- [ ] Important pages have adequate internal links
- [ ] No broken internal links
- [ ] Reasonable number of links per page

### External Links
- [ ] Links to authoritative sources where appropriate
- [ ] No broken external links
- [ ] rel="nofollow" on untrusted/sponsored links
- [ ] rel="sponsored" on paid links
- [ ] Links open in same tab (unless external resources)

### Images
- [ ] All images have alt text
- [ ] Alt text is descriptive (not stuffed)
- [ ] Decorative images have empty alt=""
- [ ] Optimized file sizes
- [ ] Modern formats (WebP/AVIF with fallbacks)
- [ ] Descriptive file names
- [ ] Width and height attributes set
- [ ] Lazy loading for below-fold images

---

## Core Web Vitals

### LCP (Largest Contentful Paint) - Target: < 2.5s
- [ ] Optimize server response time
- [ ] Use CDN for static assets
- [ ] Preload critical resources
- [ ] Optimize images (largest element is often an image)
- [ ] Remove render-blocking resources
- [ ] Minimize CSS/JS blocking time

### INP (Interaction to Next Paint) - Target: < 200ms
- [ ] Break up long tasks
- [ ] Optimize event handlers
- [ ] Reduce JavaScript execution time
- [ ] Use web workers for heavy computation
- [ ] Implement code splitting
- [ ] Debounce/throttle frequent events

### CLS (Cumulative Layout Shift) - Target: < 0.1
- [ ] Set explicit dimensions on images/videos
- [ ] Reserve space for ads/embeds
- [ ] Avoid inserting content above existing content
- [ ] Use transform animations (not layout-changing)
- [ ] Preload fonts to avoid FOIT/FOUT
- [ ] Avoid dynamically injected content

### Additional Performance
- [ ] Enable compression (gzip/brotli)
- [ ] Leverage browser caching
- [ ] Minimize HTTP requests
- [ ] Use HTTP/2 or HTTP/3
- [ ] Optimize critical rendering path
- [ ] Defer non-critical JavaScript
- [ ] Inline critical CSS

---

## Mobile Optimization

### Viewport & Rendering
- [ ] Viewport meta tag present and correct
- [ ] Content fits viewport without horizontal scroll
- [ ] Text readable without zooming (16px+ base)
- [ ] Responsive design implemented
- [ ] No mobile-specific redirects (use responsive)

### Touch & Interaction
- [ ] Touch targets 48x48px minimum
- [ ] Adequate spacing between touch targets
- [ ] No hover-only interactions
- [ ] Forms are mobile-friendly
- [ ] No Flash or unsupported plugins

### Mobile Content
- [ ] Same content as desktop (no hidden content)
- [ ] Images scale properly
- [ ] Videos are responsive
- [ ] Tables scroll horizontally if needed
- [ ] Pop-ups don't block content

---

## Security

### HTTPS
- [ ] HTTPS enabled site-wide
- [ ] Valid SSL certificate
- [ ] Certificate not expired
- [ ] HTTP redirects to HTTPS
- [ ] No mixed content warnings
- [ ] HSTS header implemented

### Security Headers
- [ ] Content-Security-Policy (CSP)
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options or CSP frame-ancestors
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy for sensitive APIs

---

## International SEO

### Hreflang (if applicable)
- [ ] Hreflang tags present for all language versions
- [ ] Self-referencing hreflang included
- [ ] x-default specified
- [ ] Reciprocal hreflang tags (bidirectional)
- [ ] Valid ISO language/region codes

### Language & Region
- [ ] lang attribute on HTML tag
- [ ] Content matches declared language
- [ ] Currency/pricing localized
- [ ] Date formats localized

---

## E-E-A-T Signals

### Experience
- [ ] First-hand experience demonstrated in content
- [ ] Original photos/videos where relevant
- [ ] Personal insights and examples

### Expertise
- [ ] Author bylines on content
- [ ] Author bio/credentials
- [ ] Links to author profiles
- [ ] Accurate, well-researched content

### Authoritativeness
- [ ] About page exists
- [ ] Contact information available
- [ ] Physical address (for local/business)
- [ ] Social proof (testimonials, reviews)
- [ ] Industry credentials/certifications

### Trustworthiness
- [ ] Privacy policy present
- [ ] Terms of service present
- [ ] Clear ownership/attribution
- [ ] Secure checkout (if e-commerce)
- [ ] Customer service information
- [ ] Accurate, factual content
- [ ] Sources cited where appropriate
