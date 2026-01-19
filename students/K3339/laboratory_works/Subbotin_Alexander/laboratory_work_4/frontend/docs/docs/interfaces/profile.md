# Интерфейс профиля

## Страница профиля (ProfilePage)

### Описание

Страница профиля позволяет пользователю просматривать и редактировать личные данные.

### Секции

1. **Информация об аккаунте** — имя пользователя, email, дата регистрации
2. **Личные данные** — дата рождения (редактируемая)

---

## Информация об аккаунте

### Отображаемые данные

| Поле | Редактирование |
|------|----------------|
| Имя пользователя | ❌ |
| Email | ❌ |
| Дата регистрации | ❌ |

### API-запрос

```
GET /auth/me
Authorization: Bearer <token>
```

### Ответ

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-01-01T10:00:00Z"
}
```

---

## Личные данные

### Профиль пользователя

| Поле | Редактирование |
|------|----------------|
| Дата рождения | ✅ |

### API-запросы

**Получение профиля:**
```
GET /auth/me/profile
Authorization: Bearer <token>
```

**Ответ:**
```json
{
  "id": 1,
  "user_id": 1,
  "date_of_birth": "1990-05-15T00:00:00Z"
}
```

**Обновление профиля:**
```
PUT /auth/me/profile
Content-Type: application/json
Authorization: Bearer <token>

{
  "date_of_birth": "1990-05-15T00:00:00Z"
}
```

---

## Режим редактирования

### Переключение

```tsx
const [isEditing, setIsEditing] = useState(false);
```

### Форма редактирования

```tsx
<form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="date_of_birth">Дата рождения</Label>
    <Input
      id="date_of_birth"
      type="date"
      {...register('date_of_birth')}
    />
  </div>
  <div className="flex space-x-2">
    <Button type="submit" disabled={isPending}>
      {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      Сохранить
    </Button>
    <Button type="button" variant="outline" onClick={handleCancel}>
      Отмена
    </Button>
  </div>
</form>
```

### Отмена редактирования

```typescript
const handleCancel = () => {
  setIsEditing(false);
  reset({
    date_of_birth: profile?.date_of_birth 
      ? format(new Date(profile.date_of_birth), 'yyyy-MM-dd') 
      : '',
  });
};
```

---

## Обновление данных

### Mutation

```typescript
const updateProfileMutation = useMutation({
  mutationFn: authApi.updateProfile,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['profile'] });
    toast({
      title: 'Успешно!',
      description: 'Профиль обновлён',
    });
    setIsEditing(false);
  },
  onError: () => {
    toast({
      variant: 'destructive',
      title: 'Ошибка',
      description: 'Не удалось обновить профиль',
    });
  },
});
```

---

## Компоненты

### Информационная строка

```tsx
<div className="flex items-center space-x-4">
  <User className="h-5 w-5 text-muted-foreground" />
  <div>
    <p className="text-sm font-medium">Имя пользователя</p>
    <p className="text-sm text-muted-foreground">{user?.username}</p>
  </div>
</div>
```

### Карточка информации

```tsx
<Card>
  <CardHeader>
    <CardTitle>Информация об аккаунте</CardTitle>
    <CardDescription>Основные данные вашей учётной записи</CardDescription>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Информационные строки */}
  </CardContent>
</Card>
```

---

## Форматирование даты

```typescript
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

// Для отображения
format(new Date(date), 'd MMMM yyyy', { locale: ru })
// Результат: "15 мая 1990"

// Для формы
format(new Date(date), 'yyyy-MM-dd')
// Результат: "1990-05-15"
```
