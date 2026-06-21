---
name: seo-audit
description: Audit external front-facing pages for SEO optimization and modern web standards. Use when checking if a public webpage follows Google's best practices, analyzing Core Web Vitals, reviewing meta tags, structured data, mobile-friendliness, or any SEO-related analysis. Triggers on requests like "check SEO", "audit this page", "is this page optimized", "review for search engines", or "check Google ranking factors".
---

# SEO Audit Skill

Audit public webpages for SEO optimization following Google's 2024-2025 standards and best practices.

## Quick Start

To audit a page:

1. Fetch the page using WebFetch or browser tools
2. Run through the audit checklist below
3. Report findings with severity levels and actionable fixes

## Audit Categories

### 1. Critical SEO Elements

**Title Tag**
- Present and unique (50-60 characters optimal)
- Contains primary keyword near the beginning
- Compelling for click-through

**Meta Description**
- Present (150-160 characters optimal)
- Contains primary keyword naturally
- Includes call-to-action

**Canonical URL**
- Self-referencing canonical present
- No duplicate content issues

**Robots Directives**
- No accidental `noindex` or `nofollow`
- Check `<meta name="robots">` and HTTP headers

### 2. Content Structure

**Heading Hierarchy**
- Single H1 tag containing primary keyword
- Logical H2-H6 nesting (no skipped levels)
- Keywords distributed naturally in headings

**Content Quality Signals**
- Sufficient word count (aim for comprehensive coverage)
- No thin content pages
- Original, valuable content

**Internal Linking**
- Descriptive anchor text (not "click here")
- Logical site structure reflected

### 3. Technical SEO

**Page Speed (Core Web Vitals)**
- LCP (Largest Contentful Paint): < 2.5 seconds
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Mobile-Friendliness**
- Viewport meta tag present: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Touch targets adequately sized (48x48px minimum)
- No horizontal scrolling
- Readable font sizes (16px+ base)

**Security**
- HTTPS enabled
- No mixed content warnings
- HSTS header recommended

**Crawlability**
- robots.txt accessible and correct
- XML sitemap present and valid
- No orphan pages

### 4. Structured Data (Schema.org)

**Recommended Schema Types**
- Organization/LocalBusiness for company sites
- Article/BlogPosting for content
- Product for e-commerce
- FAQ for question pages
- BreadcrumbList for navigation
- WebPage/WebSite basics

**Validation**
- Valid JSON-LD format (preferred over microdata)
- No errors in Google Rich Results Test
- Required properties present for each type

### 5. Social & Sharing

**Open Graph Tags**
```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

**Twitter Cards**
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### 6. Images & Media

**Image Optimization**
- Alt text present and descriptive
- Modern formats (WebP, AVIF with fallbacks)
- Lazy loading for below-fold images
- Explicit width/height to prevent CLS
- Responsive images with srcset

### 7. Accessibility (SEO-Impacting)

- Proper heading structure
- Alt text for images
- Sufficient color contrast
- Keyboard navigable
- ARIA labels where needed

## Audit Report Format

Present findings using this structure:

```
## SEO Audit: [Page URL]

### Score: [X/100]

### Critical Issues (Fix Immediately)
- [Issue]: [Current state] → [Recommendation]

### Warnings (Should Fix)
- [Issue]: [Current state] → [Recommendation]

### Passed Checks
- [Check name]: ✓

### Opportunities
- [Suggestion for improvement]
```

## Severity Levels

| Level | Description | Impact |
|-------|-------------|--------|
| Critical | Blocks indexing or severely hurts rankings | Fix immediately |
| Warning | Negatively impacts SEO performance | Fix soon |
| Info | Best practice not followed | Consider fixing |
| Passed | Meets or exceeds standards | No action needed |

## References

For detailed checklists and code examples, see:
- [references/technical-checklist.md](references/technical-checklist.md) - Complete technical SEO checklist with 50+ checks
- [references/schema-examples.md](references/schema-examples.md) - Structured data templates for common page types
