from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from connection import init_db
from routers import users, books, deals, chats, parser_proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(deals.router)
app.include_router(chats.router)
app.include_router(parser_proxy.router)

@app.get("/")
def hallo():
    return {"message": "Hallo!"}

if __name__=="__main__":
    uvicorn.run("main:app", reload=True)