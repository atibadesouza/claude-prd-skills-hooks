---
name: aeo-audit
description: Use when auditing, improving, measuring, or operating AEO for a brand, website, article, offer, video, or content plan across Google AI Overviews, Google AI Mode, ChatGPT, Perplexity, Claude, Copilot, Gemini, and other answer engines. Applies AEO principles including SEO fundamentals, training data, real-time retrieval, query fan-out, people-first content, non-commodity content, content structure, freshness, authority, consensus, citations, brand mentions, YouTube visibility, technical crawlability, AI analytics, bot activity, self-reported attribution, ROI, misinformation monitoring, and platform-specific visibility.
---

# AEO Audit

Use this skill to evaluate and improve visibility in AI-generated search answers. Treat AEO as a probability problem: the goal is to increase the odds that an AI system mentions, cites, or accurately describes the brand.

## Core Principles

- AI search draws from both **training data** and **real-time retrieval**.
- Traditional SEO remains foundational because retrieval often depends on search-like discovery.
- For Google Search generative AI features, treat AEO/GEO as SEO applied to AI search experiences, not as a separate hack-based discipline.
- AI prompts can trigger **query fan-out**, where one prompt becomes many synthetic subqueries.
- Optimize for broad topical coverage, not only exact-match keywords, but do not create thin pages for every fan-out variation.
- AI citations are probabilistic, so use **AI visibility** instead of fixed rankings.
- Consensus, freshness, authority, third-party mentions, and source quality can increase citation probability.
- Different platforms cite different ecosystems, so diagnose by platform when possible.
- Content should be people-first and citation-ready: fresh, focused, structured, entity-rich, easy to parse, and genuinely useful.
- Off-site mentions and YouTube assets can be major AEO levers.
- Technical access matters: blocked crawlers, JavaScript-only content, slow pages, and poor structure can reduce AI retrieval.
- AEO measurement needs multiple signals: AI referral traffic, AI bot activity, self-reported attribution, share of voice, cited domains, topic coverage, and sentiment.
- AI referral traffic is usually undercounted; use it for trends, not absolute value.
- AEO value includes direct clicks, prequalified visitors, and brand awareness inside AI conversations.

## Workflow

1. Define the target.
   - Identify the brand, product, topic, page, or offer.
   - Clarify the audience and the AI platforms that matter most.

2. Map likely AI prompts.
   - List buyer, research, comparison, problem-aware, and recommendation-style prompts.
   - Include prompts that mention competitors, alternatives, reviews, pricing, use cases, and risks.

3. Expand into fan-out topics.
   - Break each prompt into adjacent subquestions an AI system might retrieve.
   - Look for missing coverage around definitions, comparisons, examples, pricing, implementation, objections, proof, and next steps.
   - Use fan-out to identify coverage gaps, not to create scaled thin content variants.

4. Audit retrieval readiness.
   - Check whether the target content is crawlable, clear, current, and search-discoverable.
   - Prefer content that directly answers specific subquestions with concise, sourceable sections.
   - Note where traditional SEO improvements would also help AEO.

5. Audit content citation readiness.
   - Check whether each major section uses BLUF: answer first, support after.
   - Confirm important H2 sections are clear and useful on their own for readers and retrieval.
   - Look for entity-rich specificity: named products, brands, categories, tools, places, use cases, and relationships.
   - Prefer clear declarative sentences with one main idea per sentence.
   - Flag stale pages, old comparisons, outdated stats, and sleeper pages with authority but traffic decline.
   - Recommend citation-friendly formats where useful: listicles, comparisons, reviews, "best X," "top X," X-versus-Y, and original data.
   - Check whether content is non-commodity: first-hand experience, expert analysis, original data, practical examples, or a distinct point of view.
   - Reject AI-only rewrites, generic summaries, or pages that would not satisfy a real visitor.

6. Audit consensus and authority.
   - Look for consistent mentions across the brand site, third-party publishers, communities, directories, reviews, podcasts, videos, and social platforms.
   - Identify unsupported claims, conflicting descriptions, outdated information, or thin third-party presence.
   - Prioritize mention opportunities in three tiers: editorial/review/listicle pages, community/Q&A/forum pages, and owned media properties.
   - Recommend authentic mention earning only; do not recommend artificial mention seeding or spam.

7. Audit YouTube visibility.
   - Identify whether YouTube videos already rank for important niche keywords.
   - Prioritize search-hit topics over viral-hit topics.
   - Recommend clear keyword titles, descriptive summaries, timestamps, spoken keywords/entities, and formats matching current search intent.
   - Treat transcripts as both potential citation sources and training examples.

8. Audit technical AEO.
   - Check for AI crawler blocks in `robots.txt`, especially GPTBot, OAI-SearchBot, ClaudeBot, and Google-Extended.
   - Flag JavaScript-only content that may be invisible to some AI crawlers.
   - Note page speed issues that could hurt real-time retrieval.
   - Check heading hierarchy, clean HTML structure, and focused paragraphs.
   - Treat schema as useful SEO support, not a required or guaranteed AI citation lever.
   - Recommend redirects for recurring AI hallucinated URLs that produce 404s.
   - Treat `llms.txt` as optional and low priority unless the user specifically asks for it; Google says special AI text files are not required for generative AI features in Search.
   - For Google AI features, check indexability, snippet eligibility, crawlability, Search Essentials compliance, JavaScript SEO, page experience, and duplicate-content issues.
   - For local and ecommerce sites, check whether business and product details are maintained through appropriate Google surfaces.

9. Audit measurement and analytics.
   - Check whether AI referral traffic is isolated in analytics using known AI sources.
   - Identify which pages receive AI traffic and whether those pages are fresh, accurate, and conversion-ready.
   - Identify important pages that receive no AI traffic and investigate content, crawlability, internal linking, topic demand, or mention gaps.
   - Check whether AI bot activity is available through server logs, CDN logs, or analytics.
   - Separate training bots from search/citation bots where possible.
   - Recommend self-reported attribution in signup, checkout, demo, or post-purchase flows.

10. Audit ROI and progress tracking.
   - Treat raw AI traffic as incomplete and often smaller than SEO traffic.
   - Look for conversion quality, assisted awareness, branded search lift, and self-reported AI influence.
   - Track AI share of voice against competitors.
   - Track cited domains, topic coverage, and mention sentiment over time.
   - Recommend a monthly quick check and quarterly competitive audit.

11. Audit misinformation risk.
   - Check whether AI systems describe the brand accurately, specifically, and positively.
   - Identify vague official information that could allow third-party misinformation to fill the gap.
   - Recommend specific official pages or FAQs with dates, numbers, company facts, pricing, product details, and direct corrections.
   - If misinformation appears, update owned content first, then pursue corrections from third-party sources.

12. Diagnose by platform.
   - **Google AI Overviews:** Prioritize foundational SEO, indexed and snippet-eligible pages, helpful non-commodity content, crawlability, page experience, useful media, and authentic authority signals.
   - **Google AI Mode:** Treat as a Google Search generative AI experience where SEO fundamentals still apply; monitor actual source behavior separately from AI Overviews.
   - **ChatGPT:** Prioritize publisher mentions, editorial authority, knowledge-base clarity, widespread brand associations, and trusted third-party context.
   - **Perplexity:** Prioritize pages that already perform well in search and provide clear citation-worthy answers.

13. Produce the output.
   - Start with the highest-leverage gaps.
   - Separate recommendations into content, SEO, third-party mentions, YouTube, technical access, measurement, misinformation, freshness, authority, and platform-specific actions.
   - Include quick wins and longer-term visibility plays.

## Output Format

When asked for an AEO audit, use this structure:

```markdown
## AEO Snapshot

Brief summary of current AI visibility strengths and weaknesses.

## Likely AI Prompts

- Prompt examples the target should appear for.

## Query Fan-Out Gaps

- Missing subtopics or questions AI systems may retrieve.

## Visibility Factors

- Consensus:
- Freshness:
- Authority:
- Retrieval readiness:
- Content citation readiness:
- Third-party mentions:
- YouTube visibility:
- Technical access:
- Measurement readiness:
- Misinformation risk:

## Platform Notes

- Google AI Overviews:
- Google AI Mode:
- ChatGPT:
- Perplexity:

## Recommended Actions

1. Highest-priority action.
2. Next action.
3. Longer-term action.

## Operating Cadence

- This week:
- Monthly:
- Quarterly:
```

## Guardrails

- Do not treat AEO as a replacement for SEO.
- For Google Search, do not present AEO/GEO as a separate system from SEO; use Google's framing that generative AI search optimization is still optimizing for the search experience.
- Do not claim exact AI ranking positions; describe visibility probability and observed citations instead.
- Do not assume all AI platforms use the same sources.
- When current platform behavior, market share, or citations matter, verify with current research or live checks.
- Keep recommendations practical: every recommendation should help content coverage, retrieval, authority, consensus, freshness, or platform-specific visibility.
- Do not recommend creating separate pages for every query fan-out variation. Avoid scaled thin content.
- Do not recommend content rewritten only for AI systems. Prioritize people-first, non-commodity content.
- Do not overstate chunking. Clear sections help readers and retrieval, but Google does not require tiny AI chunks.
- Do not overstate `llms.txt`, special AI files, or schema as Google AI visibility requirements.
- Do not pursue inauthentic mentions.
- Do not recommend fake freshness. Content updates should be meaningful.
- Do not spam communities for mentions. Recommend useful participation in relevant discussions.
- Do not overstate AI analytics precision. Explain undercounting and attribution gaps.
- Do not judge AEO ROI on referral traffic alone; include conversion quality, self-attribution, brand awareness, and share-of-voice movement.
