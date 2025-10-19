from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List, Optional
from app.utils import templates
from app.auth import get_current_user, create_access_token, verify_password
from app.db import engine
from sqlmodel import Session, select
from sqlmodel import func
from app.models import ConferenceTopicLink
from datetime import date
from app.models import User, Conference, Topic, Registration, Review

router = APIRouter()

@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return RedirectResponse(url='/ui/login')
    try:
        user = get_current_user(token)
    except Exception:
        return RedirectResponse(url='/ui/login')
    return templates.TemplateResponse('index.html', {"request": request, "user": user})

@router.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {"request": request, "user": None})


@router.get('/signup', response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse('signup.html', {"request": request, "user": None})


@router.post('/signup')
def do_signup(request: Request, username: str = Form(...), password: str = Form(...), display_name: str = Form(None)):
    from app.auth import get_password_hash
    from app.models import User
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            return templates.TemplateResponse('signup.html', {"request": request, "user": None, "error": "Username already exists"}, status_code=400)
        u = User(username=username, display_name=display_name, password_hash=get_password_hash(password))
        session.add(u)
        session.commit()
        session.refresh(u)
    return RedirectResponse(url='/ui/login', status_code=302)

@router.post('/login')
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        return templates.TemplateResponse('login.html', {"request": request, "user": None, "error": "Invalid credentials"}, status_code=400)
    access_token = create_access_token(data={"sub": str(user.id)})
    response = RedirectResponse(url='/ui/', status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.post('/logout')
def logout():
    response = RedirectResponse(url='/ui/login', status_code=302)
    response.delete_cookie('access_token')
    return response


def _get_current_user_from_cookie(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
    try:
        return get_current_user(token)
    except Exception:
        return None


@router.get('/conferences', response_class=HTMLResponse)
def conferences_page(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(2, ge=1, le=50),
    topic: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
):
    user = _get_current_user_from_cookie(request)
    # build query with optional filters
    with Session(engine) as session:
        base_q = select(Conference)
        # filter by topic name (join through link table)
        if topic:
            from app.models import Topic
            base_q = base_q.join(ConferenceTopicLink).join(Topic).where(Topic.name == topic)
        if location:
            base_q = base_q.where(Conference.location_name.contains(location))
        if search:
            base_q = base_q.where((Conference.title.contains(search)) | (Conference.description.contains(search)))
        if date_from:
            try:
                df = date.fromisoformat(date_from)
                base_q = base_q.where(Conference.end_date >= df)
            except Exception:
                pass
        if date_to:
            try:
                dt = date.fromisoformat(date_to)
                base_q = base_q.where(Conference.start_date <= dt)
            except Exception:
                pass

        # total count for pagination
        total_res = session.exec(select(func.count()).select_from(base_q.subquery())).one()
        total = int(total_res or 0)

        # pagination
        offset = (page - 1) * per_page
        q = base_q.offset(offset).limit(per_page)
        confs = session.exec(q).all()

        # build a list of dicts with conference and its topics names to avoid assigning new fields
        from app.models import Topic
        confs_out = []
        for conf in confs:
            topics = session.exec(select(Topic).join(ConferenceTopicLink).where(ConferenceTopicLink.conference_id == conf.id)).all()
            topics_names = [t.name for t in topics]
            confs_out.append({"conf": conf, "topics_names": topics_names})

    # pagination metadata
    total = int(total or 0)
    pages = (total + per_page - 1) // per_page if per_page else 1
    pagination = {"page": page, "per_page": per_page, "total": total, "pages": pages}

    return templates.TemplateResponse('conferences.html', {"request": request, "user": user, "conferences": confs_out, "pagination": pagination, "filters": {"topic": topic, "location": location, "search": search, "date_from": date_from, "date_to": date_to}})


@router.post('/conferences', response_class=HTMLResponse)
def create_conference_web(request: Request, title: str = Form(...), description: str = Form(None), location_name: str = Form(None), start_date: str = Form(...), end_date: str = Form(...), topics: str = Form(None)):
    user = _get_current_user_from_cookie(request)
    # only admin can create conferences
    if not user or getattr(user, 'role', None) != 'admin':
        return RedirectResponse(url='/ui/login')
    # parse topics comma separated
    topic_names = [t.strip() for t in (topics or '').split(',') if t.strip()]
    with Session(engine) as session:
        conf = Conference(title=title, description=description, location_name=location_name, start_date=start_date, end_date=end_date)
        topic_objs: List[Topic] = []
        for tname in topic_names:
            t = session.exec(select(Topic).where(Topic.name == tname)).first()
            if not t:
                t = Topic(name=tname)
                session.add(t)
                session.flush()
            topic_objs.append(t)
        conf.topics = topic_objs
        session.add(conf)
        session.commit()
        session.refresh(conf)
    return RedirectResponse(url='/ui/conferences', status_code=302)


@router.get('/conferences/{conf_id}', response_class=HTMLResponse)
def conference_detail(request: Request, conf_id: int):
    user = _get_current_user_from_cookie(request)
    with Session(engine) as session:
        conf = session.get(Conference, conf_id)
        if not conf:
            return RedirectResponse(url='/ui/conferences')
        reviews = session.exec(select(Review).where(Review.conference_id == conf_id)).all()
        # load registrations while session is open to avoid detached instance lazy-loading in template
        regs = session.exec(select(Registration).where(Registration.conference_id == conf_id)).all()
        conf.registrations = regs
    return templates.TemplateResponse('conference.html', {"request": request, "user": user, "conference": conf, "reviews": reviews})


@router.post('/conferences/{conf_id}/register')
def conference_register(request: Request, conf_id: int, title: str = Form(None), abstract: str = Form(None)):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        reg = Registration(user_id=user.id, conference_id=conf_id, title=title, abstract=abstract)
        session.add(reg)
        session.commit()
        session.refresh(reg)
    return RedirectResponse(url=f'/ui/conferences/{conf_id}', status_code=302)


@router.post('/conferences/{conf_id}/review')
def conference_review(request: Request, conf_id: int, text: str = Form(...), rating: int = Form(...)):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        r = Review(conference_id=conf_id, user_id=user.id, text=text, rating=rating)
        session.add(r)
        session.commit()
        session.refresh(r)
    return RedirectResponse(url=f'/ui/conferences/{conf_id}', status_code=302)


@router.get('/participants-page', response_class=HTMLResponse)
def participants_page(request: Request):
    user = _get_current_user_from_cookie(request)
    with Session(engine) as session:
        regs = session.exec(select(Registration)).all()
        out = []
        for r in regs:
            u = session.get(User, r.user_id)
            conf = session.get(Conference, r.conference_id)
            out.append({"registration": r, "user": u, "conference": conf})
    return templates.TemplateResponse('participants.html', {"request": request, "user": user, "items": out})


@router.get('/my_registrations', response_class=HTMLResponse)
def my_registrations(request: Request):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        q = select(Registration).where(Registration.user_id == user.id)
        regs = session.exec(q).all()
    return templates.TemplateResponse('registrations.html', {"request": request, "user": user, "registrations": regs})


@router.get('/registrations/{reg_id}/edit', response_class=HTMLResponse)
def edit_registration_page(request: Request, reg_id: int):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg or reg.user_id != user.id:
            return RedirectResponse(url='/ui/my_registrations')
    return templates.TemplateResponse('edit_registration.html', {"request": request, "user": user, "registration": reg})


@router.post('/registrations/{reg_id}/edit')
def edit_registration(request: Request, reg_id: int, title: str = Form(None), abstract: str = Form(None)):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg or reg.user_id != user.id:
            return RedirectResponse(url='/ui/my_registrations')
        reg.title = title
        reg.abstract = abstract
        session.add(reg)
        session.commit()
    return RedirectResponse(url='/ui/my_registrations', status_code=303)


@router.post('/registrations/{reg_id}/delete')
def delete_registration(request: Request, reg_id: int):
    user = _get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url='/ui/login')
    from app.models import Role
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg:
            return RedirectResponse(url='/ui/my_registrations')
        if reg.user_id != user.id and user.role != Role.admin:
            return RedirectResponse(url='/ui/my_registrations')
        session.delete(reg)
        session.commit()
    return RedirectResponse(url='/ui/my_registrations', status_code=303)


@router.get('/admin/registrations', response_class=HTMLResponse)
def admin_registrations_page(request: Request):
    user = _get_current_user_from_cookie(request)
    if not user or user.role != 'admin':
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        regs = session.exec(select(Registration)).all()
        # populate related user and conference to avoid DetachedInstanceError in templates
        for r in regs:
            r.user = session.get(User, r.user_id)
            r.conference = session.get(Conference, r.conference_id)
    return templates.TemplateResponse('admin_registrations.html', {"request": request, "user": user, "registrations": regs})


@router.post('/admin/registrations/{reg_id}/set')
@router.post('/admin/registrations/{reg_id}/set/')
@router.get('/admin/registrations/{reg_id}/set')
@router.get('/admin/registrations/{reg_id}/set/')
def admin_set_result(request: Request, reg_id: int, status: str = Form(None)):
    user = _get_current_user_from_cookie(request)
    if not user or user.role != 'admin':
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if reg:
            # support status from form (POST) or query param (GET)
            s = status if status is not None else request.query_params.get('status')
            if s:
                reg.status = s
            session.add(reg)
            session.commit()
    return RedirectResponse(url='/ui/admin/registrations', status_code=303)


@router.post('/admin/registrations')
def admin_registrations_post(request: Request, reg_id: int = Form(...), status: str = Form(...)):
    user = _get_current_user_from_cookie(request)
    if not user or user.role != 'admin':
        return RedirectResponse(url='/ui/login')
    with Session(engine) as session:
        reg = session.get(Registration, int(reg_id))
        if reg:
            reg.status = status
            session.add(reg)
            session.commit()
    return RedirectResponse(url='/ui/admin/registrations', status_code=303)
