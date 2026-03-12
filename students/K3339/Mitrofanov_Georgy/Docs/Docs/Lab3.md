# Лабораторная работа №3
## Реализация серверной части на django rest. Документирование API.

**Студент:** Митрофанов Георгий Алексеевич  
**Университет:** ИТМО  
**Группа:** К3339  
**Вариант:** Облачное хранилище файлов (аналог Google Drive)

---

## Описание проекта

Разработано облачное хранилище файлов, позволяющее пользователям загружать, скачивать и управлять своими файлами и папками, а также делиться ими с другими пользователями по ссылкам.

---

## Модели данных

### Модель Folder

Модель для хранения информации о папках пользователя.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | CharField | Название папки |
| `owner` | ForeignKey(User) | Владелец папки |
| `parent` | ForeignKey('self') | Родительская папка (для вложенных папок) |
| `created_at` | DateField | Дата создания |

**Особенности:**
- `unique_together = ('owner', 'parent', 'name')` — уникальность имени в пределах одной папки
- Поле `parent` ссылается само на себя, что позволяет создавать вложенные структуры

```python
class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    parent = models.ForeignKey("self", null=True, blank=True, 
                               on_delete=models.CASCADE, related_name="children")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'parent', 'name')
        ordering = ["created_at"]
    
    def __str__(self):
        return self.name
```

## Модель File


```python
class File(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL, related_name="files")
    file = models.FileField(upload_to='content/')
    size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True) 
    preview_image = models.ImageField(upload_to="previews/", null=True, blank=True)
    duration_ms = models.BigIntegerField(null=True, blank=True)
    collaborators = models.ManyToManyField(User, related_name="shared_files", blank=True)
    
    def __str__(self):
        return self.name
```


## Модель SharedLink

```python
class SharedLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="shared_links")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_downloads = models.PositiveIntegerField(null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.token)

    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        if self.max_downloads is not None and self.download_count >= self.max_downloads:
            return True
        return False

    def increment_download(self):
        self.download_count += 1
        self.save()
```

## Эндпоинты API

### Files (Файлы)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/files/` | Список всех файлов текущего пользователя |
| POST | `/api/files/` | Загрузить новый файл |
| GET | `/api/files/{id}/` | Детальная информация о файле |
| PUT/PATCH | `/api/files/{id}/` | Обновить информацию о файле |
| DELETE | `/api/files/{id}/` | Удалить файл (мягкое удаление) |

#### Специальные действия:

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/files/{id}/download/` | Скачать файл |
| GET | `/api/files/{id}/preview/` | Получить превью файла |
| POST | `/api/files/{id}/move/` | Переместить файл в другую папку |
| POST | `/api/files/{id}/share/` | Создать публичную ссылку на файл |
| POST | `/api/files/bulk_upload/` | Загрузить несколько файлов сразу |

---

### Folders (Папки)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/folders/` | Список всех папок пользователя |
| POST | `/api/folders/` | Создать новую папку |
| GET | `/api/folders/{id}/` | Детальная информация о папке |
| PUT/PATCH | `/api/folders/{id}/` | Обновить папку (переименовать) |
| DELETE | `/api/folders/{id}/` | Удалить папку |

#### Специальные действия:

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/folders/{id}/content/` | Получить содержимое папки (вложенные папки и файлы) |

---

### Public (Публичные ссылки)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/p/{token}/` | Доступ к файлу по публичной ссылке (не требует авторизации) |

---

### Auth (Авторизация)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/auth/users/` | Регистрация нового пользователя |
| POST | `/api/auth/jwt/create/` | Получение JWT токена (вход) |
| POST | `/api/auth/jwt/refresh/` | Обновление токена |
| GET | `/api/auth/users/me/` | Информация о текущем пользователе |

---

### Документация

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/swagger/` | Swagger UI документация |
| GET | `/redoc/` | ReDoc документация |
| GET | `/swagger.json/` | JSON схема API |