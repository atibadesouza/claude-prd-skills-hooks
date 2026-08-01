#!/usr/bin/env python3
"""
demand_scan.py - free search-demand scan via Google Autocomplete.

Reconstructs the "what is everyone asking" cloud (the dataset AnswerThePublic
and AlsoAsked resell) for $0, no API key. Used by the niche-verdict skill to
find demand and blue-ocean gaps that VidIQ's YouTube-only view misses.

Usage:
    python demand_scan.py "ai automation"
    python demand_scan.py "ai automation" --yt          # YouTube-scoped suggestions
    python demand_scan.py "ai automation" --gl US        # force US weighting
    python demand_scan.py "ai automation" --yt --gl US

Output: JSON grouped into questions / comparisons / general, plus a total count.
Stdlib only. No dependencies, no key.
"""
import sys
import json
import time
import urllib.parse
import urllib.request

MODIFIERS = list("abcdefghijklmnopqrstuvwxyz")
QUESTIONS = ["how", "what", "why", "when", "where", "which", "who",
             "can", "does", "do", "is", "are", "should", "will"]
PREPS = ["for", "vs", "versus", "with", "without", "near", "like", "to", "or"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def fetch(query, gl="CA", hl="en", yt=False):
    params = {"client": "firefox", "q": query, "hl": hl, "gl": gl}
    if yt:
        params["ds"] = "yt"
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("utf-8", "ignore")
        data = json.loads(raw)
        return data[1] if len(data) > 1 else []
    except Exception:
        return []


def classify(sug):
    s = sug.lower().strip()
    first = s.split(" ")[0] if s else ""
    if first in QUESTIONS or any(" " + q + " " in " " + s + " " for q in QUESTIONS):
        return "questions"
    if " vs " in s or " versus " in s or s.endswith(" or") or " or " in s:
        return "comparisons"
    return "general"


def scan(seed, gl="CA", hl="en", yt=False):
    seen = set()
    groups = {"questions": [], "comparisons": [], "general": []}
    seeds = [seed]
    seeds += [seed + " " + m for m in MODIFIERS]
    seeds += [q + " " + seed for q in QUESTIONS]
    seeds += [seed + " " + p for p in PREPS]

    for s in seeds:
        for sug in fetch(s, gl=gl, hl=hl, yt=yt):
            key = sug.lower().strip()
            if not key or key in seen:
                continue
            seen.add(key)
            groups[classify(sug)].append(sug)
        time.sleep(0.2)

    return {
        "seed": seed,
        "scope": "youtube" if yt else "google",
        "geo": gl,
        "total": len(seen),
        "questions": sorted(groups["questions"]),
        "comparisons": sorted(groups["comparisons"]),
        "general": sorted(groups["general"]),
    }


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print('usage: python demand_scan.py "niche keyword" [--yt] [--gl US]')
        sys.exit(1)
    seed = args[0]
    yt = "--yt" in args
    gl = "CA"
    if "--gl" in args:
        try:
            gl = args[args.index("--gl") + 1]
        except IndexError:
            pass
    out = scan(seed, gl=gl, yt=yt)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
