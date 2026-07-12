from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from twikit import Client

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import Settings
from publish_one import create_one_post

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("x-post")


async def login_client(settings: Settings) -> Client:
    client = Client("zh-CN")
    cookies = settings.cookies_file

    if cookies.exists():
        client.load_cookies(str(cookies))
        log.info("已加载 cookies")
        return client

    if not settings.x_username or not settings.x_password:
        raise RuntimeError("请先配置 X_USERNAME / X_PASSWORD，或运行 python post_to_x.py --login")

    await client.login(
        auth_info_1=settings.x_username,
        auth_info_2=settings.x_email or settings.x_username,
        password=settings.x_password,
        cookies_file=str(cookies),
    )
    log.info("X 登录成功，cookies 已保存")
    return client


async def post_tweet(client: Client, text: str) -> None:
    await client.create_tweet(text=text)
    log.info("已发推: %s", text.replace("\n", " / "))


async def main() -> None:
    parser = argparse.ArgumentParser(description="生成落地页并发到 X")
    parser.add_argument("--login", action="store_true", help="仅登录 X 并保存 cookies")
    parser.add_argument("--dry-run", action="store_true", help="只生成落地页，不发 X")
    args = parser.parse_args()

    settings = Settings.load()
    client = await login_client(settings)

    if args.login:
        return

    post = create_one_post(settings)
    tweet = f"{post['caption']}\n{post['page_url']}"

    if args.dry-run:
        log.info("dry-run，待发内容: %s", tweet)
        return

    await post_tweet(client, tweet)


if __name__ == "__main__":
    asyncio.run(main())
