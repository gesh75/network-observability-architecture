#!/usr/bin/env python3
"""Smoke-check the Pages console. Exit 0 only if the site can still boot.

Catches the class of failure already shipped twice (949aee3, 1d2b1d8):
an HTML-decoded escape helper that made the inline script invalid JS
and left GitHub Pages as a blank shell.
"""
from __future__ import annotations

import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "index.html",
    "ARCHITECTURE.md",
    "CHANGELOG.md",
    "README.md",
    "LICENSE",
    "architecture.png",
    ".nojekyll",
)
SCRIPT_IDS = ("view", "nav", "ham", "chrome", "feed-dot", "feed-count")
ENTITY_RE = re.compile(r"&(?:amp|lt|gt|quot|#39|#x27);", re.I)
OG_SIZE = (2000, 1400)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{path.name} is not a PNG")
    ihdr = data.find(b"IHDR")
    if ihdr < 0:
        fail(f"{path.name} has no IHDR")
    return struct.unpack(">II", data[ihdr + 4 : ihdr + 12])


def extract_script(html: str) -> str:
    blocks = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
    if len(blocks) != 1:
        fail(f"expected exactly one inline <script>, found {len(blocks)}")
    return blocks[0]


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    png = ROOT / "architecture.png"
    width, height = png_size(png)
    if (width, height) != OG_SIZE:
        fail(f"architecture.png is {width}x{height}, expected {OG_SIZE[0]}x{OG_SIZE[1]}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    if "<noscript" not in html:
        fail("index.html has no <noscript> fallback (blank shell if JS dies)")
    for element_id in SCRIPT_IDS:
        if f'id="{element_id}"' not in html:
            fail(f"index.html missing id={element_id}")

    og_w = re.search(r'property="og:image:width" content="(\d+)"', html)
    og_h = re.search(r'property="og:image:height" content="(\d+)"', html)
    if not og_w or not og_h:
        fail("index.html missing og:image width/height")
    if (int(og_w.group(1)), int(og_h.group(1))) != (width, height):
        fail("og:image dimensions do not match architecture.png")

    js = extract_script(html)
    hit = ENTITY_RE.search(js)
    if hit:
        fail(
            "inline script still contains an HTML entity "
            f"({hit.group(0)!r}) — this is the 949aee3 blank-page landmine"
        )

    tmp = Path("/tmp/network-obs-console.js")
    tmp.write_text(js, encoding="utf-8")
    check = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
    if check.returncode != 0:
        fail("inline script failed node --check:\n" + (check.stderr or check.stdout))

    print("OK: required files, PNG 2000x1400, noscript, script parses")


if __name__ == "__main__":
    main()
