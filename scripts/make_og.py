#!/usr/bin/env python3
"""Generate the 1200×630 Open Graph share image at assets/img/og.png.

Re-run anytime you want to refresh it:
    python3 scripts/make_og.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets" / "img" / "og.png"

W, H = 1200, 630

# ── Palette (matches the site's _sass/_variables.scss) ────────────────────
BG_TOP    = (7, 7, 13)        # #07070d
BG_BOT    = (5, 6, 12)        # #05060c
ACCENT    = (99, 102, 241)    # indigo-500
ACCENT_HI = (129, 140, 248)   # indigo-400
ACCENT_LO = (79, 70, 229)     # indigo-600
FG        = (230, 232, 242)
FG_DIM    = (164, 169, 194)
FG_MUTE   = (110, 116, 148)

# ── Fonts (macOS) ──────────────────────────────────────────────────────────
def load(name_candidates, size, index=0):
    for path in name_candidates:
        try:
            return ImageFont.truetype(path, size, index=index)
        except Exception:
            continue
    return ImageFont.load_default()

NAME_FONT  = load(["/System/Library/Fonts/Helvetica.ttc",
                   "/System/Library/Fonts/HelveticaNeue.ttc",
                   "/System/Library/Fonts/Supplemental/Arial Black.ttf"], 88, index=1)
TAG_FONT   = load(["/System/Library/Fonts/Helvetica.ttc",
                   "/System/Library/Fonts/HelveticaNeue.ttc"], 34, index=0)
MONO_FONT  = load(["/System/Library/Fonts/Menlo.ttc",
                   "/System/Library/Fonts/Monaco.ttf",
                   "/System/Library/Fonts/Courier.dfont"], 22, index=0)
CHIP_FONT  = load(["/System/Library/Fonts/Menlo.ttc",
                   "/System/Library/Fonts/Monaco.ttf"], 18, index=0)

# ── Canvas ────────────────────────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(img, "RGBA")

# Vertical gradient backdrop
for y in range(H):
    t = y / (H - 1)
    r = int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t)
    g = int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t)
    b = int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Indigo glow — radial-ish, faked with overlapping translucent circles
def soft_blob(cx, cy, radius, rgb, peak_alpha=70, steps=12):
    for i in range(steps, 0, -1):
        rr = radius * i / steps
        a  = int(peak_alpha * (1 - (i / steps)) ** 1.6)
        if a <= 0:
            continue
        draw.ellipse([(cx - rr, cy - rr), (cx + rr, cy + rr)],
                     fill=(rgb[0], rgb[1], rgb[2], a))

soft_blob(W * 0.82, -80,        420, ACCENT,    peak_alpha=130)
soft_blob(-80,      H * 1.05,   460, ACCENT_LO, peak_alpha=110)
soft_blob(W * 0.55, H * 0.55,   260, ACCENT_HI, peak_alpha=80)

# Subtle "chip" grid in the lower-right corner — evokes the site backdrop
def grid(x0, y0, cols, rows, cell, stroke=(255, 255, 255, 18)):
    for c in range(cols + 1):
        x = x0 + c * cell
        draw.line([(x, y0), (x, y0 + rows * cell)], fill=stroke, width=1)
    for r in range(rows + 1):
        y = y0 + r * cell
        draw.line([(x0, y), (x0 + cols * cell, y)], fill=stroke, width=1)

grid(W - 360, H - 260, cols=10, rows=7, cell=32)

# A few lit "cores" in that grid for life
def lit_core(x, y, size=22, rgb=ACCENT, alpha=160):
    draw.rounded_rectangle([(x, y), (x + size, y + size)],
                           radius=4, fill=(rgb[0], rgb[1], rgb[2], alpha),
                           outline=(rgb[0], rgb[1], rgb[2], 200), width=1)

# Place a handful of cores at intersections
for (cx, cy, a) in [(2, 1, 200), (5, 2, 130), (7, 4, 180),
                    (3, 5, 110), (8, 1, 90),  (4, 3, 220),
                    (1, 4, 120), (6, 6, 150)]:
    lit_core(W - 360 + cx * 32 + 4, H - 260 + cy * 32 + 4,
             size=24, rgb=ACCENT_HI, alpha=a)

# ── Foreground content ────────────────────────────────────────────────────
PAD = 90

# Small SRG badge (top-left)
badge_pad_x, badge_pad_y = 18, 10
badge_text = "SRG"
btw = draw.textlength(badge_text, font=CHIP_FONT)
bx, by = PAD, PAD
draw.rounded_rectangle([(bx, by), (bx + btw + badge_pad_x * 2, by + 36)],
                       radius=8, fill=(99, 102, 241, 40),
                       outline=(99, 102, 241, 140), width=1)
draw.text((bx + badge_pad_x, by + badge_pad_y - 4),
          badge_text, fill=ACCENT_HI, font=CHIP_FONT)

# Eyebrow tagline (mono, all-caps)
eyebrow = "COMPUTER ARCHITECTURE · POWER & PERFORMANCE · RISC-V"
draw.text((PAD, PAD + 70), eyebrow, fill=ACCENT_HI, font=MONO_FONT)

# Big name
name = "Sai Rajat Goparaju"
draw.text((PAD, PAD + 120), name, fill=FG, font=NAME_FONT)

# Tagline
tagline = "Incoming PhD @ UW–Madison  ·  HAL Lab"
draw.text((PAD, PAD + 235), tagline, fill=FG_DIM, font=TAG_FONT)

# Affiliation strip near the bottom
affiliations = ["Tenstorrent", "Google · Silicon", "Samsung SSIR", "BITS Pilani"]
strip_y = H - PAD - 50
x = PAD
for i, label in enumerate(affiliations):
    tw = draw.textlength(label, font=MONO_FONT)
    chip_w = tw + 28
    draw.rounded_rectangle([(x, strip_y), (x + chip_w, strip_y + 38)],
                           radius=10, fill=(255, 255, 255, 8),
                           outline=(255, 255, 255, 30), width=1)
    draw.text((x + 14, strip_y + 8), label, fill=FG_DIM, font=MONO_FONT)
    x += chip_w + 12

# Thin accent rule above affiliations
draw.line([(PAD, strip_y - 24), (PAD + 220, strip_y - 24)],
          fill=(99, 102, 241, 200), width=2)

# Save
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT}  ({OUT.stat().st_size:,} bytes, {W}×{H})")
