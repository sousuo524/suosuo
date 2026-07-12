from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass
class Settings:
    site_base: str
    tg_link: str
    github_token: str
    github_repo: str
    x_username: str
    x_email: str
    x_password: str
    daily_limit: int
    images_per_collage: int

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            site_base=os.getenv("SITE_BASE", "https://sousuo524.github.io/suosuo").rstrip("/"),
            tg_link=os.getenv("TG_LINK", "https://t.me/baoliaoresou"),
            github_token=os.getenv("GITHUB_TOKEN", "").strip(),
            github_repo=os.getenv("GITHUB_REPO", "sousuo524/suosuo").strip(),
            x_username=os.getenv("X_USERNAME", "").strip(),
            x_email=os.getenv("X_EMAIL", "").strip(),
            x_password=os.getenv("X_PASSWORD", "").strip(),
            daily_limit=_int("DAILY_LIMIT", 10),
            images_per_collage=_int("IMAGES_PER_COLLAGE", 4),
        )

    @property
    def images_dir(self) -> Path:
        return ROOT / "images"

    @property
    def covers_dir(self) -> Path:
        return ROOT / "covers"

    @property
    def pages_dir(self) -> Path:
        return ROOT / "pages"

    @property
    def copy_file(self) -> Path:
        return ROOT / "copy" / "templates.txt"

    @property
    def state_file(self) -> Path:
        return ROOT / "state.json"

    @property
    def cookies_file(self) -> Path:
        return ROOT / "cookies.json"
