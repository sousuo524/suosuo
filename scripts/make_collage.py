from __future__ import annotations

import random
from pathlib import Path

from PIL import Image

CANVAS_W = 1200
CANVAS_H = 630


def make_collage(image_paths: list[Path], output: Path) -> None:
    if len(image_paths) != 4:
        raise ValueError("需要恰好 4 张图片")

    cell_w = CANVAS_W // 2
    cell_h = CANVAS_H // 2
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (20, 20, 20))

    positions = [
        (0, 0),
        (cell_w, 0),
        (0, cell_h),
        (cell_w, cell_h),
    ]

    for path, (x, y) in zip(image_paths, positions, strict=True):
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (cell_w, cell_h), (30, 30, 30))
            offset_x = (cell_w - img.width) // 2
            offset_y = (cell_h - img.height) // 2
            tile.paste(img, (offset_x, offset_y))
            canvas.paste(tile, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "JPEG", quality=88)


def pick_images(images_dir: Path, count: int = 4) -> list[Path]:
    files = sorted(
        p
        for p in images_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    if len(files) < count:
        raise RuntimeError(f"images/ 里至少需要 {count} 张图，当前只有 {len(files)} 张")
    return random.sample(files, count)
