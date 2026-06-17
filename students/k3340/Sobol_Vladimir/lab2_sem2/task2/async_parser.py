"""Парсинг через asyncio + aiohttp."""
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

from db import init_db, save_page
from urls import URLS

APPROACH = "async"


async def parse_and_save(session: aiohttp.ClientSession, url: str) -> None:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
            r.raise_for_status()
            html = await r.text()
        title = BeautifulSoup(html, "html.parser").title
        title_text = title.string.strip() if title and title.string else "<no title>"
    except Exception as e:  # noqa: BLE001
        title_text = f"<error: {e.__class__.__name__}>"
    save_page(url, title_text, APPROACH)
    print(f"[{APPROACH}] {url} -> {title_text}")


async def main() -> float:
    init_db()
    headers = {"User-Agent": "lab2-bot/1.0"}
    t0 = time.perf_counter()
    async with aiohttp.ClientSession(headers=headers) as session:
        await asyncio.gather(*(parse_and_save(session, u) for u in URLS))
    return time.perf_counter() - t0


if __name__ == "__main__":
    elapsed = asyncio.run(main())
    print(f"\n{APPROACH}: {len(URLS)} страниц за {elapsed:.3f}s")
