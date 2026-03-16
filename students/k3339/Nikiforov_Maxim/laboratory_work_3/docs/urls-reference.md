# Справочник URL проекта

## Где что определено

| Что | Файл |
|-----|------|
| **Главный роутинг** (admin, app, auth) | `laboratory_work_3/urls.py` |
| **Все URL приложения** (веб-страницы + API) | `app/urls.py` |
| **API (Swagger/DRF)** | `app/urls.py` — роутер `router` + `path('api/', include(router.urls))` |
| **Djoser (auth)** | Подключается в `laboratory_work_3/urls.py` через `include('djoser.urls')` и `include('djoser.urls.authtoken')` |

---

## 1. Главный файл: `laboratory_work_3/urls.py`

Здесь подключаются только три группы маршрутов:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),           # все страницы и API приложения app
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
```

- **`/admin/`** — админка Django.
- **`/auth/...`** — регистрация, логин по токену и т.д. (Djoser).
- Всё остальное (включая `/api/`, `/login/`, `/books/` и т.д.) задаётся в **`app/urls.py`**.

---

## 2. API (то, что видно в Swagger / Browsable API)

Все API-адреса задаются в **`app/urls.py`** через **роутер**:

```python
router = DefaultRouter()
router.register(r'reading-rooms', ReadingRoomViewSet, basename='readingroom')
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'books', BookViewSet, basename='book')
router.register(r'book-copies', BookCopyViewSet, basename='bookcopy')
router.register(r'book-assignments', BookAssignmentViewSet, basename='bookassignment')
router.register(r'librarian-operations', LibrarianOperationsViewSet, basename='librarian')

# ...
path('api/', include(router.urls)),
```

Роутер для каждого ViewSet автоматически создаёт:

- `GET .../` — список
- `POST .../` — создание
- `GET .../<id>/` — один объект
- `PUT` / `PATCH .../<id>/` — обновление
- `DELETE .../<id>/` — удаление

Дополнительные действия (кнопки в Swagger) задаются декоратором **`@action`** в **`app/views.py`** в соответствующих ViewSet’ах.

### Список всех API URL (Swagger)

Базовый префикс: **`/api/`**.

| Метод | URL | Описание |
|-------|-----|----------|
| **Читальные залы** (`/api/reading-rooms/`) | | |
| GET | `/api/reading-rooms/` | Список залов |
| POST | `/api/reading-rooms/` | Создать зал |
| GET | `/api/reading-rooms/<id>/` | Один зал |
| PUT/PATCH | `/api/reading-rooms/<id>/` | Обновить зал |
| DELETE | `/api/reading-rooms/<id>/` | Удалить зал |
| **Читатели** (`/api/readers/`) | | |
| GET | `/api/readers/` | Список читателей |
| POST | `/api/readers/` | Создать читателя |
| GET | `/api/readers/<id>/` | Один читатель |
| PUT/PATCH | `/api/readers/<id>/` | Обновить читателя |
| DELETE | `/api/readers/<id>/` | Удалить читателя |
| GET | `/api/readers/<id>/books/` | Книги читателя (@action) |
| GET | `/api/readers/old_assignments/` | Старые закрепления (@action) |
| GET | `/api/readers/with_rare_books/` | Читатели с редкими книгами (@action) |
| GET | `/api/readers/young_readers/` | Количество читателей < 20 лет (@action) |
| GET | `/api/readers/education_stats/` | Статистика по образованию (@action) |
| **Книги** (`/api/books/`) | | |
| GET | `/api/books/` | Список книг |
| POST | `/api/books/` | Создать книгу |
| GET | `/api/books/<id>/` | Одна книга |
| PUT/PATCH | `/api/books/<id>/` | Обновить книгу |
| DELETE | `/api/books/<id>/` | Удалить книгу |
| **Экземпляры книг** (`/api/book-copies/`) | | |
| GET | `/api/book-copies/` | Список экземпляров |
| POST | `/api/book-copies/` | Создать экземпляр |
| GET | `/api/book-copies/<id>/` | Один экземпляр |
| PUT/PATCH | `/api/book-copies/<id>/` | Обновить |
| DELETE | `/api/book-copies/<id>/` | Удалить |
| **Закрепления** (`/api/book-assignments/`) | | |
| GET | `/api/book-assignments/` | Список закреплений |
| POST | `/api/book-assignments/` | Создать закрепление |
| GET | `/api/book-assignments/<id>/` | Одно закрепление |
| PUT/PATCH | `/api/book-assignments/<id>/` | Обновить |
| DELETE | `/api/book-assignments/<id>/` | Удалить |
| POST | `/api/book-assignments/<id>/return_book/` | Вернуть книгу (@action) |
| **Операции библиотекаря** (`/api/librarian-operations/`) | | |
| POST | `/api/librarian-operations/register_reader/` | Записать читателя (@action) |
| POST | `/api/librarian-operations/unregister_old_readers/` | Исключить старых (@action) |
| POST | `/api/librarian-operations/write_off_book/` | Списать книгу (@action) |
| POST | `/api/librarian-operations/accept_book/` | Принять книгу (@action) |
| GET | `/api/librarian-operations/monthly_report/` | Месячный отчёт (@action) |

Страница, где это всё видно в браузере (Browsable API, похоже на Swagger): **`/api/`**.

---

## 3. Djoser (auth) — где написаны URL

Сами маршруты **не лежат в вашем проекте** — они внутри пакета **Djoser**. Подключение в **`laboratory_work_3/urls.py`**:

```python
path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),
```

Типичные URL Djoser (префикс **`/auth/`**):

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/users/` | Регистрация |
| GET | `/auth/users/me/` | Текущий пользователь |
| POST | `/auth/token/login/` | Получить токен (то, что открывалось как «Swagger») |
| POST | `/auth/token/logout/` | Выход (инвалидация токена) |

Полный список можно посмотреть в коде Djoser (установленный пакет) или в [документации Djoser](https://djoser.readthedocs.io/).

---

## 4. Веб-страницы (HTML)

Все заданы в **`app/urls.py`** в списке **`urlpatterns`** (не роутер).

| URL | Имя (name) | Шаблон |
|-----|------------|--------|
| `/` | `index` | `index.html` |
| `/login/` | `login` | `auth/login.html` |
| `/register/` | `register` | `auth/register.html` |
| `/logout/` | `logout` | редирект |
| **Залы** | | |
| `/reading-rooms/` | `reading_rooms_list` | `reading_rooms/list.html` |
| `/reading-rooms/create/` | `reading_room_create` | `reading_rooms/form.html` |
| `/reading-rooms/<id>/` | `reading_room_detail` | `reading_rooms/detail.html` |
| `/reading-rooms/<id>/edit/` | `reading_room_edit` | `reading_rooms/form.html` |
| **Читатели** | | |
| `/readers/` | `readers_list` | `readers/list.html` |
| `/readers/create/` | `reader_create` | `readers/form.html` |
| `/readers/<id>/` | `reader_detail` | `readers/detail.html` |
| `/readers/<id>/edit/` | `reader_edit` | `readers/form.html` |
| **Книги** | | |
| `/books/` | `books_list` | `books/list.html` |
| `/books/create/` | `book_create` | `books/form.html` |
| `/books/<id>/` | `book_detail` | `books/detail.html` |
| `/books/<id>/edit/` | `book_edit` | `books/form.html` |
| `/books/<id>/delete/` | `book_delete` | `books/delete.html` |
| **Экземпляры** | | |
| `/book-copies/create/` | `book_copy_create` | `book_copies/form.html` |
| `/book-copies/create/<book_id>/` | `book_copy_create` | `book_copies/form.html` |
| **Закрепления** | | |
| `/assignments/` | `assignments_list` | `assignments/list.html` |
| `/assignments/create/` | `assignment_create` | `assignments/form.html` |
| `/assignments/<id>/return/` | `assignment_return` | `assignments/return.html` |
| **Операции** | | |
| `/librarian/` | `librarian_operations` | `librarian/operations.html` |
| `/librarian/unregister-old/` | `librarian_old_readers` | `librarian/unregister_old.html` |
| `/librarian/monthly-report/` | `librarian_monthly_report` | `librarian/monthly_report.html` |
| **Запросы** | | |
| `/queries/reader/<id>/books/` | `query_reader_books` | `queries/reader_books.html` |
| `/queries/old-assignments/` | `query_old_assignments` | `queries/old_assignments.html` |
| `/queries/rare-books/` | `query_rare_books` | `queries/rare_books.html` |
| `/queries/young-readers/` | `query_young_readers` | `queries/young_readers.html` |
| `/queries/education-stats/` | `query_education_stats` | `queries/education_stats.html` |

---

## Кратко

- **Swagger/API URL** — в **`app/urls.py`** (роутер + `path('api/', include(router.urls))`), логика и `@action` — в **`app/views.py`**.
- **Страницы сайта** — в **`app/urls.py`** в том же файле, списком `path(...)`.
- **Auth (Djoser)** — подключаются в **`laboratory_work_3/urls.py`**, сами URL определены в пакете Djoser, не в вашем коде.
- Открыть список API в браузере: **`/api/`**.
