"""Парсинг через threading + requests."""
import threading
import time

import requests
from bs4 import BeautifulSoup

from db import init_db, save_page
from urls import URLS

APPROACH = "threading"


def parse_and_save(url: str) -> None:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "lab2-bot/1.0"})
        r.raise_for_status()
        title = BeautifulSoup(r.text, "html.parser").title
        title_text = title.string.strip() if title and title.string else "<no title>"
    except Exception as e:  # noqa: BLE001
        title_text = f"<error: {e.__class__.__name__}>"
    save_page(url, title_text, APPROACH)
    print(f"[{APPROACH}] {url} -> {title_text}")


def run() -> float:
    init_db()
    threads = [threading.Thread(target=parse_and_save, args=(u,)) for u in URLS]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - t0


if __name__ == "__main__":
    elapsed = run()
    print(f"\n{APPROACH}: {len(URLS)} страниц за {elapsed:.3f}s")
