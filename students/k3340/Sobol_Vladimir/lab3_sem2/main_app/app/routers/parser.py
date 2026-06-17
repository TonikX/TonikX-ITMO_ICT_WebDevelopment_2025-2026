"""Прокси-роутер: вызов внешнего парсер-сервиса (sync) и постановка
задачи в Celery (async)."""
import os
from typing import List

import requests
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import ParsedPage
from ..schemas import ParseRequest, ParsedPageRead
from ..tasks.celery_app import celery_app
from ..tasks.parse_task import parse_url_task

PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")

router = APIRouter(prefix="/parser", tags=["parser"])


@router.post("/parse")
def parse_sync(payload: ParseRequest):
    """Синхронный вызов: дёргает parser-сервис по HTTP и ждёт ответа."""
    try:
        r = requests.post(
            f"{PARSER_URL}/parse",
            json={"url": payload.url},
            timeout=30,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Parser unavailable: {e}")
    return r.json()


@router.post("/parse-async", status_code=202)
def parse_async(payload: ParseRequest):
    """Кладёт задачу в очередь Celery (Redis broker) и возвращает task_id."""
    task = parse_url_task.delay(payload.url)
    return {"task_id": task.id, "status": "queued"}


@router.get("/parse-async/{task_id}")
def parse_async_status(task_id: str):
    """Проверка статуса фоновой задачи."""
    res = AsyncResult(task_id, app=celery_app)
    body: dict = {"task_id": task_id, "status": res.status}
    if res.successful():
        body["result"] = res.result
    elif res.failed():
        body["error"] = str(res.result)
    return body


@router.get("/pages", response_model=List[ParsedPageRead])
def list_pages(session=Depends(get_session)):
    """История распаршенных страниц (общая таблица в Postgres)."""
    return session.exec(select(ParsedPage).order_by(ParsedPage.id.desc())).all()
