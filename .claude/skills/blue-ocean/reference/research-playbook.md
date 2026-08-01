# Research Playbook

How to actually pull the three inputs and turn them into a verdict. The user should feel like they answered three questions and got a transformation. This file is the engine behind that.

---

## Input 1 — VidIQ (live YouTube data)

Use these tools, in roughly this order. Do not narrate each call, just pull and synthesize.

| Goal | Tool | What to take from it |
|---|---|---|
| Find / confirm their channel | `vidiq_channel_search`, `vidiq_channel_stats` | Niche, size, current performance baseline |
| Build the competitor set | `vidiq_similar_channels`, `vidiq_competitors` | The 5 to 10 channels they're actually up against |
| Read demand + competition | `vidiq_keyword_research` on 4–6 seeds | Search volume + competition score per topic |
| Find what's overperforming | `vidiq_outliers` | Videos punching above their channel size = proven hungry demand |
| Test supply strength | `vidiq_youtube_search` on the sharpest queries | If the top results are weak / old / low-effort, the lane is open |

**Seeds to research:** the niche term itself, plus 3 to 5 obvious sub-topics. For "AI automation" that's "ai agents", "n8n", "ai for small business", "automate my business", etc. Pull volume + competition for each.

**Reading competition from VidIQ:** high volume + low competition = the dream. High volume + high competition = crowded, needs an angle to enter. Low volume = either too early or no real audience, dig into why before recommending it.

---

## Input 2 — Free demand scan (Google Autocomplete)

`<py> scripts/demand_scan.py "<niche>"` (use the interpreter from the Step 0.5 preflight: `python3`, `python`, or `py -3`) returns the full "what is everyone asking" cloud, grouped into questions, comparisons, and general suggestions. This is the exact dataset AnswerThePublic resells, pulled for $0 with no API key.

- Add `--yt` to get YouTube-scoped suggestions (what people type into YouTube specifically). Run both the plain and `--yt` versions and compare. Gaps between them are signal.
- Add `--gl US` to force a US-weighted result (default is CA).
- The **questions** group is gold for the gap analysis. A question that shows up in autocomplete but has weak YouTube answers (check with `vidiq_youtube_search`) is a blue ocean.

How it works under the hood (so you can explain it if asked): it loops the seed keyword through the alphabet (a to z), question words (how / what / why / can / does), and prepositions (for / vs / with), hits Google's suggest endpoint for each, and dedupes the results. That "alphabet soup" rebuilds the whole demand cloud.

---

## Input 3 — Revenue-model read

Ads are usually the smallest slice of income in a high-value niche. The verdict has to show how creators in this lane ACTUALLY make money. Detect it from the competitor set:

| Revenue model | Tells to look for in descriptions / About / links |
|---|---|
| Paid community | Skool, Patreon, Circle, Discord (paid), "join my community" |
| Own product | Course links, Gumroad, Kajabi, Teachable, their own domain, "my program" |
| Affiliate | Amazon links, promo codes, "use my link", "affiliate" disclaimers |
| Sponsorships | "sponsored by", "thanks to X", recurring brand mentions |
| Merch / physical | Merch store, product drops |

If you can pull competitor video descriptions through VidIQ, scan them. If not, ask the user to paste 2 to 3 top competitor channel URLs and read those directly. Report which models dominate the lane, because that tells the creator where the real money is (and whether the audience is one that buys).

---

## Crossing the inputs into a gap

The blue ocean is the intersection:
- **Demand** is high (autocomplete questions + VidIQ search volume), AND
- **Supply** is weak (VidIQ outliers show appetite, but `youtube_search` shows the existing content is thin / old / low-quality).

That intersection is a list of gaps. Their **mashup** and **edge** (from intake) pick which gap is theirs. The one where their two welded worlds let them make content nobody else in the niche can = the premium angle.

---

## Handling thin or messy input

- **Vague niche** ("I want to do business content"): narrow it with one question ("Business for who, doing what?") before researching. A verdict on "business" is useless; a verdict on "AI automation for local service businesses" is sharp.
- **No edge / no mashup yet**: don't force it. Render the money + competition + gap, then say the angle is the missing piece and offer `/mission-workshop` to find it. Honesty beats a fake angle.
- **They picked a Low-tier niche they love**: don't just kill it. Show the money reality, then show the off-platform revenue path (community / product) that makes a Low-ad niche work anyway, IF the demand and a real angle are there. Premium positioning can rescue a low-CPM niche.
- **Niche not in the CPM table**: place it by nearest neighbor, say you're estimating.

---

## The one rule
End on a decision, never on "it depends." The creator came for a verdict. Give them the call and the first move, even if the call is "reconsider, here's why."
