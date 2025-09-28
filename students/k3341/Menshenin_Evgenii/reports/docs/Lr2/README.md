# Отчет по лабораторной работе №2

## Описание выполненных задач

### 1. Хранение информации о домашнем задании
Реализована система хранения всей необходимой информации о домашних заданиях:
- Предмет (Subject model)
- Преподаватель (ForeignKey в Homework model)
- Дата выдачи (issue_date в Homework model)
- Период выполнения (issue_date и due_date в Homework model)
- Текст задания (description в Homework model)
- Информация о штрафах (Penalty model с типами штрафов и значениями)

### 2. Регистрация новых пользователей
Реализована система регистрации пользователей с использованием Django authentication:
- Создан Profile model для хранения дополнительной информации о пользователях (роль: ученик/учитель, класс)
- Интеграция с Django admin для управления пользователями

### 3. Просмотр домашних заданий по всем дисциплинам
Реализованы представления для просмотра домашних заданий:
- Список всех домашних заданий с отображением предмета, названия, даты выдачи и срока сдачи
- Детальная страница каждого задания с полным описанием

### 4. Сдача домашних заданий в текстовом виде
Создана форма для сдачи домашних заданий:
- Текстовое поле для ввода ответа на задание
- Автоматическое сохранение даты сдачи
- Проверка прав доступа (только ученики могут сдавать задания)

### 5. Возможность постановки оценки через Django-admin
Настроена админ-панель Django для управления оценками:
- Администраторы и учителя могут ставить оценки за задания
- Интерфейс включает фильтры и поиск по заданиям и студентам
- Интеграция с моделью Submission для хранения оценок и комментариев
### 6. Формирование таблицы оценок всех учеников класса
Реализована страница с таблицей оценок:
- Отображение оценок всех учеников по всем заданиям в виде таблицы
- Группировка по классам (ученики видят только оценки своего класса)
- Отображение прочерков для заданий, которые еще не сданы или не оценены

## Вывод

В ходе выполнения лабораторной работы была разработана система управления домашними заданиями на базе Django.
Реализованы все поставленные задачи: хранение информации о домашних заданиях, регистрация пользователей,
просмотр заданий, сдача заданий в текстовом виде, постановка оценок через Django-admin и формирование таблицы оценок.
Система позволяет эффективно управлять учебным процессом, обеспечивая удобный интерфейс для как учеников, так и преподавателей.

## Примеры кода

### 1. Модель Submission с логикой расчета штрафов

```python
class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_submissions')
    content = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(blank=True, null=True)
    teacher_comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
    
    def is_late(self):
        return self.submission_date.date() > self.homework.due_date
    
    def get_penalty(self):
        if not self.is_late():
            return 0
        
        days_late = (self.submission_date.date() - self.homework.due_date).days
        penalty = self.homework.penalties.filter(days_after_due__lte=days_late).order_by('-days_after_due').first()
        
        if penalty:
            if penalty.penalty_type == 'percentage':
                return self.homework.max_score * (penalty.penalty_value / 100)
            else:
                return penalty.penalty_value
        return 0
    
    def get_final_score(self):
        if self.score is None:
            return None
        penalty = self.get_penalty()
        final_score = self.score - penalty
        return max(0, final_score)  # Ensure score doesn't go below 0
```

### 2. Представление для сдачи домашнего задания

```python
@login_required
def submit_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)

    if request.user.profile.group != 'student':
        messages.error(request, 'Only students can submit homework.')
        return redirect('homework_detail', pk=pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()
            messages.success(request, 'Homework submitted successfully!')
            return redirect('homework_detail', pk=pk)
    else:
        form = SubmissionForm()

    return render(request, 'homeworks/submit_homework.html', {
        'form': form,
        'homework': homework
    })
```
