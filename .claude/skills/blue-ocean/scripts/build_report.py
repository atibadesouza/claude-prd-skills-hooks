#!/usr/bin/env python3
"""
build_report.py - render the Blue Ocean Report dashboard from a JSON payload.

Self-contained: embeds the bundled fonts + CV logo (assets/assets.json) as base64,
so the output HTML opens flawlessly on any Mac or PC, offline, with zero external
dependencies (the only web calls are optional YouTube thumbnails / links).

Usage:
    python build_report.py payload.json output.html          # builds + auto-opens
    python build_report.py payload.json output.html --no-open

The skill (Claude) does the research, assembles payload.json to the contract below,
then calls this. See SKILL.md Step 3 for the contract.

PAYLOAD CONTRACT (both modes):
{
  "mode": "channel" | "fresh",
  "header": {"title","title_grad"(opt),"subtitle","badge","visit_url"(channel only)},
  "stats": [{"n","l"} x4],
  "winning": {"type":"videos"|"channels","label","items":[
        videos:   {"vid","title","meta"}
        channels: {"name","subs","tag","cid"} ]},
  "tiles_label": "...",
  "concept": {"promise","names":[..],"rows":[["label","text"],..]}   # fresh mode only
  "swot": {"s":[..],"w":[..],"o":[..],"t":[..]},
  "opportunities": [{"opt","title","body"} x3],
  "competition": [{"name","sub","cid","strength","weakness","beat"} x3],
  "money": {"tier","rpm","cpm","text","spectrum":{"left","width","dot","label"}},
  "position": {"statement","rows":[["label","text"],..]},
  "ideas": [{"title","why"}, ..],
  "verdict": {"tag","text","steps":[..]}
}
"""
import sys, os, json, subprocess, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets", "assets.json")

CSS = r"""
:root{--bg:#08080C;--card:#0F0F16;--ink:#F5F5FA;--grey:#9A9AB2;--muted:#6E6E88;
--line:#ffffff14;--blue:#3a6bff;--purple:#8a3df0;
--f-head:'Anton',Impact,sans-serif;--f-mono:'Share Tech Mono',monospace;--f-body:'Outfit',system-ui,sans-serif;--f-sig:'Grotters',cursive;}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-weight:300;min-height:100vh;-webkit-font-smoothing:antialiased}
.grad{background:linear-gradient(90deg,var(--blue),var(--purple));-webkit-background-clip:text;background-clip:text;color:transparent}
.wrap{max-width:1080px;margin:0 auto;padding:5vh 40px 8vh}
.eyebrow{font-family:var(--f-mono);text-transform:uppercase;font-size:11px;letter-spacing:.24em;color:var(--muted)}
.top{display:flex;align-items:center;gap:14px;margin-bottom:5vh}.top img{width:30px}.top .frag{font-family:var(--f-mono);font-size:10px;letter-spacing:.2em;color:#8fa0ff;text-transform:uppercase;padding-left:10px;border-left:1px solid var(--line)}
.chan{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:20px;border-bottom:1px solid var(--line);padding-bottom:28px;margin-bottom:26px}
.namewrap{display:flex;align-items:center;gap:13px}
.chan h1{font-family:var(--f-head);font-weight:400;font-size:58px;line-height:.92;text-transform:uppercase;letter-spacing:-.01em;max-width:17ch}
.visit{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;border:1px solid var(--line);color:var(--grey);text-decoration:none;font-size:17px;transition:.2s}
.visit:hover{color:var(--ink);border-color:rgba(122,140,255,.5);background:rgba(80,1,214,.12);transform:translateY(-2px)}
.chan .handle{font-family:var(--f-mono);font-size:12px;color:var(--grey);margin-top:12px;letter-spacing:.1em}
.badge{font-family:var(--f-mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;padding:9px 16px;border-radius:100px;border:1px solid var(--line);color:#bfcaff;white-space:nowrap;background:linear-gradient(90deg,rgba(58,107,255,.16),rgba(138,61,240,.16))}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:30px}
.stat .n{font-family:var(--f-head);font-weight:400;font-size:31px;line-height:1}.stat .l{font-family:var(--f-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.sec-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin:26px 0 12px}
.vids{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:36px}
.vid{display:block;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;transition:.2s}
.vid:hover{border-color:rgba(122,140,255,.5);transform:translateY(-3px)}
.vid .th{aspect-ratio:16/9;background:#15151f center/cover;position:relative}
.vid .th::after{content:"\25B6";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#ffffff66;font-size:20px}
.vid .t{font-size:12px;line-height:1.3;padding:10px 11px 4px;font-weight:300}
.vid .v{font-family:var(--f-mono);font-size:10px;color:#8fa0ff;padding:0 11px 11px;letter-spacing:.08em}
.chans{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:36px}
.chcard{display:flex;flex-direction:column;justify-content:space-between;min-height:104px;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:15px;transition:.2s;position:relative}
.chcard:hover{border-color:rgba(122,140,255,.5);transform:translateY(-3px)}
.chcard .cn{font-weight:600;font-size:14px;line-height:1.2}.chcard .cs{font-family:var(--f-mono);font-size:11px;color:#8fa0ff;letter-spacing:.05em;margin-top:9px}.chcard .cv{font-family:var(--f-mono);font-size:10px;color:var(--muted);margin-top:3px}
.chcard .go{position:absolute;top:13px;right:14px;color:var(--muted);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:880px){.grid{grid-template-columns:repeat(2,1fr)}.stats{grid-template-columns:repeat(2,1fr)}.vids,.chans{grid-template-columns:repeat(2,1fr)}.chan h1{font-size:42px}}
.tile{cursor:pointer;display:flex;flex-direction:column;justify-content:space-between;min-height:150px;background:rgba(255,255,255,.025);border:1px solid var(--line);border-radius:16px;padding:18px;transition:.2s;position:relative;overflow:hidden;text-align:left;font:inherit;color:inherit}
.tile:hover{border-color:rgba(122,140,255,.5);background:rgba(80,1,214,.12);transform:translateY(-3px)}
.tile::before{content:"";position:absolute;left:0;top:0;height:3px;width:100%;background:linear-gradient(90deg,var(--blue),var(--purple));opacity:0;transition:.2s}.tile:hover::before{opacity:1}
.tile .mnum{font-family:var(--f-head);font-weight:400;font-size:30px;line-height:1}
.tile .mtitle{font-family:var(--f-head);font-weight:400;font-size:18px;text-transform:uppercase;letter-spacing:.01em;margin-top:auto;line-height:1.05}
.tile .mmeta{font-family:var(--f-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:6px}
footer{margin-top:5vh;font-family:var(--f-mono);font-size:11px;letter-spacing:.1em;color:#45455e;display:flex;align-items:center;gap:8px}footer img{width:16px;opacity:.7}
.panel{position:fixed;inset:0;background:rgba(6,6,10,.86);backdrop-filter:blur(8px);display:none;align-items:flex-start;justify-content:center;padding:6vh 24px;overflow-y:auto;z-index:50}.panel.open{display:flex}
.sheet{max-width:760px;width:100%;background:#0C0C13;border:1px solid var(--line);border-radius:20px;padding:40px;animation:rise .26s ease}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.sheet .x{float:right;cursor:pointer;font-family:var(--f-mono);color:var(--grey);font-size:20px;line-height:1;border:1px solid var(--line);border-radius:8px;padding:4px 10px}.sheet .x:hover{color:var(--ink);border-color:var(--grey)}
.sheet h2{font-family:var(--f-head);font-weight:400;font-size:40px;text-transform:uppercase;line-height:.95;margin-bottom:6px}
.kick{font-family:var(--f-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--blue);margin-bottom:14px}
.sheet p{color:var(--grey);line-height:1.6;margin:10px 0;font-size:15px}.sheet b{color:var(--ink);font-weight:600}
.li{display:flex;gap:12px;padding:13px 0;border-bottom:1px solid var(--line)}.li .d{font-family:var(--f-mono);color:var(--blue);font-size:13px;padding-top:2px;white-space:nowrap}.li p{margin:0}
.namedirs{display:flex;flex-wrap:wrap;gap:10px;margin:4px 0}
.nd{font-family:var(--f-head);font-weight:400;font-size:17px;text-transform:uppercase;letter-spacing:.01em;padding:9px 15px;border:1px solid var(--line);border-radius:10px;background:rgba(255,255,255,.02)}
.money-row{display:flex;gap:34px;margin:18px 0 6px}.money-row .n{font-family:var(--f-head);font-size:40px}.money-row .l{font-family:var(--f-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.swot{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}.swot .q{border:1px solid var(--line);border-radius:14px;padding:18px}
.swot .q h4{font-family:var(--f-mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px}
.swot .s h4{color:#5bd6a0}.swot .w h4{color:#ff6b8a}.swot .o h4{color:#6ba8ff}.swot .t h4{color:#ffcf5b}
.swot ul{list-style:none}.swot li{color:var(--grey);font-size:13px;line-height:1.4;padding:5px 0 5px 14px;position:relative}.swot li::before{content:"";position:absolute;left:0;top:11px;width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.5}
.avenue{border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:12px 0;transition:.2s}.avenue:hover{border-color:rgba(122,140,255,.35);background:rgba(255,255,255,.02)}
.avenue .opt{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--blue)}
.avenue h3{font-family:var(--f-head);font-weight:400;font-size:21px;text-transform:uppercase;margin:7px 0;color:var(--ink)}.avenue p{margin:0;font-size:14px}
.ccard{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:10px 0;cursor:pointer;transition:.2s}.ccard:hover{border-color:rgba(122,140,255,.4)}
.ccard .ch{display:flex;justify-content:space-between;align-items:center}.ccard .nm{font-weight:600;font-size:16px}.ccard .pl{font-family:var(--f-mono);color:var(--blue);transition:.2s}.ccard.open .pl{transform:rotate(45deg)}
.ccard .sub{font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-top:3px}.ccard .dt{max-height:0;overflow:hidden;transition:max-height .3s;font-size:13px;color:var(--grey);line-height:1.55}.ccard.open .dt{max-height:360px;margin-top:12px}
.visitc{display:inline-flex;align-items:center;gap:6px;margin-top:13px;font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#bfcaff;text-decoration:none;border:1px solid var(--line);border-radius:8px;padding:7px 12px;transition:.2s}.visitc:hover{border-color:rgba(122,140,255,.5);background:rgba(80,1,214,.12)}
.idea{display:flex;gap:13px;align-items:flex-start;padding:14px 0;border-bottom:1px solid var(--line)}.idea .n{font-family:var(--f-head);color:transparent;background:linear-gradient(135deg,var(--blue),var(--purple));-webkit-background-clip:text;background-clip:text;font-size:22px;line-height:1}.idea .t{font-weight:600;font-size:15px}.idea .why{color:var(--muted);font-size:12px;font-family:var(--f-mono);margin-top:3px;letter-spacing:.04em}
.spectrum{margin-top:26px}.track{position:relative;height:12px;border-radius:100px;background:linear-gradient(90deg,#1a1a26,#222232);border:1px solid var(--line);margin:34px 0 12px}
.band{position:absolute;top:-1px;bottom:-1px;border-radius:100px;background:linear-gradient(90deg,var(--blue),var(--purple));box-shadow:0 0 18px rgba(80,1,214,.6)}
.dot{position:absolute;top:50%;width:15px;height:15px;border-radius:50%;background:#fff;transform:translate(-50%,-50%);box-shadow:0 0 0 4px rgba(255,255,255,.13)}
.youlab{position:absolute;top:-27px;transform:translateX(-50%);font-family:var(--f-mono);font-size:10px;letter-spacing:.1em;color:#fff;white-space:nowrap}
.scale{display:flex;justify-content:space-between;font-family:var(--f-mono);font-size:10px;letter-spacing:.06em;color:var(--muted)}
.verdict{margin-top:8px;border:1px solid rgba(122,140,255,.4);border-radius:14px;padding:22px;background:linear-gradient(90deg,rgba(58,107,255,.08),rgba(138,61,240,.08))}
.verdict .opt{font-family:var(--f-mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#bfcaff;margin-bottom:6px}.verdict .tag{font-family:var(--f-head);font-size:30px}
.sig{font-family:var(--f-sig);font-size:30px;transform:rotate(-3deg);display:inline-block;margin:18px 0 6px}
"""

def esc(s): return _html.escape(str(s), quote=True)

def faces_css(assets):
    fam={"anton":"Anton","sharetechmono":"Share Tech Mono","outfit":"Outfit","grotters":"Grotters"}
    out=[]
    for key,items in assets["fonts"].items():
        for it in items:
            fmt="woff2" if it["fmt"]=="woff2" else "ttf"
            out.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:block;src:url(data:font/%s;base64,%s) format('%s');}"%(fam[key],it["weight"],fmt,it["b64"],it["fmt"]))
    return "\n".join(out)

def li(label,text): return '<div class="li"><div class="d">%s</div><p>%s</p></div>'%(esc(label),text)
def panel(pid,kick,title,inner):
    return ('<div class="panel" id="%s"><div class="sheet"><span class="x" onclick="cl(\'%s\')">&times;</span>'
            '<div class="kick">%s</div><h2>%s</h2>%s</div></div>'%(pid,pid,esc(kick),esc(title),inner))

def build(payload, assets):
    mode = payload.get("mode","fresh")
    h = payload["header"]
    LOGO = assets["logo"]

    # header
    title = esc(h["title"])
    if h.get("title_grad"):
        g=esc(h["title_grad"]); title = title.replace(g, '<span class="grad">%s</span>'%g)
    if mode=="channel" and h.get("visit_url"):
        name_html = ('<div class="namewrap"><h1>%s</h1><a class="visit" href="%s" target="_blank" rel="noopener" title="Open channel">&#8599;</a></div>'
                     % (title, esc(h["visit_url"])))
        frag=""
    else:
        name_html = "<h1>%s</h1>"%title
        frag='<div class="frag">Starting from scratch</div>'
    stats = "".join('<div class="stat"><div class="n">%s</div><div class="l">%s</div></div>'%(s["n"],esc(s["l"])) for s in payload["stats"])

    # winning row
    w=payload["winning"]
    if w["type"]=="videos":
        items="".join('<a class="vid" href="https://youtube.com/watch?v=%s" target="_blank" rel="noopener"><div class="th" style="background-image:url(https://i.ytimg.com/vi/%s/mqdefault.jpg)"></div><div class="t">%s</div><div class="v">%s</div></a>'
                      %(esc(i["vid"]),esc(i["vid"]),esc(i["title"]),esc(i["meta"])) for i in w["items"])
        win='<div class="vids">%s</div>'%items
    else:
        items="".join('<a class="chcard" href="https://youtube.com/channel/%s" target="_blank" rel="noopener"><div class="go">&#8599;</div><div class="cn">%s</div><div class="cs">%s</div><div class="cv">%s</div></a>'
                      %(esc(i["cid"]),esc(i["name"]),esc(i["subs"]),esc(i["tag"])) for i in w["items"])
        win='<div class="chans">%s</div>'%items

    # tiles + panels (order depends on mode)
    panels=[]; tiles=[]
    def add(num,t,meta,pid): tiles.append((num,t,meta,pid))
    n=1
    if mode=="fresh":
        c=payload["concept"]
        inner='<div class="kick">The one-line promise</div><p style="font-size:18px;color:var(--ink)">%s</p>'%esc(c["promise"])
        inner+='<div class="kick" style="margin-top:20px">Channel name directions &mdash; starting points, not final</div>'
        inner+='<div class="namedirs">%s</div>'%"".join('<span class="nd">%s</span>'%esc(x) for x in c["names"])
        inner+="".join(li(r[0],esc(r[1])) for r in c["rows"])
        panels.append(panel("p_concept","Your channel, defined from the market","The Concept",inner))
        add("%02d"%n,"The Concept","Your channel, defined","p_concept"); n+=1

    sw=payload["swot"]
    def ul(x): return "<ul>%s</ul>"%"".join("<li>%s</li>"%esc(i) for i in x)
    inner=('<div class="swot"><div class="q s"><h4>Strengths</h4>%s</div><div class="q w"><h4>Weaknesses</h4>%s</div>'
           '<div class="q o"><h4>Opportunities</h4>%s</div><div class="q t"><h4>Threats</h4>%s</div></div>'
           %(ul(sw["s"]),ul(sw["w"]),ul(sw["o"]),ul(sw["t"])))
    panels.append(panel("p_swot","Honest mirror","SWOT",inner)); add("%02d"%n,"SWOT","Honest mirror","p_swot"); n+=1

    inner="<p>Not a directive, three real openings the data surfaced. Pick the one that feels most like you:</p>"
    inner+="".join('<div class="avenue"><div class="opt">%s</div><h3>%s</h3><p>%s</p></div>'%(esc(o["opt"]),esc(o["title"]),esc(o["body"])) for o in payload["opportunities"])
    panels.append(panel("p_opp","3 paths you could take &mdash; based on the market","Opportunities",inner)); add("%02d"%n,"Opportunities","3 paths you could take","p_opp"); n+=1

    inner="".join('<div class="ccard" onclick="this.classList.toggle(\'open\')"><div class="ch"><div><div class="nm">%s</div><div class="sub">%s</div></div><div class="pl">+</div></div>'
                  '<div class="dt"><b>Strength:</b> %s<br><b>Weakness:</b> %s<br><b>How you beat them:</b> %s'
                  '<br><a class="visitc" href="https://youtube.com/channel/%s" target="_blank" rel="noopener" onclick="event.stopPropagation()">Visit channel &#8599;</a></div></div>'
                  %(esc(c["name"]),esc(c["sub"]),esc(c["strength"]),esc(c["weakness"]),esc(c["beat"]),esc(c["cid"])) for c in payload["competition"])
    panels.append(panel("p_comp","Who's already winning &mdash; tap to expand","Competition",inner)); add("%02d"%n,"Competition","Who you're up against","p_comp"); n+=1

    m=payload["money"]; sp=m["spectrum"]
    inner=('<div class="money-row"><div><div class="n grad">%s</div><div class="l">Money tier</div></div>'
           '<div><div class="n">%s</div><div class="l">RPM (NA)</div></div><div><div class="n">%s</div><div class="l">CPM</div></div></div>'
           '<p>%s</p><div class="kick" style="margin-top:8px">Where this niche sits on the whole platform</div>'
           '<div class="spectrum"><div class="track"><div class="band" style="left:%s;width:%s"></div>'
           '<div class="youlab" style="left:%s">%s</div><div class="dot" style="left:%s"></div></div>'
           '<div class="scale"><span>$1 &middot; Music (floor)</span><span>$60 &middot; Insurance (ceiling)</span></div></div>'
           %(esc(m["tier"]),esc(m["rpm"]),esc(m["cpm"]),m["text"],sp["left"],sp["width"],sp["dot"],esc(sp["label"]),sp["dot"]))
    panels.append(panel("p_money","Tier &amp; spectrum","The Money",inner)); add("%02d"%n,"The Money","Tier &amp; spectrum","p_money"); n+=1

    pos=payload["position"]
    inner='<div class="kick">Positioning statement</div><p style="font-size:18px;color:var(--ink)">%s</p>'%esc(pos["statement"])
    inner+="".join(li(r[0],esc(r[1])) for r in pos["rows"])
    inner+='<p style="font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-top:14px">This is the self-serve version of the Systems by Vic onboarding game plan.</p>'
    panels.append(panel("p_pos","The plan","Your Position",inner)); add("%02d"%n,"Your Position","The plan","p_pos"); n+=1

    inner="<p>Each welds real search demand to your angle:</p>"+"".join('<div class="idea"><div class="n">%02d</div><div><div class="t">%s</div><div class="why">// %s</div></div></div>'%(i+1,esc(v["title"]),esc(v["why"])) for i,v in enumerate(payload["ideas"]))
    panels.append(panel("p_ideas","Try these next","Video Ideas",inner)); add("%02d"%n,"Video Ideas","Try these next","p_ideas"); n+=1

    vd=payload["verdict"]
    inner=('<div class="verdict"><div class="opt">Our suggestion</div><div class="tag grad">%s</div><p>%s</p></div>'
           '<div class="kick" style="margin-top:22px">Action steps</div>'%(esc(vd["tag"]),vd["text"]))
    inner+="".join(li("Step %d"%(i+1),esc(s)) for i,s in enumerate(vd["steps"]))
    inner+='<div class="sig">Blue Ocean</div><p style="font-family:var(--f-mono);font-size:10px;color:var(--muted)">Directional read from public data + published CPM ranges. Not an income guarantee.</p>'
    panels.append(panel("p_verdict","Our suggestion","The Verdict",inner)); add("%02d"%n,"The Verdict","Our suggestion","p_verdict"); n+=1

    tiles_html="".join('<button class="tile" onclick="op(\'%s\')"><div class="mnum">%s</div><div><div class="mtitle">%s</div><div class="mmeta">%s</div></div></button>'%(pid,num,esc(t),meta) for num,t,meta,pid in tiles)

    HEAD='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blue Ocean Report</title><style>%s%s</style></head><body>'%(faces_css(assets),CSS)
    BODY=('<div class="wrap"><div class="top"><img src="data:image/png;base64,%s" alt="CV"><div class="eyebrow">Blue Ocean Report</div>%s</div>'
          '<div class="chan"><div>%s<div class="handle">%s</div></div><div class="badge">%s</div></div>'
          '<div class="stats">%s</div><div class="sec-lab">%s</div>%s'
          '<div class="sec-lab">%s</div><div class="grid">%s</div>'
          '<footer><img src="data:image/png;base64,%s" alt="CV">Generated by Blue Ocean &middot; Systems by Vic</footer></div>%s'
          %(LOGO,frag,name_html,esc(h["subtitle"]),esc(h["badge"]),stats,esc(w["label"]),win,esc(payload["tiles_label"]),tiles_html,LOGO,"".join(panels)))
    SCRIPT=("<script>function op(i){document.getElementById(i).classList.add('open');document.body.style.overflow='hidden'}"
            "function cl(i){document.getElementById(i).classList.remove('open');document.body.style.overflow=''}"
            "addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.panel.open').forEach(p=>cl(p.id))});"
            "document.querySelectorAll('.panel').forEach(p=>p.addEventListener('click',e=>{if(e.target===p)cl(p.id)}));</script></body></html>")
    return HEAD+BODY+SCRIPT

def open_in_browser(path):
    try:
        if sys.platform.startswith("win"): os.startfile(os.path.abspath(path))
        elif sys.platform=="darwin": subprocess.run(["open",path],check=False)
        else: subprocess.run(["xdg-open",path],check=False)
        return True
    except Exception as e:
        print("auto-open failed (%s); open the file manually: %s"%(e,path)); return False

def main():
    args=[a for a in sys.argv[1:]]
    if len(args)<2:
        print("usage: python build_report.py payload.json output.html [--no-open]"); sys.exit(1)
    payload=json.load(open(args[0],encoding="utf-8"))
    assets=json.load(open(ASSETS,encoding="utf-8"))
    out=args[1]
    open(out,"w",encoding="utf-8").write(build(payload,assets))
    print("report written: %s"%os.path.abspath(out))
    if "--no-open" not in args:
        if open_in_browser(out): print("opened in default browser")

if __name__=="__main__":
    main()
