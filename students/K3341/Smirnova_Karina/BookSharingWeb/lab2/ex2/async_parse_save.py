import time
import asyncio
import aiohttp

from connection import get_session, init_db
from models import Book, ParsedPage, Status, Condition
from parser import parse
from urls_25 import URLS_25

USER_ID = 1

def save_to_db(url: str, page_title: str, book_title: str, author: str, summary: str | None):
    session = next(get_session())
    try:
        session.add(ParsedPage(url=url, title=page_title))
        session.add(Book(
            user_id=USER_ID,
            title=book_title,
            author=author or "Unknown",
            description=summary,
            status=Status.ACTIVE,
            condition=Condition.NEW,
        ))
        session.commit()
    finally:
        session.close()

async def parse_and_save(url: str, http: aiohttp.ClientSession, sem: asyncio.Semaphore):
    async with sem:
        async with http.get(url, timeout=aiohttp.ClientTimeout(total=20),
                            headers={"User-Agent": "Mozilla/5.0 (student parser)"}) as resp:
            resp.raise_for_status()
            html = await resp.text()

    data = parse(html)
    save_to_db(url, data["page_title"], data["title"], data["author"], data["description"])
    print(f"[async] {url} -> {data['title']} / {data['author']}")

async def main_async():
    init_db()

    urls = URLS_25[:25]
    concurrency = 8
    sem = asyncio.Semaphore(concurrency)

    t0 = time.perf_counter()
    async with aiohttp.ClientSession() as http:
        tasks = [asyncio.create_task(parse_and_save(url, http, sem)) for url in urls]
        await asyncio.gather(*tasks)
    t1 = time.perf_counter()

    print(f"[asyncio] urls={len(urls)} concurrency={concurrency} time={t1 - t0:.6f}s")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()