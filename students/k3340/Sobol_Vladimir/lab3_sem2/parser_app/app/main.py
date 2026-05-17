"""Микро-сервис парсера: принимает URL, тянет страницу, кладёт <title> в БД."""
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .db import save_page

app = FastAPI(title="Parser Service")


class ParseRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"app": "parser", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse")
def parse(payload: ParseRequest):
    try:
        r = requests.get(
            payload.url,
            timeout=15,
            headers={"User-Agent": "lab3-parser/1.0"},
        )
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "<no title>"
    page = save_page(payload.url, title, source="http")
    return {
        "id": page.id,
        "url": page.url,
        "title": page.title,
        "source": page.source,
    }
