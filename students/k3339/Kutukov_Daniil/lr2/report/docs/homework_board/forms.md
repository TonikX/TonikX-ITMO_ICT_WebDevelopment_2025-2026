# Формы - Homework Board

## 📋 Обзор

В проекте используются различные формы для работы с данными, валидации и обеспечения безопасности.

## 👤 Формы пользователей

### CustomUserCreationForm

Форма регистрации нового пользователя, расширяющая стандартную `UserCreationForm`.

```python
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'student_id', 
            'phone', 
            'birth_date'
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
```

**Особенности**:
- Расширяет стандартную форму регистрации Django
- Добавляет дополнительные поля (роль, студенческий билет, телефон)
- Делает email, имя и фамилию обязательными
- Использует HTML5 виджет для даты рождения

**Поля**:
- `username` - имя пользователя (обязательное)
- `email` - email (обязательное)
- `first_name` - имя (обязательное)
- `last_name` - фамилия (обязательное)
- `role` - роль в системе
- `student_id` - студенческий билет (опционально)
- `phone` - телефон (опционально)
- `birth_date` - дата рождения (опционально)
- `password1` - пароль (наследуется)
- `password2` - подтверждение пароля (наследуется)

## 📝 Формы заданий

### AssignmentForm

Форма для создания и редактирования домашних заданий.

```python
class AssignmentForm(forms.ModelForm):
    """Форма создания/редактирования задания"""
    
    class Meta:
        model = Assignment
        fields = [
            'subject', 
            'title', 
            'description', 
            'due_date', 
            'penalty_info', 
            'max_points'
        ]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'penalty_info': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Настройка виджетов и помощи
        if user and user.role == User.TEACHER:
            # Можно добавить фильтрацию предметов для преподавателя
            pass
```

**Поля**:
- `subject` - предмет (выбор из списка)
- `title` - название задания
- `description` - подробное описание
- `due_date` - срок сдачи (datetime)
- `penalty_info` - информация о штрафах
- `max_points` - максимальный балл

**Виджеты**:
- `datetime-local` для поля даты/времени
- `Textarea` для текстовых полей

**Валидация**:
```python
def clean_due_date(self):
    due_date = self.cleaned_data.get('due_date')
    if due_date and due_date < timezone.now():
        raise forms.ValidationError('Срок сдачи не может быть в прошлом!')
    return due_date

def clean_max_points(self):
    max_points = self.cleaned_data.get('max_points')
    if max_points < 1:
        raise forms.ValidationError('Максимальный балл должен быть больше 0!')
    return max_points
```

## 📤 Форма сдачи

### SubmissionForm

Форма для сдачи выполненного задания студентом.

```python
class SubmissionForm(forms.ModelForm):
    """Форма сдачи задания"""
    
    class Meta:
        model = Submission
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10, 
                'placeholder': 'Введите текст вашего решения...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment', None)
        super().__init__(*args, **kwargs)
        
        if self.assignment:
            self.fields['content'].help_text = f"Задание: {self.assignment.title}"
```

**Поля**:
- `content` - текст решения задания

**Особенности**:
- Принимает объект задания для отображения контекста
- Большое текстовое поле для ввода решения
- Подсказка с названием задания

**Использование**:
```python
# В представлении
form = SubmissionForm(assignment=assignment)
```

## ⭐ Форма оценивания

### GradeForm

Форма для выставления оценки преподавателем.

```python
class GradeForm(forms.ModelForm):
    """Форма оценки задания"""
    
    class Meta:
        model = Grade
        fields = ['points', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.submission = kwargs.pop('submission', None)
        super().__init__(*args, **kwargs)
        
        if self.submission:
            max_points = self.submission.assignment.max_points
            self.fields['points'].widget.attrs['max'] = max_points
            self.fields['points'].help_text = f"Максимальный балл: {max_points}"
```

**Поля**:
- `points` - количество баллов
- `feedback` - комментарий преподавателя

**Валидация**:
```python
def clean_points(self):
    points = self.cleaned_data.get('points')
    if self.submission and points > self.submission.assignment.max_points:
        raise forms.ValidationError(
            f'Баллы не могут превышать максимум ({self.submission.assignment.max_points})!'
        )
    if points < 0:
        raise forms.ValidationError('Баллы не могут быть отрицательными!')
    return points
```

## 🔍 Формы поиска

### AssignmentSearchForm

Форма для поиска и фильтрации заданий.

```python
class AssignmentSearchForm(forms.Form):
    """Форма поиска заданий"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию или описанию...',
            'class': 'form-control'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="Все предметы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'Все статусы'),
            ('active', 'Активные'),
            ('overdue', 'Просроченные'),
            ('completed', 'Сданные'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
```

**Поля**:
- `search` - текстовый поиск
- `subject` - фильтр по предмету
- `status` - фильтр по статусу

**Использование в шаблоне**:
```html
<form method="get" class="mb-4">
    {{ form.search }}
    {{ form.subject }}
    {{ form.status }}
    <button type="submit" class="btn btn-primary">Поиск</button>
</form>
```

### GradeSearchForm

Форма для поиска оценок.

```python
class GradeSearchForm(forms.Form):
    """Форма поиска оценок"""
    student = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по имени студента...',
            'class': 'form-control'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="Все предметы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_points = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Минимум баллов',
            'class': 'form-control'
        })
    )
```

## 🎨 Стилизация форм

### Bootstrap классы

Добавление Bootstrap классов к полям формы:

```python
class StyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'
```

### Crispy Forms (опционально)

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))
```

## ✅ Примеры валидации

### Пользовательская валидация полей

```python
def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError('Пользователь с таким email уже существует!')
    return email
```

### Валидация нескольких полей

```python
def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get('created_at')
    due_date = cleaned_data.get('due_date')
    
    if start_date and due_date and due_date <= start_date:
        raise forms.ValidationError(
            'Срок сдачи должен быть после даты создания!'
        )
    
    return cleaned_data
```

## 🔐 CSRF защита

Все формы автоматически защищены от CSRF атак через Django middleware.

**В шаблоне**:
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Отправить</button>
</form>
```

## 📝 Примеры использования

### Создание формы в представлении

```python
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(user=request.user)
    
    return render(request, 'assignment_form.html', {'form': form})
```

### Редактирование объекта

```python
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', pk=pk)
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'assignment_form.html', {'form': form})
```

### Обработка ошибок

```python
if form.is_valid():
    # Сохранение
else:
    # form.errors содержит все ошибки валидации
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f'{field}: {error}')
```

---

!!! tip "Совет"
    Всегда валидируйте данные на стороне сервера, даже если есть клиентская валидация!
