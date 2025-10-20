# Отчет по лабораторной работе №2

**Выполнил:** Шафиков Максим Азатович  
**Факультет:** ПИН (ИКТ)  
**Группа:** К3339  
**Преподаватель:** Говоров Антон Игоревич

---

## Тема и цель работы

Разработать веб‑сервис для бронирования отелей на базе FastAPI с использованием шаблонов Jinja2, СУБД PostgreSQL и ORM SQLAlchemy. Реализовать публичные страницы, личный кабинет, отзывы, административные разделы, пагинацию и основную бизнес‑логику бронирований.

---

## Структура проекта

```
app/
  main.py                      # запуск приложения, middleware, обработчики ошибок
  pages/                       # пользовательские страницы и админ-панель
    router.py
  bookings/                    # маршруты бронирований
    router.py
  auth/                        # аутентификация и зависимости
    router.py
    deps.py
    utils.py
  crud/                        # слой работы с БД
    hotels.py
    bookings.py
    reviews.py
    users.py
  db/                          # модели и подключение к БД
    base.py
    models.py
    utils.py
  core/                        # конфигурация и безопасность
    config.py
    security.py
  templates/                   # Jinja2 шаблоны
    base.html, index.html, ...
  static/                      # статика и стили
    css/style.css
alembic.ini, app/alembic/      # миграции схемы БД
Dockerfile, docker-compose.yml # инфраструктура и запуск
```

Ключевые директории:
- `app/db` — модели SQLAlchemy и базовые слои подключения.
- `app/crud` — инкапсуляция запросов к БД (чтение/запись, пагинация, фильтрация).
- `app/pages` и `app/bookings` — HTTP‑маршруты для страниц и операций бронирования.
- `app/auth` — регистрация, логин, middleware‑аутентификация по cookie‑токену.
- `app/templates` — шаблоны Jinja2 для UI.

---

## Модели данных (основные)

```python
# app/db/models.py (фрагменты)
class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    checked_in = "checked_in"
    checked_out = "checked_out"

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)
```

Модели `User`, `Hotel`, `Room`, `Review` описывают пользователей, отели, номера и отзывы соответственно. Связи настроены через `relationship`.

---

## Основной запуск приложения и middleware

```python
# app/main.py (фрагменты)
app = FastAPI(title="Hotel Booking Service")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    db: Session = next(get_db())
    create_initial_admin(db)
    db.close()

@app.middleware("http")
async def add_user_to_context(request: Request, call_next):
    user = await get_current_user_from_cookie(request, next(get_db()))
    request.state.user = user
    return await call_next(request)
```

При старте создается админ (если отсутствует). Middleware добавляет текущего пользователя в `request.state.user` для доступа в шаблонах.

---

## Маршруты страниц и функционал

### Главная страница `/`

Функции:
- Отображение списка отелей с минимальной ценой номера и средним рейтингом.
- Фильтры по цене, сортировка по рейтингу/цене.
- Пагинация по 5 отелей с «диапазонной» навигацией.

```python
# app/pages/router.py (фрагмент)
@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request, db: Session = Depends(get_db),
                        page: int = 1, sort: str = Query("rating", enum=["rating","price_asc","price_desc"]),
                        min_price: str = Query(None), max_price: str = Query(None)):
    # безопасный парсинг фильтров цены
    min_price_float = float(min_price) if min_price and min_price.strip() else None
    max_price_float = float(max_price) if max_price and max_price.strip() else None

    hotels_with_stats, total_pages = hotel_repo.get_paginated(
        db=db, page=page, per_page=5, sort=sort,
        min_price=min_price_float, max_price=max_price_float,
    )
    return templates.TemplateResponse("index.html", {
        "request": request,
        "hotels": hotels_with_stats,
        "page": page,
        "total_pages": total_pages,
        "sort": sort,
        "min_price": min_price,
        "max_price": max_price,
    })
```

Пагинация отображает диапазоны элементов: «1‑5», «>> 6‑10» и т.д., при этом на первой/последней страницах лишние кнопки скрываются.

### Страница отеля `/hotel/{hotel_id}`

Функции:
- Детали отеля, список отзывов с пагинацией.
- Для админа — список гостей за последний месяц (с пагинацией).
- Форма добавления отзыва с валидацией дат: начало < конец, конец — в прошлом.

```python
# app/pages/router.py (фрагмент)
@router.post("/hotel/{hotel_id}/review")
async def add_review(..., stay_start: date = Form(), stay_end: date = Form()):
    today = date.today()
    if stay_start >= stay_end:
        return RedirectResponse(url=f"/hotel/{hotel_id}?error=invalid_dates", status_code=302)
    if stay_end > today:
        return RedirectResponse(url=f"/hotel/{hotel_id}?error=future_stay", status_code=302)
    review_repo.create(...)
    return RedirectResponse(url=f"/hotel/{hotel_id}", status_code=302)
```

### Личный кабинет `/cabinet`

Функции:
- Список бронирований пользователя с пагинацией по 5.
- Отмена будущих бронирований.

### Админ‑панель `/admin/bookings`

Функции:
- Список неподтвержденных бронирований с пагинацией по 5.
- Подтверждение/отклонение заявок.

---

## Бизнес‑логика в репозиториях

### Репозиторий отелей: сортировка, фильтрация, пагинация

```python
# app/crud/hotels.py (фрагмент)
q = (db.query(Hotel, func.min(Room.price).label("min_room_price"),
              func.avg(Review.rating.cast(Float)).label("avg_rating"))
       .outerjoin(Room, Room.hotel_id == Hotel.id)
       .outerjoin(Review, Review.hotel_id == Hotel.id)
       .group_by(Hotel.id))

if min_price is not None:
    q = q.having(func.min(Room.price) >= min_price)
if max_price is not None:
    q = q.having(func.min(Room.price) <= max_price)

if sort == "rating":
    q = q.order_by(func.coalesce(func.avg(Review.rating), 0).desc())
elif sort == "price_asc":
    q = q.order_by(func.coalesce(func.min(Room.price), 1e12).asc())
elif sort == "price_desc":
    q = q.order_by(func.coalesce(func.min(Room.price), 0).desc())

total = q.count()
items = q.offset((page - 1) * per_page).limit(per_page).all()
```

### Репозиторий бронирований: выборки и админ‑операции

```python
# app/crud/bookings.py (фрагмент)
def get_pending_paginated(self, db: Session, page: int, per_page: int):
    offset = (page - 1) * per_page
    query = db.query(models.Booking).filter(models.Booking.status == models.BookingStatus.pending)
    total = query.count()
    bookings = query.order_by(models.Booking.id).offset(offset).limit(per_page).all()
    return bookings, math.ceil(total / per_page)
```

---

## Аутентификация

Реализована простая cookie‑аутентификация:
1. Пользователь логинится, сервер выдает JWT (подписанный `SECRET_KEY`) и кладет его в cookie `access_token` (HttpOnly).
2. Middleware декодирует токен, подставляет пользователя в `request.state.user`.
3. Декораторы‑зависимости защищают доступ к личному кабинету и админ‑панели.

```python
# app/auth/deps.py (фрагмент)
async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    email = payload.get("sub")
    user = user_repo.get_by_email(db, email=email)
    return user
```

---

## Пагинация (UI)

На страницах используется единый стиль «диапазонной» пагинации (по 5 элементов):
- Левая кнопка скрыта на первой странице.
- Правая скрыта на последней.
- Текущий диапазон отображается как «i – i+4»; соседние диапазоны показываются в кнопках перехода.

Пример (фрагмент Jinja2):

```jinja2
{% set start_item = (page - 1) * 5 + 1 %}
{% set end_item = page * 5 %}
{% if page > 1 %}
  <a class="page-link" href="?page={{ page - 1 }}">{{ (page-2)*5+1 }} - {{ (page-1)*5 }} <<</a>
{% endif %}
<span class="page-link">{{ start_item }} - {{ end_item }}</span>
{% if page < total_pages %}
  <a class="page-link" href="?page={{ page + 1 }}">>> {{ page*5+1 }} - {{ (page+1)*5 }}</a>
{% endif %}
```

---

## Валидация дат

- При бронировании: дата заезда < даты выезда и заезд в будущем.
- В отзывах: период проживания завершен (дата окончания в прошлом).

```python
# app/bookings/router.py (фрагмент)
if check_in_date >= check_out_date:
    return RedirectResponse(url="/?error=invalid_dates", status_code=302)
if check_in_date < date.today():
    return RedirectResponse(url="/?error=past_checkin", status_code=302)
```

Сообщения об ошибках отображаются в шаблонах с помощью Bootstrap‑alert.

---

## Сборка и запуск (Docker)

Сервис контейнеризирован. Запуск:

```bash
docker compose up --build -d
```

Приложение доступно по адресу `http://localhost:8000` (или по адресу контейнера).

---

## Вывод

В рамках ЛР №2 реализован веб‑сервис бронирования отелей:
- Структура проекта разделена на слои (маршрутизация, репозитории, модели, шаблоны).
- Реализованы фильтры, сортировка, пагинация с удобным UI.
- Добавлены аутентификация, личный кабинет, отзывы, админ‑панель.
Работа позволила повторить работу с Jinja2, FastAPI и Sqlalchemy
