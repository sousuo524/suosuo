from __future__ import annotations

import random
from pathlib import Path

from PIL import Image

CANVAS_W = 1200
CANVAS_H = 630
GUTTER = 6  # 图片之间的细白边（像素）


def _cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """居中裁剪，铺满格子，不留黑边。"""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = max(1, int(src_w * scale))
    new_h = max(1, int(src_h * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def make_collage(image_paths: list[Path], output: Path) -> None:
    if len(image_paths) != 4:
        raise ValueError("需要恰好 4 张图片")

    cell_w = (CANVAS_W - GUTTER) // 2
    cell_h = (CANVAS_H - GUTTER) // 2
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (255, 255, 255))

    positions = [
        (0, 0),
        (cell_w + GUTTER, 0),
        (0, cell_h + GUTTER),
        (cell_w + GUTTER, cell_h + GUTTER),
    ]

    for path, (x, y) in zip(image_paths, positions, strict=True):
        with Image.open(path) as img:
            tile = _cover_crop(img.convert("RGB"), cell_w, cell_h)
            canvas.paste(tile, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "JPEG", quality=90)


def pick_images(images_dir: Path, count: int = 4) -> list[Path]:
    files = sorted(
        p
        for p in images_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    if len(files) < count:
        raise RuntimeError(f"images/ 里至少需要 {count} 张图，当前只有 {len(files)} 张")
    return random.sample(files, count)
