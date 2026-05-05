from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
from celery.result import AsyncResult

from celery_app import celery_app
from parser_service import parse_books_task

router = APIRouter(prefix="/parser", tags=["parser-queue"])

class ParseAsyncRequest(BaseModel):
    ids: List[int] = Field(..., min_length=1, max_length=200)
    user_id: int = Field(..., ge=1)
    concurrency: int = Field(default=8, ge=1, le=50)

@router.post("/parse-async")
def parse_async(req: ParseAsyncRequest):
    job = parse_books_task.delay(req.ids, req.user_id, req.concurrency)
    return {"task_id": job.id, "state": "queued"}

@router.get("/task/{task_id}")
def task_status(task_id: str):
    r = AsyncResult(task_id, app=celery_app)
    # r.state: PENDING / STARTED / SUCCESS / FAILURE
    resp = {"task_id": task_id, "state": r.state}
    if r.successful():
        resp["result"] = r.result
    if r.failed():
        resp["error"] = str(r.result)
    return resp