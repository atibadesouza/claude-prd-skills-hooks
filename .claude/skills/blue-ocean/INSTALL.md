# Install — Blue Ocean

**This skill runs in Claude Code** (Anthropic's coding app, terminal or desktop). It is **not** for regular Claude at claude.ai — uploading it there may look like it works, but the data pulls will fail. No GitHub. No repositories. No coding.

You need two things: **Claude Code** and a **vidIQ account** (free signup at vidiq.com works). Everything else is automatic.

---

## The install: copy, paste, done

**Step 1.** Unzip `blue-ocean.zip` if it isn't already. Mac users: Safari often unzips it for you, so if you just see a `blue-ocean` folder in Downloads, that's fine. Windows users: right-click the zip → **Extract All** first (if your Explorer address bar still ends in `.zip`, you're browsing inside the zip, not a real folder).

**Step 2.** Open Claude Code and paste this whole box as one message:

```
Install the Blue Ocean skill for me. Do every step yourself and only stop when you need me:

1. Find the "blue-ocean" folder (start in my Downloads). If there's a blue-ocean folder INSIDE another blue-ocean folder, use the inner one. If the folder got renamed like "blue-ocean (1)", rename it back to exactly "blue-ocean". Ignore/delete any __MACOSX folder.
2. Create my personal skills folder if it doesn't exist, and move the folder so this exact file path exists:
   ~/.claude/skills/blue-ocean/SKILL.md   (Windows: %USERPROFILE%\.claude\skills\blue-ocean\SKILL.md)
3. Check Python: try "python3 --version", then "python --version", then "py -3 --version". If one prints Python 3.x, we're good. (If a command answers "Python was not found", that one doesn't count.) If none work, give me the one-click install for my OS and wait.
4. Connect the vidIQ data engine by running:
   claude mcp add --transport http --scope user vidiq https://mcp.vidiq.com/mcp
   then confirm it registered with "claude mcp list".
5. Then tell me to do the only two things you can't:
   a) restart Claude Code (quit and fully reopen),
   b) after restart, type /mcp, select "vidiq", choose "Authenticate", and sign in in the browser (free vidiq.com account works, I can create one right there). If I'm on the Claude desktop app, tell me to use Settings -> Connectors -> vidiq instead.
6. Finish by telling me to say "run blue ocean".
```

Claude will ask permission to run a few commands. **Click Allow / Yes** — that's it doing the install for you.

**Step 3.** Do the two things it asks at the end (restart + sign in to vidIQ). Then say **"run blue ocean."**

That's the whole install.

---

## Manual install (only if you prefer doing it yourself)

**Mac (Terminal):**
```
mkdir -p ~/.claude/skills && mv ~/Downloads/blue-ocean ~/.claude/skills/
claude mcp add --transport http --scope user vidiq https://mcp.vidiq.com/mcp
```
(The `.claude` folder is hidden in Finder — use Cmd+Shift+G and paste `~/.claude/skills` if you go the drag-and-drop route.)

**Windows (PowerShell):**
```
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Move-Item "$env:USERPROFILE\Downloads\blue-ocean" "$env:USERPROFILE\.claude\skills\"
claude mcp add --transport http --scope user vidiq https://mcp.vidiq.com/mcp
```

Then: restart Claude Code → `/mcp` → **vidiq** → **Authenticate** → sign in → say "run blue ocean."

---

## About vidIQ (the data engine)

Blue Ocean's verdict runs on live YouTube data (your channel, real competitors, real search volume) through vidIQ's official MCP server. That's why it's required, without it the report would be guesses.

- **A free vidiq.com account currently works** with the MCP. Usage draws from your plan's monthly AI credits (a typical pull is a handful of credits), and vidIQ may change plan access after their launch period.
- Sign-in happens in your browser on vidiq.com. Claude never sees your password, and you can disconnect anytime at app.vidiq.com → Account Settings → MCP.
- Analyzing **your own channel**? It resolves best if your YouTube channel is connected inside vidIQ (app.vidiq.com → Channel Settings). Optional, Blue Ocean can also just read your public channel link.
- vidIQ's own setup/troubleshooting page: support.vidiq.com/en/articles/15082430-vidiq-mcp

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/blue-ocean` doesn't show up | Quit and fully reopen Claude Code. Check the folder is exactly `~/.claude/skills/blue-ocean/SKILL.md` (not `blue-ocean/blue-ocean/` and not `blue-ocean (1)`). |
| "Zip contains invalid characters" or upload errors | You're uploading to claude.ai. This skill is for **Claude Code**, use the paste-box install above. |
| It asks about GitHub / repositories | Nothing here uses GitHub. Re-paste the install box, it only moves a folder and runs two commands. |
| "Python was not found" | Windows: install Python from the Microsoft Store (one click). Mac: run `python3` once in Terminal and click **Install** on the popup. |
| vidIQ tools still missing after sign-in | Restart Claude Code again, then run `claude mcp list`, `vidiq` should be listed. If not, re-run the `claude mcp add` command from the box above. |
| Browser never opened for sign-in | Run `claude mcp login vidiq` in any terminal, or on the desktop app use Settings → Connectors. |

---
*Part of the Systems by Vic — Skill Vault. Free to share.*
