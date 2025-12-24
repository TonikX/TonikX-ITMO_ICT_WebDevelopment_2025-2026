from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, HomeworkSubmissionForm
from .models import Homework, Submission, Student


def register(request):
    """Регистрация нового студента (функциональное представление)"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('assignment_list')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def assignment_list(request):
        assignments = Homework.objects.select_related('subject', 'teacher').all()
    
        # Если студент вошёл — добавим флаг is_submitted
        if request.user.is_authenticated and hasattr(request.user, 'student'):
            student = request.user.student
            # Получаем ID заданий, которые студент уже сдал
            submitted_hw_ids = Submission.objects.filter(student=student).values_list('homework_id', flat=True)
            # Добавляем атрибут is_submitted к каждому заданию
            for hw in assignments:
                hw.is_submitted = hw.id in submitted_hw_ids
        else:
            for hw in assignments:
                hw.is_submitted = False

        return render(request, 'homework/assignment_list.html', {
            'assignments': assignments,
            'is_student': request.user.is_authenticated and hasattr(request.user, 'student')
        })


def assignment_detail(request, pk):
    assignment = get_object_or_404(Homework, pk=pk)
    
    # Добавляем флаг: сдано ли это задание текущим студентом
    is_submitted = False
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        is_submitted = Submission.objects.filter(
            homework=assignment,
            student=request.user.student
        ).exists()

    return render(request, 'homework/assignment_detail.html', {
        'assignment': assignment,
        'is_submitted': is_submitted,
        'is_student': request.user.is_authenticated and hasattr(request.user, 'student')
    })


@login_required
def submit_homework(request, homework_id=None):
    """
    Сдача домашнего задания.
    Если homework_id=None — показываем список доступных заданий.
    """
    # Проверка: студент ли?
    if not hasattr(request.user, 'student'):
        messages.error(request, "Только студенты могут сдавать задания.")
        return redirect('assignment_list')

    student = request.user.student

    # Режим выбора задания
    if homework_id is None:
        # Берём задания, которые студент ещё не сдал
        available = Homework.objects.exclude(
            submission__student=student
        ).order_by('due_date')
        return render(request, 'homework/assignment_list.html', {
            'assignments': available,
            'submit_mode': True  # флаг для шаблона: показать кнопки "Сдать"
        })

    # Режим сдачи конкретного задания
    homework = get_object_or_404(Homework, pk=homework_id)

    # Уже сдано?
    if Submission.objects.filter(homework=homework, student=student).exists():
        messages.warning(request, "Вы уже сдали это задание.")
        return redirect('grades_table')

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = student
            submission.save()
            messages.success(request, f"Задание «{homework.title}» сдано!")
            return redirect('grades_table')
    else:
        form = HomeworkSubmissionForm()

    return render(request, 'homework/submit_homework.html', {
        'form': form,
        'homework': homework
    })


@login_required
def grades_table(request):
    """Таблица оценок студента (его собственных)"""
    if not hasattr(request.user, 'student'):
        messages.error(request, "Страница доступна только студентам.")
        return redirect('assignment_list')

    submissions = Submission.objects.filter(
        student=request.user.student
    ).select_related('homework__subject').order_by('-submitted_at')

    return render(request, 'homework/grades_table.html', {'submissions': submissions})