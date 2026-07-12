from __future__ import annotations

from pathlib import Path


def build_page(
    page_id: str,
    title: str,
    description: str,
    cover_url: str,
    tg_link: str,
    output: Path,
) -> None:
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{cover_url}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{cover_url}" />
  <meta http-equiv="refresh" content="0;url={tg_link}" />
  <script>location.replace("{tg_link}");</script>
</head>
<body>
  <p>正在跳转到 Telegram…</p>
  <p><a href="{tg_link}">若未自动跳转，请点击这里</a></p>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
