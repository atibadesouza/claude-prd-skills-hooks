---
name: blue-ocean
description: Tell a creator whether their niche can actually win, what it pays, and the exact premium angle to take, in about a minute. Pulls live YouTube data through the VidIQ MCP, scans real search demand for free, scores the niche against a baked-in CPM table, then renders one decisive verdict (money tier, revenue models, blue-ocean gap, their unfair angle, go / no-go / pivot). Use when the user says "run blue ocean", "should I start a channel about X", "is my niche worth it", "can I make money in this niche", "what's my angle", "size up this niche", "is this niche too saturated", or invokes /blue-ocean.
metadata:
  trigger: Verdict on whether a YouTube niche can win + the premium angle to take
  author: Vic Laranja (built with Claude)
  requires: VidIQ MCP (auto-checked on run), Python 3 (for the free demand scan)
---

# Blue Ocean

Take a creator who is guessing about their niche and hand them a decision. By the end they know three things they did not know a minute ago: whether the niche can make money, how saturated it is, and the one angle that is theirs to own. One screen. Decisive. Premium positioning is the bias the whole skill is built around.

This is not a research dump. VidIQ data, search demand, and CPM ranges are the inputs. The output is a **verdict** the creator can act on today.

## The posture
- **You do the heavy lifting.** The user gives minimal input (their channel or their target niche, plus a quick read on their edge). You pull the data, run the math, and render the call.
- **Decisive, not a survey.** Never end on "it depends." Pick a lane and say why. If the niche is a trap, say so. If the angle is obvious, name it.
- **Premium bias.** The goal is the lane where brands chase them and the CPM is high, not just any open gap. Always steer toward the premium version of the opportunity.
- **Honest, never a promise.** Everything is directional, drawn from public data and published CPM ranges. Never state or imply a guaranteed income. No "you will make $X." Say "creators in this lane tend to earn..." (compliance: this is education, not a forecast).
- **Plain English. No AI tells.** No em-dashes or en-dashes. No "in today's fast-paced world." Talk like a sharp friend who knows the platform. If `stop-slop` is installed, run the final verdict prose through it before presenting.

## Step 0 — VidIQ gate (required, but YOU do the wiring)

VidIQ is the data engine of the verdict. It is **required**. But the user should never have to figure out the setup: you do every step for them, and the only thing they do themselves is sign in.

1. Check whether the VidIQ MCP tools are available (any tool named `...vidiq_...`, e.g. `vidiq_keyword_research`, `vidiq_channel_search`).
2. **If present:** say nothing about it, just proceed.
3. **If missing:** wire it up yourself, right now. Say "One-time setup, I'll do it for you, takes a minute," then:
   a. Run in the shell: `claude mcp add --transport http --scope user vidiq https://mcp.vidiq.com/mcp`
   b. Confirm it registered: `claude mcp list` (look for `vidiq`).
   c. Tell them the ONE thing only they can do, in plain words:
      > "Now the sign-in, the only part I can't do for you. Restart Claude Code (quit and reopen). When it's back, type `/mcp`, pick **vidiq**, choose **Authenticate**. Your browser opens vidIQ's login. Sign in, a **free vidiq.com account works**, create one right there if you don't have one. Then come back and say 'run blue ocean' and I'll take it from the top."
      - If they're in the **desktop app** (no `/mcp` panel): Settings → Connectors → vidiq → sign in. Same result.
      - If the browser doesn't open, they can run `claude mcp login vidiq` in any terminal.
   d. Stop there and wait. New MCP servers only load on restart, so do not pretend to continue.
4. **If they hit a wall** (auth fails, tools still missing after restart): re-run `claude mcp list` to verify the entry survived, re-add if missing, and point them to vidIQ's own setup page: support.vidiq.com/en/articles/15082430-vidiq-mcp

Notes you may need mid-run: a free vidIQ account works with the MCP (usage draws from the plan's monthly AI credits, ~5 per call, so don't spam calls). For channel mode, auto-detection is strongest when their YouTube channel is connected inside vidIQ (app.vidiq.com → Channel Settings), mention it only if their channel won't resolve. Never fake data, if VidIQ isn't connected yet, finish the wiring first.

## Step 0.5 — Python preflight (silent, once per session)

The two bundled scripts need Python 3, but the command name differs by machine. Detect once, remember, reuse:

1. Try `python3 --version`, then `python --version`, then `py -3 --version`.
2. Treat "Python was not found" output as a failure even if the command exists (that's the Windows Store stub).
3. Use whichever worked for every script call this session (`<py> scripts/demand_scan.py ...`).
4. If none work, give the one-click fix and wait: **Mac** → run `python3` once and click Install on the popup (or `xcode-select --install`). **Windows** → install Python from the Microsoft Store (one click), then retry.

## Step 1 — Intake (short, then move)

The very first thing the skill asks, before anything else, is the branch. Nothing is assumed.

**"Are you already posting on YouTube? If yes, drop your channel link. If not, tell me the niche you're eyeing and I'll build it from scratch."**

Wait for the answer, then route. Do not skip ahead to the edge questions until they've said which path they're on.

**If they have a channel:**
- Get the handle or URL.
- Use `vidiq_channel_search` / `vidiq_channel_stats` to pull it, and auto-detect the niche from their content. Confirm the niche back to them in one line ("Reading you as [niche], that right?").

**If they are starting fresh:**
- Ask: **"What niche are you eyeing?"** Get one or two sentences.

Then, either path, run the **unique-value mini-dig** (condensed from the mission-workshop, three questions, do not over-run it):

1. **The mashup** — "What two worlds do you actually live in? Most people in this niche only live in one." (e.g. AI + the scared beginner, fitness + busy dads.)
2. **The edge** — "What can you say in this space that almost nobody else will say out loud?"
3. **The who** — "Who is the one person you can't stand to watch fall behind?"

Keep it tight. You are gathering the raw material for THEIR angle, not running a full identity workshop. If they want to go deeper, point them to `/mission-workshop`.

> Full intake logic and how to handle thin answers: `reference/research-playbook.md`.

## Step 2 — Research (mostly silent, you run it)

Pull the three inputs. Tell them you're "pulling the data" and go quiet, do not narrate every call.

1. **VidIQ** — demand, competition, and what's already winning:
   - `vidiq_keyword_research` on 4 to 6 niche seeds (the niche term + obvious sub-topics) for search volume + competition.
   - `vidiq_similar_channels` / `vidiq_competitors` to build the competitor set.
   - `vidiq_outliers` on the niche to see what is overperforming (overperformers in a niche are gap signals).
   - `vidiq_youtube_search` on the sharpest queries to see how strong the EXISTING content is (weak top results = open lane).
2. **Free demand scan** — the "what is everyone asking" cloud, $0, no key:
   - Run `<py> scripts/demand_scan.py "<niche>"` with the interpreter from the Step 0.5 preflight (add `--yt` for the YouTube-scoped variant, `--gl US` to force US).
   - This reconstructs the AnswerThePublic-style question cloud from Google Autocomplete. Use it to find demand that VidIQ's YouTube-only view misses.
3. **CPM classification** — open `reference/cpm-table.md`, match the niche to its money tier and RPM band. If the exact niche isn't listed, place it by its nearest neighbor and the tier legend.
4. **Revenue-model read** — how creators in this lane actually make money (ads are usually the smallest slice). Detect from competitor descriptions / About pages: paid community (Skool / Patreon / Circle), own product (course / Gumroad / Kajabi), affiliate (links / codes), sponsorships ("sponsored by"), merch. If you can't pull descriptions, ask them to paste 2 to 3 top competitor channel URLs and read those. Heuristics in `reference/research-playbook.md`.

Cross the inputs: **high demand (autocomplete + VidIQ volume) + weak supply (VidIQ outliers / search results) = the blue ocean.** Their mashup and edge decide which blue ocean is actually theirs.

## Step 3 — Build the report dashboard (the payoff)

The output is a **self-contained HTML dashboard**, not a chat message. Build it with `scripts/build_report.py` using the portable asset bundle (`assets/assets.json` — fonts + CV logo base64-embedded, zero external dependencies) and the data you pulled.

The dashboard has a homepage hub + click-to-open panels. It branches on the intake:

**Has a channel** → hub shows channel name (with a ↗ link to open it), real stats, biggest videos ranked by all-time views. Tiles: SWOT · Opportunities (3 suggested avenues) · Competition (3 expandable cards, each with a Visit-channel button) · The Money (tier + platform CPM spectrum) · Your Position · Video Ideas · The Verdict (suggestion + Step 1/2/3).

**No channel** → hub shows the niche as the headline, "opportunity at a glance" stats, and "who's already winning here" (top channels, clickable). Tiles add **The Concept** first (channel name directions, the promise, who it's for, format), then the same SWOT / Opportunities / Competition / Money / Position / Video Ideas / Verdict, all framed as a launch plan.

Rules that make it land:
- **Honest money read.** If the niche is Low tier, say so plainly and point at off-platform monetization. Never hype a low-money niche.
- **Suggestions, not orders.** Opportunities = 3 avenues. Verdict = "our suggestion" + action steps, never a command.
- **Specific, from the data.** Real competitor names, real search queries, real view counts.

## Step 4 — Open it automatically (NON-NEGOTIABLE)

The instant the file is written, **open it in the user's default browser yourself.** Never print a path and tell them to open it. Detect the OS and run:

- **Windows:** `Start-Process "<path>"` (PowerShell) or `cmd /c start "" "<path>"`
- **macOS:** `open "<path>"`
- **Linux:** `xdg-open "<path>"`

Then in chat, give the one-paragraph verdict (the headline call) so they have it without scrolling, and let the dashboard carry the depth. Offer `/mission-workshop` if their angle needs more excavation.

## Building the report (Step 3-4 mechanics)
After the research, assemble a `payload.json` to the contract documented at the top of `scripts/build_report.py`, then run it with the interpreter from the Step 0.5 preflight:

```
<py> scripts/build_report.py payload.json "<output>.html"
```

`build_report.py` embeds the bundled fonts + logo from `assets/assets.json` (self-contained, zero external deps), renders the dashboard for the right mode (channel / fresh), writes the HTML, and **auto-opens it in the default browser**. Pass `--no-open` only when testing.

## Reference files
- `reference/cpm-table.md` — the baked-in CPM / RPM table by niche + the money-tier legend.
- `reference/research-playbook.md` — how to run VidIQ + the demand scan, the alphabet-soup logic, revenue-model detection, handling thin input.
- `scripts/demand_scan.py` — the free Google-autocomplete demand engine (stdlib Python, no API key).
- `scripts/build_report.py` — renders + auto-opens the report from a JSON payload; the payload contract is in its docstring.
- `assets/assets.json` — base64 fonts (Anton, Share Tech Mono, Outfit, Grotters) + CV logo, embedded into every report.
- `SECURITY.md` — plain-English security/privacy map for the people you give this to.
- `reference/verdict-template.md` — legacy one-screen text format (superseded by the dashboard; kept for reference).
