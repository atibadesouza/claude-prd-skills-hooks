# Structured Data Examples

JSON-LD templates for common Schema.org types. Copy and customize for implementation.

## Table of Contents
1. [WebSite](#website)
2. [Organization](#organization)
3. [LocalBusiness](#localbusiness)
4. [Article](#article)
5. [Product](#product)
6. [FAQ](#faq)
7. [BreadcrumbList](#breadcrumblist)
8. [HowTo](#howto)
9. [Event](#event)
10. [Video](#video)

---

## WebSite

Basic website schema with sitelinks search box:

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## Organization

Company/brand schema:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Brief company description",
  "foundingDate": "2020",
  "founders": [
    {
      "@type": "Person",
      "name": "Founder Name"
    }
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-800-555-1234",
    "contactType": "customer service",
    "availableLanguage": ["English"]
  },
  "sameAs": [
    "https://www.facebook.com/company",
    "https://twitter.com/company",
    "https://www.linkedin.com/company/company",
    "https://www.instagram.com/company"
  ]
}
```

---

## LocalBusiness

For businesses with physical locations:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/photos/storefront.jpg",
  "url": "https://example.com",
  "telephone": "+1-555-123-4567",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "City",
    "addressRegion": "ST",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "10:00",
      "closes": "14:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "127"
  }
}
```

---

## Article

For blog posts and news articles:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title (max 110 characters)",
  "description": "Brief article description",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2024-01-15T08:00:00+00:00",
  "dateModified": "2024-01-20T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article-url"
  }
}
```

---

## Product

For e-commerce product pages:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": [
    "https://example.com/photos/product-1.jpg",
    "https://example.com/photos/product-2.jpg"
  ],
  "description": "Product description",
  "sku": "SKU12345",
  "mpn": "MPN12345",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.99",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "89"
  },
  "review": {
    "@type": "Review",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": "5",
      "bestRating": "5"
    },
    "author": {
      "@type": "Person",
      "name": "Reviewer Name"
    },
    "reviewBody": "Review text here..."
  }
}
```

---

## FAQ

For FAQ pages (eligible for rich results):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the first question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The answer to the first question goes here. Can include <a href=\"https://example.com\">links</a> and basic HTML."
      }
    },
    {
      "@type": "Question",
      "name": "What is the second question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The answer to the second question."
      }
    },
    {
      "@type": "Question",
      "name": "What is the third question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The answer to the third question."
      }
    }
  ]
}
```

---

## BreadcrumbList

For breadcrumb navigation:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Current Page",
      "item": "https://example.com/category/current-page"
    }
  ]
}
```

---

## HowTo

For instructional content:

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do Something",
  "description": "Brief description of the how-to",
  "image": "https://example.com/photos/how-to.jpg",
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "50"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Supply item 1"
    },
    {
      "@type": "HowToSupply",
      "name": "Supply item 2"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Tool 1"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 Title",
      "text": "Description of step 1",
      "image": "https://example.com/photos/step1.jpg",
      "url": "https://example.com/how-to#step1"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2 Title",
      "text": "Description of step 2",
      "image": "https://example.com/photos/step2.jpg",
      "url": "https://example.com/how-to#step2"
    }
  ]
}
```

---

## Event

For events and webinars:

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Event Name",
  "description": "Event description",
  "image": "https://example.com/photos/event.jpg",
  "startDate": "2025-03-15T19:00:00-05:00",
  "endDate": "2025-03-15T22:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://example.com/event-stream"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Organizer Name",
    "url": "https://example.com"
  },
  "performer": {
    "@type": "Person",
    "name": "Performer Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/tickets",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2025-01-01T00:00:00-05:00"
  }
}
```

---

## Video

For video content:

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video Title",
  "description": "Video description",
  "thumbnailUrl": "https://example.com/photos/thumbnail.jpg",
  "uploadDate": "2024-01-15T08:00:00+00:00",
  "duration": "PT5M30S",
  "contentUrl": "https://example.com/videos/video.mp4",
  "embedUrl": "https://example.com/embed/video",
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

---

## Implementation Notes

1. **Place in `<head>`**: Add JSON-LD in a `<script type="application/ld+json">` tag
2. **One script per type**: Use separate script tags for each schema type
3. **Validate**: Test with [Google Rich Results Test](https://search.google.com/test/rich-results)
4. **Keep updated**: Ensure data matches visible page content
5. **No hidden content**: Schema must reflect what users see
