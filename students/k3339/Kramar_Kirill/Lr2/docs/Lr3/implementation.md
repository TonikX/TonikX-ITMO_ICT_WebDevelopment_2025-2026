### Руководство по использованию API для управления школьными данными

---

#### 1. **Регистрация пользователя**
- **URL:** `/auth/users/`
- **Метод:** `POST`

**Запрос:**
```http
POST /auth/users/
Content-Type: application/json

{
  "username": "user",
  "password": "123",
  "email": "user@example.com"
}
```

---

#### 2. **Получение токена авторизации**
- **URL:** `/auth/token/login/`
- **Метод:** `POST`

**Запрос:**
```http
POST /auth/token/login/
Content-Type: application/json

{
  "username": "user",
  "password": "123"
}
```

---

#### 3. **Получение информации о текущем пользователе**
- **URL:** `/auth/users/me/`
- **Метод:** `GET`

**Запрос:**
```http
GET /auth/users/me/
Authorization: Token token12314124
```

---

### Работа с API

#### 1. **Управление учителями**
- **Добавление учителя**
  - **URL:** `/teachers/`
  - **Метод:** `POST`

**Запрос:**
```http
POST /teachers/
Authorization: Token token12314124
Content-Type: application/json

{
  "first_name": "Ryan",
  "last_name": "Gosling",
  "middle_name": "",
  "classroom": 2,
  "subject": [2, 3]
}
```

---

#### 2. **Получение списка студентов**
- **URL:** `/students/`
- **Метод:** `GET`

**Запрос:**
```http
GET /students/
Authorization: Token token12314124
```

---

#### 3. **Получение информации о предмете для заданного урока**
- **URL:** `/class/<klass_id>/<weekday>/<lesson_number>/subject/`
- **Метод:** `GET`

**Запрос:**
```http
GET /class/5/Monday/1/subject/
Authorization: Token token12314124
```

---

#### 4. **Отчет о преподавателях**
- **URL:** `/subjects/teachers/count/`
- **Метод:** `GET`

**Запрос:**
```http
GET /subjects/teachers/count/
Authorization: Token token12314124
```

---

#### 5. **Отчет о мальчиках и девочках в каждом классе**
- **URL:** `/classes/gender/count/`
- **Метод:** `GET`

**Запрос:**
```http
GET /classes/gender/count/
Authorization: Token token12314124
```

---

#### 6. **Отчет по кабинетам для базовых и профильных дисциплин**
- **URL:** `/classrooms/count/`
- **Метод:** `GET`

**Запрос:**
```http
GET /classrooms/count/
Authorization: Token token12314124
```

---

#### 7. **Получение отчета об успеваемости класса**
- **URL:** `/class/<klass_id>/performance/`
- **Метод:** `GET`

**Запрос:**
```http
GET /class/5/performance/
Authorization: Token token12314124
```
---

### Swagger документация
Для визуализации и тестирования API используется Swagger UI:

- **URL:** `/doc/swagger/`
- Открывает интерфейс с подробной документацией всех эндпоинтов и их тестирование в браузере.

---