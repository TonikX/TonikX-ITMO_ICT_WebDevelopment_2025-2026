# UI-компоненты

## Обзор

Проект использует библиотеку **shadcn/ui** — набор переиспользуемых компонентов, построенных на Radix UI и стилизованных с помощью Tailwind CSS.

## Установленные компоненты

| Компонент | Описание |
|-----------|----------|
| Button | Кнопки разных вариантов и размеров |
| Card | Карточка с заголовком и содержимым |
| Input | Поле ввода текста |
| Textarea | Многострочное поле ввода |
| Label | Метка для полей формы |
| Badge | Метка/тег для статусов |
| Avatar | Аватар пользователя |
| Dialog | Модальное окно |
| DropdownMenu | Выпадающее меню |
| Select | Выпадающий список выбора |
| Separator | Разделитель |
| Toast | Уведомления |

---

## Button

### Варианты

```tsx
<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button variant="destructive">Destructive</Button>
```

### Размеры

```tsx
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

### С загрузкой

```tsx
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Сохранить
</Button>
```

---

## Card

### Структура

```tsx
<Card>
  <CardHeader>
    <CardTitle>Заголовок</CardTitle>
    <CardDescription>Описание</CardDescription>
  </CardHeader>
  <CardContent>
    Содержимое карточки
  </CardContent>
  <CardFooter>
    <Button>Действие</Button>
  </CardFooter>
</Card>
```

---

## Dialog

### Базовое использование

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogTrigger asChild>
    <Button>Открыть</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Заголовок</DialogTitle>
      <DialogDescription>Описание</DialogDescription>
    </DialogHeader>
    {/* Содержимое */}
    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Отмена
      </Button>
      <Button onClick={handleSubmit}>
        Подтвердить
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## Toast

### Использование

```tsx
import { useToast } from '@/components/ui/use-toast';

const { toast } = useToast();

// Успешное уведомление
toast({
  title: 'Успешно!',
  description: 'Операция выполнена',
});

// Уведомление об ошибке
toast({
  variant: 'destructive',
  title: 'Ошибка',
  description: 'Что-то пошло не так',
});
```

### Настройка

Добавьте `<Toaster />` в корневой компонент:

```tsx
// main.tsx
import { Toaster } from '@/components/ui/toaster';

<App />
<Toaster />
```

---

## DropdownMenu

### Пример меню пользователя

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" className="h-8 w-8 rounded-full">
      <Avatar>
        <AvatarFallback>U</AvatarFallback>
      </Avatar>
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuLabel>Мой аккаунт</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem onClick={() => navigate('/profile')}>
      <User className="mr-2 h-4 w-4" />
      Профиль
    </DropdownMenuItem>
    <DropdownMenuItem onClick={logout}>
      <LogOut className="mr-2 h-4 w-4" />
      Выйти
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

---

## Select

### Пример выбора оценки

```tsx
<Select
  value={rating.toString()}
  onValueChange={(value) => setValue('rating', parseInt(value))}
>
  <SelectTrigger className="w-24">
    <SelectValue placeholder="Оценка" />
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

---

## Badge

### Варианты

```tsx
<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge variant="outline">Outline</Badge>
```

### С иконкой

```tsx
<Badge className="bg-green-500">
  <Check className="h-3 w-3 mr-1" />
  Подтверждено
</Badge>
```

---

## Утилиты

### cn()

Функция для объединения классов Tailwind:

```typescript
import { cn } from '@/lib/utils';

<div className={cn(
  "base-class",
  condition && "conditional-class",
  className
)} />
```

### Реализация

```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```
