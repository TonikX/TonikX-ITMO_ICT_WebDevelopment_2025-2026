# Представления - Homework Board

## 📋 Обзор

В проекте используются как функциональные (Function-Based Views), так и классовые представления (Class-Based Views) для обработки различных запросов.

## 🏠 Главная страница

### `home(request)`

Функциональное представление для главной страницы.

```python
def home(request):
    """Главная страница"""
    context = {
        'total_assignments': Assignment.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.count(),
        'recent_assignments': Assignment.objects.filter(is_active=True).order_by('-created_at')[:5],
    }
    
    if request.user.is_authenticated:
        if request.user.role == User.STUDENT:
            context['my_submissions'] = Submission.objects.filter(
                student=request.user
            ).order_by('-submitted_at')[:5]
        elif request.user.role in [User.TEACHER, User.ADMIN]:
            context['pending_grades'] = Submission.objects.filter(
                grade__isnull=True
            ).count()
    
    return render(request, 'assignments/home.html', context)
```

**URL**: `/`  
**Template**: `assignments/home.html`  
**Требует аутентификации**: Нет

**Передаваемый контекст**:
- `total_assignments` - количество активных заданий
- `total_subjects` - количество предметов
- `recent_assignments` - 5 последних заданий
- `my_submissions` - последние сдачи студента (если студент)
- `pending_grades` - количество непроверенных работ (если преподаватель)

## 👤 Регистрация

### `register(request)`

Регистрация нового пользователя.

```python
def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'assignments/register.html', {'form': form})
```

**URL**: `/register/`  
**Template**: `assignments/register.html`  
**Методы**: GET, POST

## 📚 Работа с заданиями

### AssignmentListView

Классовое представление для списка заданий с поиском и фильтрацией.

```python
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Assignment.objects.filter(
            is_active=True
        ).select_related('subject', 'teacher').order_by('-created_at')
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(subject__name__icontains=search)
            )
        
        # Фильтр по предмету
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status == 'overdue':
            queryset = queryset.filter(due_date__lt=timezone.now())
        elif status == 'active':
            queryset = queryset.filter(due_date__gte=timezone.now())
        elif status == 'completed' and self.request.user.is_authenticated:
            submitted = Submission.objects.filter(
                student=self.request.user
            ).values_list('assignment_id', flat=True)
            queryset = queryset.filter(id__in=submitted)
        
        return queryset
```

**URL**: `/assignments/`  
**Template**: `assignments/assignment_list.html`  
**Базовый класс**: `ListView`

**Особенности**:
- Поиск по названию, описанию и предмету
- Фильтрация по предмету и статусу
- Пагинация (10 заданий на страницу)
- Оптимизация через `select_related()`

### AssignmentDetailView

Детальная информация о задании.

```python
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        
        if self.request.user.is_authenticated and self.request.user.role == User.STUDENT:
            # Проверяем, сдал ли студент это задание
            try:
                submission = Submission.objects.get(
                    assignment=assignment,
                    student=self.request.user
                )
                context['my_submission'] = submission
                try:
                    context['my_grade'] = submission.grade
                except Grade.DoesNotExist:
                    pass
            except Submission.DoesNotExist:
                context['can_submit'] = True
        
        elif self.request.user.is_authenticated and self.request.user.role in [User.TEACHER, User.ADMIN]:
            context['submissions'] = Submission.objects.filter(
                assignment=assignment
            ).select_related('student', 'grade')
        
        return context
```

**URL**: `/assignments/<int:pk>/`  
**Template**: `assignments/assignment_detail.html`  
**Базовый класс**: `DetailView`

**Добавляемый контекст**:
- Для студентов: `my_submission`, `my_grade`, `can_submit`
- Для преподавателей: `submissions` (все сдачи)

### AssignmentCreateView

Создание нового задания (только для преподавателей).

```python
class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignment_list')
    
    def test_func(self):
        return self.request.user.role in [User.TEACHER, User.ADMIN]
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'Задание успешно создано!')
        return super().form_valid(form)
```

**URL**: `/assignments/create/`  
**Template**: `assignments/assignment_form.html`  
**Базовый класс**: `CreateView`  
**Требует аутентификации**: Да  
**Требуемая роль**: Преподаватель или Администратор

### AssignmentUpdateView

Редактирование задания.

```python
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    
    def test_func(self):
        assignment = self.get_object()
        return (self.request.user == assignment.teacher or 
                self.request.user.role == User.ADMIN)
    
    def get_success_url(self):
        return reverse_lazy('assignment_detail', kwargs={'pk': self.object.pk})
```

**URL**: `/assignments/<int:pk>/update/`  
**Проверка прав**: Автор задания или администратор

### AssignmentDeleteView

Удаление задания.

```python
class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = 'assignments/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignment_list')
    
    def test_func(self):
        assignment = self.get_object()
        return (self.request.user == assignment.teacher or 
                self.request.user.role == User.ADMIN)
```

**URL**: `/assignments/<int:pk>/delete/`

## 📤 Сдача заданий

### `submit_assignment(request, pk)`

Функциональное представление для сдачи задания студентом.

```python
@login_required
def submit_assignment(request, pk):
    """Сдача задания студентом"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    # Проверка роли
    if request.user.role != User.STUDENT:
        messages.error(request, 'Только студенты могут сдавать задания!')
        return redirect('assignment_detail', pk=pk)
    
    # Проверка на повторную сдачу
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.error(request, 'Вы уже сдали это задание!')
        return redirect('assignment_detail', pk=pk)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Задание успешно сдано!')
            return redirect('assignment_detail', pk=pk)
    else:
        form = SubmissionForm()
    
    return render(request, 'assignments/submit_form.html', {
        'form': form,
        'assignment': assignment
    })
```

**URL**: `/assignments/<int:pk>/submit/`  
**Требует аутентификации**: Да  
**Требуемая роль**: Студент

## ⭐ Оценивание

### GradeListView

Список всех оценок.

```python
class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'assignments/grade_list.html'
    context_object_name = 'grades'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Grade.objects.select_related(
            'submission__student',
            'submission__assignment',
            'graded_by'
        ).order_by('-graded_at')
        
        # Для студентов - только их оценки
        if self.request.user.role == User.STUDENT:
            queryset = queryset.filter(submission__student=self.request.user)
        
        # Поиск по студенту
        student_query = self.request.GET.get('student')
        if student_query:
            queryset = queryset.filter(
                Q(submission__student__username__icontains=student_query) |
                Q(submission__student__first_name__icontains=student_query) |
                Q(submission__student__last_name__icontains=student_query)
            )
        
        return queryset
```

**URL**: `/grades/`  
**Template**: `assignments/grade_list.html`

### `grade_submission(request, submission_id)`

Выставление оценки за сдачу.

```python
@login_required
def grade_submission(request, submission_id):
    """Выставление оценки преподавателем"""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Проверка роли
    if request.user.role not in [User.TEACHER, User.ADMIN]:
        messages.error(request, 'Только преподаватели могут выставлять оценки!')
        return redirect('assignment_detail', pk=submission.assignment.pk)
    
    # Проверка существующей оценки
    if hasattr(submission, 'grade'):
        messages.error(request, 'Оценка уже выставлена!')
        return redirect('assignment_detail', pk=submission.assignment.pk)
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.graded_by = request.user
            
            # Проверка максимального балла
            if grade.points > submission.assignment.max_points:
                form.add_error('points', f'Максимальный балл: {submission.assignment.max_points}')
            else:
                grade.save()
                messages.success(request, 'Оценка успешно выставлена!')
                return redirect('assignment_detail', pk=submission.assignment.pk)
    else:
        form = GradeForm()
    
    return render(request, 'assignments/grade_form.html', {
        'form': form,
        'submission': submission,
        'max_points': submission.assignment.max_points
    })
```

**URL**: `/grades/submission/<int:submission_id>/`  
**Требуемая роль**: Преподаватель или Администратор

## 📊 Статистика

### `statistics(request)`

Страница статистики.

```python
@login_required
def statistics(request):
    """Статистика по заданиям и оценкам"""
    context = {}
    
    if request.user.role == User.STUDENT:
        # Статистика студента
        submissions = Submission.objects.filter(student=request.user)
        grades = Grade.objects.filter(submission__student=request.user)
        
        context.update({
            'total_submissions': submissions.count(),
            'graded_submissions': grades.count(),
            'average_grade': grades.aggregate(Avg('points'))['points__avg'] or 0,
            'late_submissions': submissions.filter(is_late=True).count(),
        })
    
    elif request.user.role in [User.TEACHER, User.ADMIN]:
        # Статистика преподавателя
        assignments = Assignment.objects.filter(teacher=request.user)
        
        context.update({
            'total_assignments': assignments.count(),
            'total_submissions': Submission.objects.filter(
                assignment__in=assignments
            ).count(),
            'pending_grades': Submission.objects.filter(
                assignment__in=assignments,
                grade__isnull=True
            ).count(),
        })
    
    return render(request, 'assignments/statistics.html', context)
```

**URL**: `/statistics/`  
**Требует аутентификации**: Да

## 👤 Личный кабинет

### `my_submissions(request)`

Список сдач текущего студента.

```python
@login_required
def my_submissions(request):
    """Мои сдачи"""
    if request.user.role != User.STUDENT:
        messages.error(request, 'Эта страница доступна только студентам!')
        return redirect('home')
    
    submissions = Submission.objects.filter(
        student=request.user
    ).select_related('assignment__subject', 'grade').order_by('-submitted_at')
    
    paginator = Paginator(submissions, 10)
    page = request.GET.get('page')
    submissions = paginator.get_page(page)
    
    return render(request, 'assignments/my_submissions.html', {
        'submissions': submissions
    })
```

**URL**: `/my-submissions/`  
**Требуемая роль**: Студент

### `profile(request)`

Профиль пользователя.

```python
@login_required
def profile(request):
    """Профиль пользователя"""
    return render(request, 'assignments/profile.html')
```

**URL**: `/profile/`

## 🔒 Декораторы и миксины

### Используемые декораторы

```python
from django.contrib.auth.decorators import login_required
```

- `@login_required` - требует аутентификации

### Используемые миксины

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
```

- `LoginRequiredMixin` - требует аутентификации
- `UserPassesTestMixin` - проверка через метод `test_func()`

### Примеры проверки прав

```python
def test_func(self):
    # Только преподаватели и администраторы
    return self.request.user.role in [User.TEACHER, User.ADMIN]

def test_func(self):
    # Только автор или администратор
    assignment = self.get_object()
    return (self.request.user == assignment.teacher or 
            self.request.user.role == User.ADMIN)
```

---

!!! info "Оптимизация"
    Используйте `select_related()` и `prefetch_related()` для минимизации количества запросов к БД!
