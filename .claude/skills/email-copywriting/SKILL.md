---
name: email-copywriting
description: Write high-converting email copy — cold outreach, warm re-activation, nurture/launch sequences — in Atiba's direct-response voice, NOT AI/marketing-speak. Use whenever drafting or reviewing any email that goes to a prospect, lead, or list (MMR webclass outreach, ADS, client campaigns). Encodes the rules from Atiba's copywriter-research compendium (Kennedy, Belcher, Halbert, Wiebe) + our own Selling Principles / Medical Ad Trust gates. Invoke BEFORE writing a subject line or body, and to self-score a draft against the checklist gate.
---

# Email Copywriting

Turns email drafts into copy that gets opened, read, and acted on — grounded in Atiba's own research (the copywriter compendium, Drive doc `1Z798geNrtxkbNLb3vc8USAE2dXszbr790HMfIO-NtG8`) and our canon: [[f2-selling-principles]] (the 8-principle floor) + [[medical-ad-trust]] (doctor audiences). **No draft ships until it passes the Checklist Gate at the bottom.**

## The one rule that fixes "heady" and "sounds like AI"

**Specificity, not concepts.** Every adjective is a failure until you replace it with a number, a name, or a concrete image. Wiebe's test: *"Whenever you see 'innovative' or 'excellent,' ask — can I show this instead, or quantify it? Replace 'fast' with 'in 7 minutes.'"* Abstract copy ("using AI in a cash-pay practice") is heady; concrete copy ("fill 6 empty afternoon slots a week") lands. If a line has no number, name, or picture, it is probably filler.

## Subject lines — the single most important element

The subject sells the **open**, not the offer. **Never announce our product/event** ("Physician-only AI class, July 29") — that reads as a promo blast from a stranger and gets deleted. The verbatim failure pattern from the research: *"Live Longer and Better with Our Program"* → *"generic, sounds like wellness spam, not specific or curiosity-piquing."* The fix model: *"52 and feeling 72? Here's how to feel 35 again"* — question + specific numbers + hits the pain + speaks to them.

Rules:
- **Be about THEM, not us.** Their problem, their world — not our offer.
- **Look 1:1**, like one person wrote to one person (not a 5,000-person send).
- **Specific > vague; curiosity or a nerve-hitting question > clever.** A question subject must hit a nerve and NOT be answerable with a flat "no."
- **Short** (≤ ~7 words for cold). No date/product-noun promo markers on cold.
- **No spam tells:** no "free", no ALL-CAPS, no exclamation, no excessive name-personalization (trips filters / feels creepy).

Cold-email formulas that work (adapt, then A/B test — never ship one, test many):
- `Quick question about {practice_name}` — Halbert's proven cold opener; personal, 1:1, curious.
- `Why do good doctors have slow months?` — nerve-hitting question, not yes/no.
- `The {adjective} truth about {pain}` — Halbert "truth about" angle.
- `{specific number}{pain}? {teased fix}` — the "52 and feeling 72" pattern.

## Body — structure & voice

**Spine (compress for email; full sales-letter machinery is for landing pages):**
1. **Voice-of-customer first.** Use their exact words/phrasing (mine reviews, transcripts, DMs). Never invent marketing phrasing.
2. **Hook on the strongest pain or desire, with specificity** — pain in *their* words (PAS: Problem → Agitate → Solution; or HSO: Hook → Story → Offer for warm).
3. **Slippery slide** — each sentence's only job is to get the next one read. Short blocks (1–3 sentences), white space, mobile-skimmable.
4. **"You" ≫ "we"** — ~3:1 ratio. Lead with "you", not our brand name. Talk about them, not us.
5. **One CTA**, benefit-first and (on the button) first-person — "Get my link", not "Submit"/"Click here". For a free/low-commitment ask keep it soft (a question: "Want the link?"). One offer per email.
6. **Reason-why** — give a believable reason for the outreach ("you're a cash-pay practice, so this is built for you"). Answers "why me / why now".
7. **P.S. is prime real estate** — many jump straight to it; restate the core benefit or the one reason to act (use where a signature/P.S. fits the format).

**PAS, the workhorse:** name the pain in their words → agitate (consequences, the cost of the status quo; "it's not your fault" externalizes blame onto the villain — the insurance system, vanity-metric agencies — not the doctor) → solution (every agitated pain gets an equal-and-opposite relief).

## Anti-AI / anti-hype / anti-spam (the deliverability + authenticity layer)

- **Cringe test (Kennedy):** *"Imagine actually speaking the words to a customer; if you'd cringe saying it, rewrite it."*
- **Read it aloud (Wiebe):** if you stumble, the reader stumbles. Copy should sound like a real person talking, not a brochure.
- **Kill your darlings:** *"Don't fall in love with your clever phrasing — if a sentence doesn't move the reader forward, it's dead weight. Cut it."*
- **"So what?" every line** — if it doesn't deliver a benefit or build momentum, cut it.
- **No empty superlatives** ("revolutionary", "world-class", "amazing", "game-changer") — every claim needs a number/proof right behind it, or it's cut. Only ~6–9% believe advertisers; overshoot believability and you lose everyone.
- **Authentic urgency only** — never fake "only 3 spots left". False urgency destroys trust.
- **Two failure modes, both flagged/spam-risky (Atiba 2026-07-21):** (a) *sounds like AI* — stiff, over-structured, "not X but Y", tricolons, em-dash cadence, lines nobody says out loud ("You didn't start your practice to become a marketer"); (b) *sounds like marketing* — reads as an ad. Target the narrow lane of a plain note between two people.

## Cold-email specifics (top-of-funnel, deliverability-sensitive)

- **Break the clutter with something personal/unexpected** in the subject + first line (pattern interrupt), not a sensational claim.
- **Low-commitment first ask** (two-step): don't hard-sell cold. A free class / a reply / a link is the right small "yes"; escalate later.
- **Establish credibility early** — a stranger with a sensational subject and no credible author = deleted as spam. Name who Atiba is in one honest line; make trust visible.
- **CAN-SPAM non-negotiables:** real physical mailing address + working one-click unsubscribe on every send.
- **Plain text**, one CTA/link, ≤120 words, warmed sending inbox (never the core domain).

## A/B testing (how the outreach engine uses this)

The checklist is the **floor**, not a variant — you never A/B "good vs. broken". Every arm must pass the gate, then you test ONE dimension above it (emotional-led vs. analytical-led; villain intensity; peer-proof vs. authority; subject open-loop vs. plain; loss vs. gain CTA). Run each arm to ≥1,000 unique, judge on **send→register** (not opens), significance-gate before promoting, winner becomes control. Enforced in `mmr-webclass-outreach/copy/copy_gate.py`.

## THE CHECKLIST GATE (score every draft; any ✗ = rewrite)

Merged from Kennedy's, Halbert's, and Wiebe's checklists in the research doc:

**Subject**
- [ ] About their problem/world, not our offer; looks 1:1
- [ ] Specific and/or curiosity/nerve-hitting; not a generic announcement
- [ ] No spam tells (free / caps / ! / over-personalization); ≤7 words (cold)

**Body**
- [ ] Opens on the reader's exact pain/desire in *their* words (PAS/HSO)
- [ ] Every adjective replaced by a number, name, or concrete image ("so what?" passes on every line)
- [ ] "You" ≫ "we" (~3:1); leads with "you", not our brand
- [ ] Short blocks, slippery-slide, mobile-skimmable
- [ ] Villain named + externalized; reader is the hero, we're the guide
- [ ] Reason-why for the outreach is present
- [ ] Exactly one CTA, benefit-first, right-sized (soft for a free ask)
- [ ] Credibility/trust made visible early

**Voice / deliverability**
- [ ] Passes the cringe test + read-aloud (sounds like a person, not AI, not an ad)
- [ ] No empty superlatives; no fake urgency; every claim has proof behind it
- [ ] CAN-SPAM: physical address + working unsubscribe present
- [ ] Clears [[f2-selling-principles]] Selling Scorecard (no *Missing*) and, for doctors, [[medical-ad-trust]] gates (Recognition Precision / Hero / Phase Match all > 2)

**Scoring is independent:** the drafting agent should not be the sole scorer of its own voice — voice is the weakest thing an AI self-scores. Route drafts through the engine's **cross-model authenticity panel** (a different model than the writer) + a human spot-check on the first live batch. The market (open/reply/register data) is the final judge.
