**Лабораторная работа2**
- **Цель**: выполнить лабораторную работу по разработке Django-приложения с собственной моделью пользователя, CRUD для автомобилей, формой создания владельца, пагинацией и поиском.

**Структура**
- **`manage.py`**: стандартный Django CLI-скрипт для управления проектом.
- **`django_project_nikiforov/settings.py`**: настройки проекта (используетсяc стандартный`sqlite3`, `AUTH_USER_MODEL` переназначён на `project_first_app.User`).
- **`django_project_nikiforov/urls.py`**: подключает `admin/` и маршруты приложения `project_first_app`.
- **`project_first_app/`**: основное приложение с моделями, формами, представлениями и URL-ами.
- **`templates/`**: общие шаблоны и шаблоны приложения (`project_first_app/` внутри папки `templates`).

- **Настройка базы и запуск**:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Ключевые настройки**
- **Custom User**: в `settings.py` указано `AUTH_USER_MODEL = 'project_first_app.User'`. Это означает, что создана собственная модель пользователя `User` в `project_first_app.models`.
- **Templates**: шаблоны ищутся в `BASE_DIR / 'templates'` и в директориях приложений (см. `TEMPLATES` в `settings.py`).
- **DB**: используется `sqlite3` (`db.sqlite3` в корне проекта).

**Модели (см. `project_first_app/models.py`)**
- **`User`**: наследует `AbstractUser`. Дополнительные поля:
  - `passport_number`: `CharField` (макс 20).
  - `address`: `CharField`.
  - `nationality`: `CharField`.
  - `birth_date`: `DateTimeField`.
  - `cars`: `ManyToManyField('Car', through='Ownership')` — связь многие-ко-многим через промежуточную модель `Ownership`.
- **`Car`**:
  - `id_car`: `AutoField` (PK)
  - `plate_number`, `brand`, `model`, `color` — сведения об автомобиле.
- **`DriverLicense`**:
  - `id_license` (PK), `id_owner` (FK -> `User`), `license_number`, `license_type`, `issue_date`.
- **`Ownership`**:
  - ассоциативная таблица между `User` и `Car`: `id_owner` (FK -> `User`), `id_car` (FK -> `Car`), `start_date`, `end_date`.

**Админка (см. `project_first_app/admin.py`)**
- **Регистрация моделей**: `User`, `Car`, `DriverLicense`, `Ownership` зарегистрированы в админке.
- **UserAdmin** расширяет базовый `UserAdmin`, добавляет поля (`passport_number`, `address`, `nationality`, `birth_date`) в форму создания/редактирования и отображает дополнительные столбцы.

**Представления и маршруты**
- Все маршруты приложения определены в `project_first_app/urls.py` и подключены в `django_project_nikiforov/urls.py` на корневом уровне (`path('', include('project_first_app.urls'))`).
- **Владельцы (функциональные представления)**:
  - `owner_list` — вывод списка владельцев с поддержкой поиска (`q` GET-параметр) и пагинации (5 элементов на страницу). Реализована безопасная обработка несуществующих страниц (`PageNotAnInteger`, `EmptyPage`).
  - `owner_detail` — детальная страница владельца по `owner_id` с обработкой `User.DoesNotExist` (возврат `Http404`).
  - `create_owner` — форма создания владельца (используется `OwnerCreationForm`). При успешном сохранении выполняется `messages.success`, при ошибках — логирование и `messages.error`.
- **Автомобили (CBV)**:
  - `CarListView` — список автомобилей.
  - `CarDetailView` — детальная информация об автомобиле (pk аргумент `car_id`).
  - `CarCreateView` / `CarUpdateView` / `CarDeleteView` — стандартные CRUD-представления на основе классов с `success_url = reverse_lazy('car_list')`.

**URLs (основные)**
- `owner/list/` → `owner_list` (name=`owner_list`)
- `owner/create/` → `create_owner` (name=`owner_create`)
- `owner/<int:owner_id>/` → `owner_detail` (name=`owner_detail`)
- `car/list/` → `CarListView` (name=`car_list`)
- `car/create/` → `CarCreateView` (name=`car_create`)
- `car/<int:car_id>/` → `CarDetailView` (name=`car_detail`)
- `car/<int:car_id>/update/` → `CarUpdateView` (name=`car_update`)
- `car/<int:car_id>/delete/` → `CarDeleteView` (name=`car_delete`)

**Шаблоны**
- Расположение: `templates/` + `templates/project_first_app/`.
- Основные файлы:
  - `templates/base.html` — базовый шаблон (общая верстка, подключение сообщений и навигации).
  - `templates/owner_list.html` — список владельцев (с формой поиска и пагинацией).
  - `templates/owner.html` — детальная страница владельца.
  - `templates/owner_create.html` — страница с формой создания владельца.
  - `templates/car_list.html`, `templates/project_first_app/car_create.html`, `car_detail.html`, `car_update.html`, `car_delete.html` — CRUD-шаблоны для `Car`.

**Формы**
- Основная форма: `OwnerCreationForm` (см. `project_first_app/forms.py`) — форма создания пользователя с валидацией. `create_owner` использует эту форму и показывает сообщения об успехе/ошибках.

**Поведение и особенности реализации**
- **Поиск и пагинация**: `owner_list` использует `GET`-параметр `q` для фильтрации по `first_name`, `last_name`, `username` и `passport_number`. Пагинация реализована через `django.core.paginator.Paginator` с 5 элементами на страницу.
- **Custom User**: использована собственная модель `User`, поэтому во всём проекте надо ссылаться на неё через `get_user_model()` или `settings.AUTH_USER_MODEL`.
- **Ассоциативная таблица `Ownership`**: позволяет хранить периоды владения автомобилем (start/end), что расширяет семантику отношения между `User` и `Car`.
- **Админка**: настроена для удобного управления всеми сущностями; добавлены поисковые поля и фильтры.

**Что было сделано (кратко)**
- Создана кастомная модель пользователя `User` с дополнительными полями.
- Реализована предметная область: `Car`, `DriverLicense`, `Ownership`.
- Реализована полная CRUD-логика для автомобилей (CBV) и форма создания владельца (FBV).
- Добавлен поиск по владельцам и пагинация списка.
- Настроена админка для всех моделей.

**Запуск и проверка**
- После миграций и создания суперпользователя проверьте:
  - `http://127.0.0.1:8000/car/list/` — список автомобилей.
  - `http://127.0.0.1:8000/owner/list/` — список владельцев (поиск & навигация).
  - `http://127.0.0.1:8000/admin/` — админка (управление моделями и создание записей).

**Где смотреть код**
- Модели: `project_first_app/models.py`
- Представления: `project_first_app/views.py`
- Маршруты: `project_first_app/urls.py` и `django_project_nikiforov/urls.py`
- Админка: `project_first_app/admin.py`
- Шаблоны: `templates/` и `templates/project_first_app/`

**Дальнейшие улучшения (рекомендации)**
- Добавить тесты для представлений и форм (`project_first_app/tests.py`).
- Добавить валидацию/унификацию форматов для номеров паспортов и номеров авто.
- Добавить API (DRF) для работы с автомобилями и владельцами.
- Рассмотреть локализацию (`LANGUAGE_CODE`) и часовой пояс для корректного отображения дат.
