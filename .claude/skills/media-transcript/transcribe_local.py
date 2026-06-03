#!/usr/bin/env python3
"""Transcribe a local audio OR video file to text using faster-whisper.

Why faster-whisper: it uses CTranslate2 (not PyTorch), so it installs cleanly
on new Python versions, and it bundles audio decoding via PyAV (no system
ffmpeg required). Video files work directly — only the audio stream is used.

Usage:
    python transcribe_local.py INPUT [--model base] [--format txt] [--language auto] [--output PATH]

Formats: txt (plain, default), srt, vtt
Models:  tiny | base | small | medium | large-v3  (base is a good default)

Exit codes: 0 ok, 2 bad args / missing file, 3 faster-whisper not installed.
"""
import argparse
import os
import sys

# Silence the harmless Windows symlink cache warning from huggingface_hub.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


def fmt_ts(seconds: float, sep: str) -> str:
    """Format a timestamp as HH:MM:SS<sep>mmm (sep is ',' for srt, '.' for vtt)."""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def main() -> int:
    p = argparse.ArgumentParser(description="Transcribe a local audio/video file.")
    p.add_argument("input", help="Path to the audio or video file.")
    p.add_argument("--model", default="base", help="Whisper model size (default: base).")
    p.add_argument("--format", default="txt", choices=["txt", "srt", "vtt"],
                   help="Output format (default: txt).")
    p.add_argument("--language", default="auto",
                   help="Language code (e.g. en) or 'auto' to detect (default: auto).")
    p.add_argument("--output", default=None,
                   help="Output path. Default: input filename with new extension, in cwd.")
    args = p.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 2

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: faster-whisper is not installed. "
              "Install it with: pip install faster-whisper", file=sys.stderr)
        return 3

    lang = None if args.language.lower() == "auto" else args.language

    # int8 keeps things light and CPU-friendly; fine for transcription accuracy.
    print(f"Loading model '{args.model}' (first run downloads it, then it's cached)...",
          file=sys.stderr)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    print("Transcribing...", file=sys.stderr)
    segments, info = model.transcribe(args.input, language=lang)
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})",
          file=sys.stderr)

    # Determine output path.
    if args.output:
        out_path = args.output
    else:
        base = os.path.splitext(os.path.basename(args.input))[0]
        out_path = f"{base}.{args.format}"

    with open(out_path, "w", encoding="utf-8") as f:
        if args.format == "txt":
            for seg in segments:
                f.write(seg.text.strip() + "\n")
        elif args.format == "srt":
            for i, seg in enumerate(segments, 1):
                f.write(f"{i}\n")
                f.write(f"{fmt_ts(seg.start, ',')} --> {fmt_ts(seg.end, ',')}\n")
                f.write(seg.text.strip() + "\n\n")
        elif args.format == "vtt":
            f.write("WEBVTT\n\n")
            for seg in segments:
                f.write(f"{fmt_ts(seg.start, '.')} --> {fmt_ts(seg.end, '.')}\n")
                f.write(seg.text.strip() + "\n\n")

    print(f"OK: wrote {out_path}", file=sys.stderr)
    print(out_path)  # stdout = the path, for scripting
    return 0


if __name__ == "__main__":
    sys.exit(main())
