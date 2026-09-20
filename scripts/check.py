#!/usr/bin/env python3
"""Smoke-check the Pages console. CPython + node only. No npm package."""
from __future__ import annotations

import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    ".nojekyll",
    "ARCHITECTURE.md",
    "CHANGELOG.md",
    "LICENSE",
    "README.md",
    "architecture.png",
    "index.html",
)
BOOT_IDS = ("view", "nav", "mob", "ham", "chrome", "feed-dot", "feed-count")
ENTITY_IN_SCRIPT = re.compile(r"&(?:amp|lt|gt|quot|#39|#x27);")
OG_DIM = re.compile(
    r'<meta property="og:image:(width|height)" content="(\d+)">'
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{path.name} is not a PNG")
    # IHDR is the first chunk.
    length, typ = struct.unpack(">I4s", data[8:16])
    if typ != b"IHDR" or length < 8:
        fail(f"{path.name} missing IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def extract_script(html: str) -> str:
    start = html.find("<script>")
    end = html.find("</script>", start)
    if start < 0 or end < 0:
        fail("index.html has no inline <script>")
    return html[start + len("<script>") : end]


def main() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("missing files: " + ", ".join(missing))

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for boot_id in BOOT_IDS:
        if f'id="{boot_id}"' not in html:
            fail(f'index.html missing id="{boot_id}" (console will not boot)')

    width, height = png_size(ROOT / "architecture.png")
    if (width, height) != (2000, 1400):
        fail(f"architecture.png is {width}x{height}, expected 2000x1400")

    og = dict(OG_DIM.findall(html))
    if og.get("width") != "2000" or og.get("height") != "1400":
        fail(f"og:image dimensions {og} do not match architecture.png 2000x1400")

    # html{} beats *{} — the reduce query must name the root scroller.
    if not re.search(
        r"@media\s*\(prefers-reduced-motion:reduce\)[^}]*html\s*\{[^}]*scroll-behavior\s*:\s*auto",
        html,
        flags=re.S,
    ):
        fail(
            "prefers-reduced-motion does not set html{scroll-behavior:auto} "
            "(a *{} rule loses to html{scroll-behavior:smooth})"
        )

    script = extract_script(html)
    if not script.strip():
        fail("inline script is empty")
    leaked = ENTITY_IN_SCRIPT.findall(script)
    if leaked:
        fail(
            "HTML entities inside <script> (this collapsed esc() and blanked Pages): "
            + ", ".join(sorted(set(leaked)))
        )

    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tmp:
        tmp.write(script)
        tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["node", "--check", tmp_path],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        fail("node is required for syntax check (node --check)")
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        fail("console script failed node --check\n" + detail)

    print("ok: files, png 2000x1400, boot ids, reduced-motion, script parses")


if __name__ == "__main__":
    main()
