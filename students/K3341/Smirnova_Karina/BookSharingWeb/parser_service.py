import asyncio
from typing import List

import aiohttp

from celery_app import celery_app
from connection import init_db, get_session
from models import Book, ParsedPage, Status, Condition
from lab2.ex2.parser import parse as parse_html


def build_url(book_id: int) -> str:
    return f"https://www.gutenberg.org/ebooks/{book_id}"


def save_to_db(user_id: int, url: str, page_title: str, book_title: str, author: str, summary: str | None):
    session = next(get_session())
    try:
        session.add(ParsedPage(url=url, title=page_title))
        session.add(Book(
            user_id=user_id,
            title=book_title,
            author=author or "Unknown",
            description=summary,
            status=Status.ACTIVE,
            condition=Condition.NEW,
        ))
        session.commit()
    finally:
        session.close()


async def _parse_many(ids: List[int], user_id: int, concurrency: int) -> dict:
    sem = asyncio.Semaphore(concurrency)

    async def parse_one(book_id: int, http: aiohttp.ClientSession):
        url = build_url(book_id)
        async with sem:
            async with http.get(
                url,
                timeout=aiohttp.ClientTimeout(total=20),
                headers={"User-Agent": "Mozilla/5.0 (student parser)"},
            ) as resp:
                resp.raise_for_status()
                html = await resp.text()

        data = parse_html(html)
        title = (data.get("title") or "").strip() or "(no title)"
        author = (data.get("author") or "").strip() or "Unknown"
        page_title = (data.get("page_title") or "").strip() or title
        desc = data.get("description")

        save_to_db(user_id, url, page_title, title, author, desc)
        return {"id": book_id, "url": url, "ok": True, "title": title, "author": author}

    init_db()
    async with aiohttp.ClientSession() as http:
        results = await asyncio.gather(*(parse_one(i, http) for i in ids), return_exceptions=True)

    normalized = []
    ok = 0
    for i, r in zip(ids, results):
        if isinstance(r, Exception):
            normalized.append({"id": i, "url": build_url(i), "ok": False, "error": str(r)})
        else:
            ok += 1
            normalized.append(r)

    return {"requested": len(ids), "saved_ok": ok, "results": normalized}


@celery_app.task(name="tasks.parse_books")
def parse_books_task(ids: list[int], user_id: int, concurrency: int = 8) -> dict:
    return asyncio.run(_parse_many(ids=ids, user_id=user_id, concurrency=concurrency))