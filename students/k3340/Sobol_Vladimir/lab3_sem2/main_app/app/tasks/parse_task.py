"""Celery-таска: парсит URL и пишет результат в общую таблицу ParsedPage.

Воркер выполняет работу сам (не дёргает parser-сервис по HTTP), чтобы
показать классический паттерн «очередь + worker делает работу».
"""
import requests
from bs4 import BeautifulSoup
from sqlmodel import Session

from ..connection import engine
from ..models import ParsedPage
from .celery_app import celery_app


@celery_app.task(name="app.tasks.parse_url", bind=True, max_retries=2, default_retry_delay=5)
def parse_url_task(self, url: str) -> dict:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "lab3-celery/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "<no title>"
    except requests.RequestException as exc:
        raise self.retry(exc=exc)

    with Session(engine) as session:
        page = ParsedPage(url=url, title=title, source="celery")
        session.add(page)
        session.commit()
        session.refresh(page)
        return {"id": page.id, "url": page.url, "title": page.title, "source": page.source}
