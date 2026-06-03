---
name: media-transcript
description: Use when the user wants a transcript, captions, or subtitles from any video or audio — a YouTube (or other yt-dlp-supported) URL, OR a local audio/video file on disk (.mp3, .wav, .m4a, .mp4, .mkv, .mov, .webm, etc.). Triggers on "transcribe this", "get the transcript/captions/subtitles", "what does this video/audio say".
allowed-tools: Bash,Read,Write
---

# Media Transcript

Get text out of any video or audio, whether it's a URL or a file on disk.

## Step 1: Route — URL or local file?

Look at what the user gave you:

| Input | Path to take |
|-------|--------------|
| A URL (`http://`, `https://`, `youtube.com`, `youtu.be`, etc.) | **YouTube / URL path** (below) — uses yt-dlp |
| A filesystem path or filename (`C:\...`, `./clip.mp4`, `audio.m4a`) | **Local file path** (below) — uses faster-whisper |
| Ambiguous | Ask: "Is that a URL or a file on your computer?" |

These converge on the same goal; only the source differs.

## Local file path (faster-whisper)

The engine is **faster-whisper** (CTranslate2-based). It needs **no PyTorch and no system ffmpeg** — audio decoding is bundled via PyAV, and it reads video files directly (uses only the audio stream). A reusable helper ships with this skill: `transcribe_local.py`.

### 1. Preflight — ensure the engine is installed

```bash
python -c "import faster_whisper" 2>/dev/null && echo INSTALLED || pip install faster-whisper
```

If `pip install` fails, fall back in this order: `pip install faster-whisper` (retry once) → tell the user to install manually. Do **not** reach for `openai-whisper` first — it pulls PyTorch, which often has no wheel for the newest Python.

### 2. Transcribe

```bash
python "<skill-dir>/transcribe_local.py" "PATH_TO_FILE" --format txt --model base
```

- `<skill-dir>` is this skill's folder (where `transcribe_local.py` lives).
- `--format` → `txt` (default), `srt`, or `vtt`. Ask the user if unsure; default to `txt`.
- `--model` → `base` is a good default. Use `small`/`medium` for accuracy on hard audio, `tiny` for speed.
- `--language en` skips auto-detection if you already know the language.
- `--output PATH` to control where it's written (default: `<input-name>.<format>` in the current directory).

The script prints progress to stderr and the **output file path to stdout**. First run downloads the model (~150 MB for `base`), then it's cached.

### 3. Confirm

Tell the user the output path and offer to show the text or convert format.

## YouTube / URL path (yt-dlp)

Prefer existing captions (fast, exact) before transcribing audio.

### 1. Ensure yt-dlp

```bash
command -v yt-dlp || pip install yt-dlp
```

### 2. List, then download captions

```bash
yt-dlp --list-subs "URL"                                              # see what exists
yt-dlp --write-sub --skip-download -o "transcript_temp" "URL"        # manual subs (best)
yt-dlp --write-auto-sub --skip-download -o "transcript_temp" "URL"   # fallback: auto subs
```

Both write a `.vtt`. Restrict languages with `--sub-langs en` if needed.

### 3. If NO captions exist → transcribe the audio

Download audio, then hand it to the **local file path** above (same engine):

```bash
yt-dlp -x --audio-format mp3 -o "audio_%(id)s.%(ext)s" "URL"
python "<skill-dir>/transcribe_local.py" "audio_<id>.mp3" --format txt
```

Show the user the audio size first (`yt-dlp --print "%(duration)s %(title)s" "URL"`) and confirm before a large download.

### 4. Clean VTT → plain text (deduplicated)

YouTube auto-captions repeat lines (progressive display). Deduplicate while keeping order:

```bash
python3 -c "
import re
seen=set()
for line in open('VTT_FILE', encoding='utf-8'):
    line=line.strip()
    if line and not line.startswith(('WEBVTT','Kind:','Language:')) and '-->' not in line:
        clean=re.sub('<[^>]*>','',line).replace('&amp;','&').replace('&gt;','>').replace('&lt;','<')
        if clean and clean not in seen:
            print(clean); seen.add(clean)
" > transcript.txt
```

(faster-whisper output does NOT need this dedup — it has no overlapping cues.)

## Output formats

- `txt` — plain text, best for reading/analysis
- `srt` / `vtt` — timestamped cues, for video players or editing

## Common mistakes

- **Installing openai-whisper for local files** — it needs PyTorch (may have no wheel on new Python). Use faster-whisper.
- **Installing system ffmpeg "to be safe"** — not needed; PyAV is bundled with faster-whisper.
- **Running dedup on faster-whisper output** — only YouTube auto-captions need it.
- **Forgetting `<skill-dir>` is a real path** — substitute the actual folder where `transcribe_local.py` lives.
