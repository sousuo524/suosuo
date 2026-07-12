from __future__ import annotations

import json
import logging
import random
import subprocess
from datetime import date
from pathlib import Path

from config import Settings
from generate_page import build_page
from make_collage import make_collage, pick_images

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("publisher")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"last_id": 0, "today": "", "today_count": 0, "posted_ids": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_templates(path: Path) -> list[str]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("copy/templates.txt 不能为空")
    return lines


def git_push(settings: Settings, message: str) -> None:
    if not settings.github_token:
        log.warning("未配置 GITHUB_TOKEN，跳过 git push")
        return

    env = {"GIT_TERMINAL_PROMPT": "0"}
    repo_url = f"https://{settings.github_token}@github.com/{settings.github_repo}.git"

    def run(*args: str) -> None:
        subprocess.run(args, cwd=settings.state_file.parent, check=True, env=env)

    run("git", "add", "covers", "pages", "state.json")
    run("git", "-c", f"user.email=bot@local", "-c", f"user.name=suosuo-bot", "commit", "-m", message)
    run("git", "push", repo_url, "main")


def create_one_post(settings: Settings) -> dict:
    state = load_state(settings.state_file)
    today = date.today().isoformat()

    if state.get("today") != today:
        state["today"] = today
        state["today_count"] = 0

    if state["today_count"] >= settings.daily_limit:
        raise RuntimeError(f"今日已达上限 {settings.daily_limit} 条")

    next_id = int(state.get("last_id", 0)) + 1
    page_id = f"{next_id:03d}"

    images = pick_images(settings.images_dir, settings.images_per_collage)
    cover_path = settings.covers_dir / f"{page_id}.jpg"
    page_path = settings.pages_dir / f"{page_id}.html"

    log.info("拼图 page=%s images=%s", page_id, [p.name for p in images])
    make_collage(images, cover_path)

    templates = load_templates(settings.copy_file)
    caption = random.choice(templates).replace("{期}", page_id).replace("{N}", page_id)

    cover_url = f"{settings.site_base}/covers/{page_id}.jpg"
    page_url = f"{settings.site_base}/pages/{page_id}.html"

    build_page(
        page_id=page_id,
        title=" ",
        description="",
        cover_url=cover_url,
        tg_link=settings.tg_link,
        output=page_path,
    )

    state["last_id"] = next_id
    state["today_count"] = int(state.get("today_count", 0)) + 1
    state.setdefault("posted_ids", []).append(page_id)
    save_state(settings.state_file, state)

    git_push(settings, f"add landing page {page_id}")

    return {
        "page_id": page_id,
        "caption": caption,
        "page_url": page_url,
        "cover_url": cover_url,
    }


if __name__ == "__main__":
    result = create_one_post(Settings.load())
    print(json.dumps(result, ensure_ascii=False, indent=2))
