#!/usr/bin/env python3
"""Build a client-facing animated GoodieX intro video."""

from __future__ import annotations

import math
import os
import subprocess
import sys
from pathlib import Path
from textwrap import wrap

BUNDLED_PYTHON = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3"
if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
    os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "goodiex-sales-workflow-visual.png"
OUT_VIDEO = ROOT / "outputs" / "codex10k" / "goodiex-intro-video.mp4"
W, H = 1280, 720
FPS = 8


SCENES = [
    {
        "tag": "Intro",
        "title": "GoodieX sales lifecycle sprint",
        "body": "Hi Krystal, I am Nakul, an independent freelancer focused on practical n8n automation.",
        "active": 0,
        "duration": 4,
    },
    {
        "tag": "Step 1",
        "title": "Capture the request or order",
        "body": "The workflow starts when a sales signal comes in from an approved channel: form, ecommerce order, email, sheet, or CRM.",
        "active": 0,
        "duration": 7,
    },
    {
        "tag": "Step 2",
        "title": "Normalize the sales fields",
        "body": "Customer, product, size, order status, urgency, channel, and owner fields are cleaned before anything moves downstream.",
        "active": 1,
        "duration": 7,
    },
    {
        "tag": "Step 3",
        "title": "Prevent duplicate records",
        "body": "The workflow checks existing customer and order records first so the team does not chase the same sale twice.",
        "active": 2,
        "duration": 7,
    },
    {
        "tag": "Step 4",
        "title": "Route to the right owner",
        "body": "Clean records are assigned to the right queue or teammate, while unclear cases are held for review instead of silently breaking.",
        "active": 3,
        "duration": 7,
    },
    {
        "tag": "Step 5",
        "title": "Queue approved follow-up",
        "body": "Approved email or WhatsApp follow-up can be prepared automatically, with status and exceptions logged in one place.",
        "active": 4,
        "duration": 7,
    },
    {
        "tag": "$1,800 v1 milestone",
        "title": "One workflow, tested and handed off",
        "body": "I would build with dummy records first, then connect real tools only after access, routing, and follow-up rules are approved.",
        "active": 5,
        "duration": 7,
    },
]

NODES = [
    ("Capture", "request/order"),
    ("Normalize", "fields"),
    ("Dedupe", "records"),
    ("Route", "owner"),
    ("Follow up", "approved"),
    ("Log", "status"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONTS = {
    "tag": font(18, bold=True),
    "title": font(52, bold=True),
    "body": font(27),
    "small": font(18),
    "node": font(19, bold=True),
    "node_small": font(15),
}


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def fit_cover(img: Image.Image, size: tuple[int, int], zoom: float, drift: float) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height) * zoom
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    max_x = max(0, resized.width - target_w)
    max_y = max(0, resized.height - target_h)
    left = int(max_x * (0.45 + 0.18 * math.sin(drift)))
    top = int(max_y * (0.42 + 0.16 * math.cos(drift * 0.8)))
    return resized.crop((left, top, left + target_w, top + target_h))


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_text(draw: ImageDraw.ImageDraw, scene: dict[str, object], local: float) -> None:
    alpha_shift = int((1 - ease(min(local / 0.18, 1))) * 18)
    x = 70
    y = 90 + alpha_shift
    tag = str(scene["tag"]).upper()
    tag_w = draw.textbbox((0, 0), tag, font=FONTS["tag"])[2] + 34
    rounded(draw, (x, y, x + tag_w, y + 42), 16, (13, 95, 77, 235))
    draw.text((x + 17, y + 11), tag, font=FONTS["tag"], fill=(255, 241, 211))

    y += 72
    for line in wrap(str(scene["title"]), width=22):
        draw.text((x, y), line, font=FONTS["title"], fill=(255, 255, 255))
        y += 61
    y += 12
    for line in wrap(str(scene["body"]), width=43):
        draw.text((x, y), line, font=FONTS["body"], fill=(233, 244, 239))
        y += 38

    draw.text((x, H - 82), "GoodieX Sales Lifecycle Workflow v1", font=FONTS["small"], fill=(218, 232, 226))
    draw.text((x, H - 52), "Illustrative workflow proposal. No customer data is shown.", font=FONTS["small"], fill=(218, 232, 226))


def draw_workflow(draw: ImageDraw.ImageDraw, active: int, scene_progress: float, global_t: float) -> None:
    left = 650
    top = 135
    gap_y = 72
    positions = []
    for idx in range(len(NODES)):
        x = left + (idx % 2) * 225
        y = top + (idx // 2) * gap_y * 1.58
        positions.append((x, y))

    # Connector paths and moving handoff token.
    for idx in range(len(positions) - 1):
        x1, y1 = positions[idx]
        x2, y2 = positions[idx + 1]
        start = (x1 + 160, y1 + 34)
        end = (x2, y2 + 34)
        color = (25, 65, 56, 225) if idx < active else (181, 196, 190, 205)
        if idx % 2 == 1:
            mid_x = start[0] + 34
            draw.line([start, (mid_x, start[1]), (mid_x, end[1]), end], fill=color, width=3)
        else:
            draw.line([start, end], fill=color, width=3)

    if active > 0:
        start_idx = max(0, active - 1)
        x1, y1 = positions[start_idx]
        x2, y2 = positions[active]
        pulse = ease(scene_progress)
        px = (x1 + 160) + ((x2 + 4) - (x1 + 160)) * pulse
        py = (y1 + 34) + ((y2 + 34) - (y1 + 34)) * pulse
        draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(216, 102, 69, 255))

    for idx, ((label, detail), (x, y)) in enumerate(zip(NODES, positions)):
        is_active = idx == active
        is_done = idx < active
        pulse = 0.5 + 0.5 * math.sin(global_t * 6)
        fill = (255, 255, 255, 236)
        outline = (13, 95, 77, 255) if is_active or is_done else (211, 222, 217, 255)
        width = 3 if is_active else 1
        rounded(draw, (x, y, x + 164, y + 68), 15, fill, outline, width)
        icon_fill = (13, 95, 77, 255) if is_active or is_done else (226, 232, 229, 255)
        if is_active:
            glow = int(45 + 35 * pulse)
            draw.ellipse((x + 15 - glow // 7, y + 17 - glow // 7, x + 49 + glow // 7, y + 51 + glow // 7), fill=(216, 102, 69, 80))
        draw.ellipse((x + 16, y + 17, x + 50, y + 51), fill=icon_fill)
        draw.text((x + 63, y + 14), label, font=FONTS["node"], fill=(19, 33, 29))
        draw.text((x + 63, y + 39), detail, font=FONTS["node_small"], fill=(95, 112, 106))

    # Current record card.
    card_y = 560
    rounded(draw, (650, card_y, 1130, card_y + 86), 18, (255, 255, 255, 230), (215, 224, 220), 1)
    draw.text((674, card_y + 18), "Current record status", font=FONTS["node"], fill=(19, 33, 29))
    status = NODES[active][0] if active < len(NODES) else "Ready"
    draw.text((674, card_y + 48), f"{status} step active", font=FONTS["node_small"], fill=(95, 112, 106))
    bar_start = 930
    bar_end = 1110
    bar_w = min(bar_end - bar_start, int((bar_end - bar_start) * ((active + scene_progress) / len(NODES))))
    rounded(draw, (bar_start, card_y + 44, bar_start + bar_w, card_y + 56), 6, (13, 95, 77, 255))
    if bar_start + bar_w < bar_end:
        rounded(draw, (bar_start + bar_w, card_y + 44, bar_end, card_y + 56), 6, (217, 226, 222, 255))


def draw_frame(bg: Image.Image, scene: dict[str, object], local: float, global_t: float) -> Image.Image:
    active = int(scene["active"])
    zoom = 1.08 + 0.02 * math.sin(global_t / 4)
    frame = fit_cover(bg, (W, H), zoom=zoom, drift=global_t / 4).convert("RGBA")

    overlay = Image.new("RGBA", (W, H), (13, 31, 27, 76))
    frame = Image.alpha_composite(frame, overlay)

    left_panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    left_draw = ImageDraw.Draw(left_panel)
    left_draw.rectangle((0, 0, 620, H), fill=(13, 31, 27, 205))
    frame = Image.alpha_composite(frame, left_panel)

    right_panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    right_draw = ImageDraw.Draw(right_panel)
    rounded(right_draw, (622, 80, 1196, 670), 24, (247, 250, 248, 212), (220, 228, 224, 190), 1)
    frame = Image.alpha_composite(frame, right_panel)

    draw = ImageDraw.Draw(frame)
    draw_text(draw, scene, local)
    draw_workflow(draw, active, local, global_t)

    if local < 0.12:
        fade = int((1 - ease(local / 0.12)) * 115)
        frame = Image.alpha_composite(frame, Image.new("RGBA", (W, H), (13, 31, 27, fade)))
    return frame.convert("RGB")


def build_video() -> None:
    OUT_VIDEO.parent.mkdir(parents=True, exist_ok=True)
    bg = Image.open(ASSET).convert("RGB")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "image2pipe",
        "-vcodec",
        "png",
        "-framerate",
        str(FPS),
        "-i",
        "-",
        "-vf",
        "fps=30,format=yuv420p",
        "-movflags",
        "+faststart",
        str(OUT_VIDEO),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    global_frame = 0
    for scene in SCENES:
        frames = int(scene["duration"] * FPS)
        for i in range(frames):
            local = i / max(1, frames - 1)
            frame = draw_frame(bg, scene, local, global_frame / FPS)
            frame.save(proc.stdin, format="PNG")
            global_frame += 1
    proc.stdin.close()
    code = proc.wait()
    if code:
        raise SystemExit(code)
    print(OUT_VIDEO)


if __name__ == "__main__":
    build_video()
