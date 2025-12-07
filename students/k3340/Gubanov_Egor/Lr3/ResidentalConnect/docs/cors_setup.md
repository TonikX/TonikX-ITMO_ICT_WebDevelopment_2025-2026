# Настройка CORS (Cross-origin resource sharing)

## Что такое CORS?

Cross-Origin Resource Sharing (CORS) — механизм, использующий дополнительные HTTP-заголовки, чтобы дать возможность агенту пользователя получать разрешения на доступ к выбранным ресурсам с сервера на источнике (домене), отличном от того, который использует сайт в данный момент.

Говорят, что агент пользователя делает запрос с другого источника (cross-origin HTTP request), если источник текущего документа отличается от запрашиваемого ресурса доменом, протоколом или портом.

### Пример cross-origin запроса

HTML страница, обслуживаемая сервером с `http://domain-a.com`, запрашивает `<img>` src по адресу `http://domain-b.com/image.jpg`. Сегодня многие страницы загружают ресурсы вроде CSS-стилей, изображений и скриптов с разных доменов, соответствующих разным сетям доставки контента (Content delivery networks, CDNs).

## Почему браузер блокирует запросы?

В целях безопасности браузеры ограничивают cross-origin запросы, инициируемые скриптами. Например, XMLHttpRequest и Fetch API следуют политике одного источника (same-origin policy). Это значит, что web-приложения, использующие такие API, могут запрашивать HTTP-ресурсы только с того домена, с которого были загружены, пока не будут использованы CORS-заголовки.

Механизм CORS поддерживает кросс-доменные запросы и передачу данных между браузером и web-серверами по защищенному соединению. Современные браузеры используют CORS в API-контейнерах, таких как XMLHttpRequest или Fetch, чтобы снизить риски, присущие запросам с других источников.

## Простые и сложные запросы

Стандарт CORS различает "простые" и "сложные" запросы.

### Простые запросы

Простым считается запрос, работающий со следующими методами:

- HEAD
- GET
- POST

И заголовками:

- Accept
- Accept-Language
- Content-Language
- Last-Event-ID
- Content-Type, но только со значениями:
  - `application/x-www-form-urlencoded`
  - `multipart/form-data`
  - `text/plain`

Если запрос удовлетворяет этим критериям, можно отсылать Ajax-запрос к другому домену из любого современного браузера. При этом браузер добавит заголовок `Origin` с адресом страницы, откуда инициирован запрос. Подделать заголовок скриптом не удастся.

Сервер, получив на обработку подобный запрос, должен прочесть `Origin` и решить, как его обрабатывать. Заголовок ответа `Access-Control-Allow-Origin` регулирует, с какого домена разрешено запрашивать данные. Это может быть как веб-адрес, так и знак астерикса (звездочки), если разрешено всем.

#### Пример простого CORS-запроса:

**Запрос:**
```
POST /foo/bar HTTP/1.1
Origin: http://foreign.com
Host: test.com
```

**Ответ с разрешением:**
```
200 OK HTTP/1.1
Access-Control-Allow-Origin: http://foreign.com
Content-Type: text/html; charset=utf-8

<h1>Welldone</h1>
```

### Сложные запросы (Preflight)

Необходимо обратить внимание, что рассматривается ситуация в которой ведется взаимодействие с чужими API. С вероятностью почти 100% они работают по протоколу JSON, то есть принимают и отдают заголовок `Content-Type: application/json`. Такой запрос автоматически перестает быть простым и переходит в разряд "сложных", где схема взаимодействия иная.

Сложные запросы проходят в два этапа. Сначала браузер делает запрос по тому же URL, но методом OPTIONS. Сервер должен ответить: какими другими методами и дополнительными заголовками (помимо стандартных) можно обращаться к этому урлу. И только получив разрешение, браузер сделает запрос на основной URL.

При этом браузер все запомнит: если разрешили только методы GET и POST, то PUT и DELETE не сработают. Аналогично с заголовками: если помимо стандартных разрешено использовать только Authorization, то нужно передать его и ничего другого.

Первая стадия, когда делается запрос OPTION, официально называется **preflight request**. Необходимо отметить, что такое взаимодействие весьма прозрачно отражается в браузере. Например, в консоли разработчика в Хроме видны оба запроса со всеми заголовками.

#### Пример сложного запроса (Preflight):

**Preflight запрос (OPTIONS):**
```
OPTIONS /cors HTTP/1.1
Origin: http://api.bob.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: X-Custom-Header
Host: api.alice.com
Accept-Language: en-US
Connection: keep-alive
User-Agent: Mozilla/5.0...
```

Клиент хотел отправить Ajax-запрос методом PUT на URL `http://api.alice.com/cors` с сайта `http://api.bob.com`. Поскольку это сложный запрос, браузер запросил разрешение: "хочу сделать PUT на этот URL с особым заголовком X-Custom-Header".

**Ответ сервера на preflight:**
```
200 OK HTTP/1.1
Access-Control-Allow-Origin: http://api.bob.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: X-Custom-Header
Content-Type: text/html; charset=utf-8
```

Таким образом, разрешено использовать методы GET, POST, PUT с заголовком X-Custom-Header. Это подходит под критерии первоначального запроса. Браузер делает второй запрос по реальному URL-адресу.

## Как работает OPTIONS запрос

OPTIONS запрос — это предварительный запрос (preflight request), который браузер автоматически отправляет перед сложными CORS-запросами. Этот запрос позволяет серверу сообщить браузеру:

- Какие HTTP-методы разрешены (`Access-Control-Allow-Methods`)
- Какие заголовки разрешены (`Access-Control-Allow-Headers`)
- С каких источников разрешены запросы (`Access-Control-Allow-Origin`)
- Можно ли отправлять credentials (`Access-Control-Allow-Credentials`)

Браузер анализирует ответ на OPTIONS запрос и решает, можно ли выполнить основной запрос. Если сервер не отвечает правильно на OPTIONS запрос, браузер блокирует основной запрос и выдает ошибку CORS.

## Настройка CORS в Django через django-cors-headers

### 1. Установка зависимости

Установите `django-cors-headers` с помощью pip:

```bash
pip install django-cors-headers
```

Или добавьте в `requirements.txt`:

```
django-cors-headers==4.3.1
```

Затем установите зависимости:

```bash
pip install -r requirements.txt
```

### 2. Настройка settings.py

#### Добавление в INSTALLED_APPS

Добавьте `corsheaders` в `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'corsheaders',
    'residential_app',
]
```

#### Добавление в MIDDLEWARE

Добавьте `corsheaders.middleware.CorsMiddleware` в `MIDDLEWARE` **перед** `CommonMiddleware`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Важно:** `CorsMiddleware` должен быть размещен как можно выше в списке middleware, особенно перед любым middleware, которое может генерировать ответы, таким как `CommonMiddleware`.

#### Настройка разрешенных источников

**Вариант 1: Разрешить все источники (для разработки)**

```python
CORS_ALLOW_ALL_ORIGINS = True
```

**Вариант 2: Разрешить только указанные домены (для production)**

```python
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 3. Создание тестового endpoint

Создайте тестовый endpoint для проверки работы CORS в `residential_app/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_cors(request):
    return Response({"message": "CORS работает!"})
```

### 4. Добавление маршрута

Добавьте маршрут в `residential_app/urls.py`:

```python
from django.urls import path
from .views import test_cors

urlpatterns = [
    path('test-cors/', test_cors, name='test-cors'),
    # ... другие маршруты
]
```

Полный URL будет: `http://localhost:8000/api/test-cors/`

## Проверка работы CORS

### Тест из браузера (консоль разработчика)

Откройте консоль браузера (F12) на любой странице и выполните:

```javascript
fetch("http://localhost:8000/api/test-cors/")
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

### Ожидаемый результат при правильной настройке

**Успешный ответ:**
```json
{
  "message": "CORS работает!"
}
```

В Network вкладке браузера вы увидите:
- Заголовок ответа: `Access-Control-Allow-Origin: *` (если `CORS_ALLOW_ALL_ORIGINS = True`)
- Статус: `200 OK`

### Пример ошибки браузера (до настройки CORS)

Если CORS не настроен, вы увидите ошибку в консоли:

```
Access to fetch at 'http://localhost:8000/api/test-cors/' from origin 'http://localhost:5173' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

Эта ошибка означает, что сервер не отправляет заголовок `Access-Control-Allow-Origin` в ответе, и браузер блокирует запрос из соображений безопасности.

### После настройки CORS

После правильной настройки CORS эта ошибка исчезнет, и запрос будет успешно выполнен. В Network вкладке вы увидите:

**Заголовки запроса:**
```
GET /api/test-cors/ HTTP/1.1
Host: localhost:8000
Origin: http://localhost:5173
```

**Заголовки ответа:**
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: application/json
```

## Дополнительные настройки CORS

### Разрешение конкретных заголовков

```python
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### Разрешение конкретных методов

```python
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### Разрешение передачи cookies

```python
CORS_ALLOW_CREDENTIALS = True
```

При использовании `CORS_ALLOW_CREDENTIALS = True` необходимо указать конкретные домены в `CORS_ALLOWED_ORIGINS` (нельзя использовать `CORS_ALLOW_ALL_ORIGINS = True`).

## Полезные ссылки

- [Документация django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Django REST Framework: CORS](https://www.django-rest-framework.org/topics/ajax-csrf-cors/)

