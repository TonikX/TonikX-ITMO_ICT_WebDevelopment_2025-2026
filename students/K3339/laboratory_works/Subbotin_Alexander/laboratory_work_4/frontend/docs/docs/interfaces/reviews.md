# Интерфейс отзывов

## Описание

Отзывы отображаются на странице детальной информации о туре. Авторизованные пользователи могут оставлять отзывы.

## Секция отзывов

### Структура

1. **Заголовок** — название секции и средний рейтинг
2. **Форма добавления** — доступна авторизованным
3. **Список отзывов** — все отзывы к туру

### Средний рейтинг

```typescript
const averageRating = reviews.length > 0
  ? (reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length).toFixed(1)
  : null;
```

---

## Добавление отзыва

### Форма

| Поле | Тип | Обязательное | Валидация |
|------|-----|--------------|-----------|
| Текст отзыва | textarea | Да | Минимум 1 символ |
| Оценка | select | Да | 1-10 |

### Компонент оценки

```tsx
<Select
  value={rating.toString()}
  onValueChange={(value) => setValue('rating', parseInt(value))}
>
  <SelectTrigger className="w-24">
    <SelectValue />
  </SelectTrigger>
  <SelectContent>
    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
      <SelectItem key={n} value={n.toString()}>
        {n}
      </SelectItem>
    ))}
  </SelectContent>
</Select>
```

### API-запрос

```
POST /reviews/
Content-Type: application/json
Authorization: Bearer <token>

{
  "tour_id": 5,
  "text": "Отличный тур! Всё очень понравилось.",
  "rating": 9
}
```

### Ответ

```json
{
  "id": 1,
  "tour_id": 5,
  "user_id": 1,
  "text": "Отличный тур! Всё очень понравилось.",
  "rating": 9,
  "created_at": "2025-01-10T15:30:00Z"
}
```

---

## Получение отзывов

### API-запрос

```
GET /reviews/tour/{tour_id}
```

### Ответ

```json
[
  {
    "id": 1,
    "tour_id": 5,
    "user_id": 1,
    "text": "Отличный тур!",
    "rating": 9,
    "created_at": "2025-01-10T15:30:00Z",
    "username": "johndoe"
  }
]
```

---

## Отображение отзыва

### Карточка отзыва

```tsx
<div className="border rounded-lg p-4">
  <div className="flex justify-between items-start mb-2">
    <span className="font-medium">
      {review.username || 'Аноним'}
    </span>
    <Badge>{review.rating} / 10</Badge>
  </div>
  <p className="text-sm text-muted-foreground">
    {review.text}
  </p>
  <p className="text-xs text-muted-foreground mt-2">
    {format(new Date(review.created_at), 'd MMMM yyyy', { locale: ru })}
  </p>
</div>
```

---

## Система оценок

| Оценка | Интерпретация |
|--------|---------------|
| 1-3 | Плохо |
| 4-5 | Ниже среднего |
| 6-7 | Хорошо |
| 8-9 | Очень хорошо |
| 10 | Отлично |

---

## Состояния

### Загрузка

```tsx
{reviewsLoading ? (
  <div className="flex justify-center py-4">
    <Loader2 className="h-6 w-6 animate-spin" />
  </div>
) : ...}
```

### Нет отзывов

```tsx
{reviews.length === 0 && (
  <p className="text-center text-muted-foreground py-4">
    Пока нет отзывов
  </p>
)}
```

### Ошибка отправки

При ошибке отправки отзыва показывается toast:

```tsx
toast({
  variant: 'destructive',
  title: 'Ошибка',
  description: 'Не удалось добавить отзыв',
});
```

---

## Обновление данных

После добавления отзыва автоматически инвалидируется кэш:

```typescript
const reviewMutation = useMutation({
  mutationFn: reviewsApi.create,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['reviews', tourId] });
    toast({ title: 'Успешно!', description: 'Отзыв добавлен' });
    reviewForm.reset();
  },
});
```
