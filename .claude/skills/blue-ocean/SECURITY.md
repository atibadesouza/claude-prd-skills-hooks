# Blue Ocean — Security & Privacy

Plain-English map of everything this skill does, so you can install it with confidence. Nothing here is hidden.

## What the skill does
1. Asks you a few questions (your channel or your target niche, plus your edge).
2. Pulls public YouTube data through the **VidIQ MCP** (your own VidIQ account).
3. Scans public Google search-suggestion data for demand (no account, no key).
4. Scores the niche against a **local CPM reference table** that ships with the skill.
5. Writes a single **self-contained HTML report** to your computer and opens it in your browser.

That's it. It's a research-and-report tool. It does not post anything, message anyone, or change your channel.

## What it touches on the network
| Destination | Why | Data sent |
|---|---|---|
| **VidIQ MCP** (your account) | Channel stats, competitors, keyword volume | The channel/niche terms you provide |
| **suggestqueries.google.com** | Free "what people search" demand cloud | The niche keyword only |
| **i.ytimg.com** (YouTube thumbnails) | Thumbnails in the report | Nothing, just image fetches |

No other network calls. The fonts and logo are **base64-embedded** in the skill (`assets/assets.json`), so the report never phones home for assets and works fully offline once generated.

## What it does NOT do
- **No telemetry. No analytics. No phone-home.** Nothing about you or your run is sent to the skill author or anyone else.
- **No credential handling.** VidIQ sign-in is standard OAuth in your own browser on vidiq.com. Claude and this skill never see your password, only a revocable token, and you can disconnect anytime at app.vidiq.com → Account Settings → MCP.
- **No background processes.** It runs only when you invoke it, then stops.
- **No writes outside the report.** It creates one HTML file (you choose where) and reads its own bundled files. It does not touch your other files.

## The one setup change it makes
If the vidIQ connector isn't set up yet, the skill runs exactly one command for you:
`claude mcp add --transport http --scope user vidiq https://mcp.vidiq.com/mcp`
That adds vidIQ's official, read-only MCP server (`https://mcp.vidiq.com/mcp`) to your own Claude config file (`~/.claude.json`). It's visible with `claude mcp list` and removable anytime with `claude mcp remove vidiq`. Nothing else on your system is modified.

## What runs on your machine
- **Python 3** (standard library only) for two scripts:
  - `scripts/demand_scan.py` — one HTTP GET loop to Google's public suggest endpoint. No packages, no key.
  - `scripts/build_report.py` — renders the HTML from your data + the bundled assets, then opens it in your default browser (`open` / `start` / `xdg-open`).
- **No third-party Python packages required.** Nothing to `pip install`. Nothing compiled.

## Permissions you're granting
- Network access to the three destinations above.
- Permission to write one HTML file and open it in your browser.
- Use of your existing VidIQ MCP connection.

## Verify it yourself
Everything is plain text you can read before running:
- `scripts/demand_scan.py` and `scripts/build_report.py` are short, commented, dependency-free.
- `assets/assets.json` is just base64-encoded open-license fonts (Anton, Share Tech Mono, Outfit, Grotters) + the logo image.
- The CPM numbers live in `reference/cpm-table.md`.

If anything here doesn't match what you see in the files, trust the files.
