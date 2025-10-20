from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.db.base import get_db
from app.pages.router import router as pages_router
from app.auth.router import router as auth_router
from app.bookings.router import router as bookings_router
from app.auth.deps import get_current_user_from_cookie


app = FastAPI(title="Hotel Booking Service")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(bookings_router)


@app.middleware("http")
async def add_user_to_context(request: Request, call_next):
    user = await get_current_user_from_cookie(request, next(get_db()))
    request.state.user = user
    response = await call_next(request)
    return response


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc):
    return RedirectResponse(url="/login", status_code=302)