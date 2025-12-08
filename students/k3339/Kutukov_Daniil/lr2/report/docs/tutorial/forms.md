# Формы - Tutorial

## 📋 Обзор

В проекте используются две основные формы для работы с владельцами и водительскими удостоверениями.

## 👤 OwnerForm

Форма для создания и редактирования владельцев автомобилей.

```python
from django import forms
from .models import User

class OwnerForm(forms.ModelForm):
    """Форма для создания/редактирования владельца автомобиля"""
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'passport_number',
            'home_address',
            'nationality',
            'birth_date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
        }
```

### Поля формы

| Поле | Тип виджета | Обязательное |
|------|-------------|--------------|
| `username` | TextInput | Да |
| `first_name` | TextInput | Нет |
| `last_name` | TextInput | Нет |
| `email` | EmailInput | Нет |
| `passport_number` | TextInput | Нет |
| `home_address` | Textarea | Нет |
| `nationality` | TextInput | Нет |
| `birth_date` | DateInput (date) | Нет |

### Использование

```python
# Создание нового владельца
form = OwnerForm(request.POST)
if form.is_valid():
    owner = form.save()

# Редактирование существующего
owner = User.objects.get(pk=1)
form = OwnerForm(request.POST, instance=owner)
if form.is_valid():
    form.save()
```

## 🪪 DriverLicenseForm

Форма для регистрации водительских удостоверений.

```python
class DriverLicenseForm(forms.ModelForm):
    """Форма для создания/редактирования водительского удостоверения"""
    
    class Meta:
        model = DriverLicense
        fields = [
            'owner',
            'license_number',
            'license_type',
            'issue_date'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'license_type': forms.Select(attrs={'class': 'form-control'}),
        }
```

### Поля формы

| Поле | Тип виджета | Обязательное |
|------|-------------|--------------|
| `owner` | Select | Да |
| `license_number` | TextInput | Да |
| `license_type` | Select | Да |
| `issue_date` | DateInput (date) | Да |

### Выбор категории

Доступные категории водительских удостоверений:

- **A** - Мотоциклы
- **B** - Легковые автомобили
- **C** - Грузовые автомобили
- **D** - Автобусы

## 🚗 Формы для автомобилей

Для автомобилей используется прямое указание полей в классовых представлениях:

```python
class CarCreateView(CreateView):
    model = Car
    fields = ['brand', 'model', 'color', 'state_number']
    # ...
```

Это эквивалентно созданию формы:

```python
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'color', 'state_number']
```

## ✅ Валидация

### Валидация на уровне модели

```python
# В models.py
state_number = models.CharField(
    max_length=10,
    validators=[MinLengthValidator(1), MaxLengthValidator(10)]
)
```

### Кастомная валидация в формах

```python
class OwnerForm(forms.ModelForm):
    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number')
        if passport and len(passport.replace(' ', '')) != 10:
            raise forms.ValidationError('Неверный формат паспорта')
        return passport
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            if not self.instance.pk or self.instance.email != email:
                raise forms.ValidationError('Email уже используется')
        return email
```

### Валидация нескольких полей

```python
def clean(self):
    cleaned_data = super().clean()
    first_name = cleaned_data.get('first_name')
    last_name = cleaned_data.get('last_name')
    
    if not first_name and not last_name:
        raise forms.ValidationError(
            'Необходимо заполнить хотя бы имя или фамилию'
        )
    
    return cleaned_data
```

## 🎨 Стилизация форм

### Добавление Bootstrap классов

```python
class OwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
```

### Использование в шаблоне

```html
<form method="post">
    {% csrf_token %}
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
        {{ field }}
        {% if field.errors %}
        <div class="invalid-feedback d-block">
            {{ field.errors }}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Сохранить</button>
</form>
```

## 📝 Примеры использования

### Создание владельца

```python
def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            owner = form.save()
            messages.success(request, 'Владелец создан!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm()
    
    return render(request, 'owner_form.html', {'form': form})
```

### Редактирование

```python
def owner_update(request, owner_id):
    owner = get_object_or_404(User, pk=owner_id)
    
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm(instance=owner)
    
    return render(request, 'owner_form.html', {
        'form': form,
        'owner': owner
    })
```

---

!!! tip "Совет"
    Всегда валидируйте данные на сервере, даже если есть клиентская валидация!
