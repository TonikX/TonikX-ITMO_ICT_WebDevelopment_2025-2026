from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Homework, HomeworkSubmission, Grade, Subject, StudentProfile
from .forms import HomeworkSubmissionForm, UserRegistrationForm, HomeworkForm


def homepage(request):
    """Главная страница"""
    if request.user.is_authenticated:
        # Если пользователь авторизован, перенаправляем в профиль
        return redirect('homeworks:profile')
    return render(request, 'homeworks/home.html')


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Создаем профиль студента
            student_class = form.cleaned_data.get('student_class')
            StudentProfile.objects.create(user=user, student_class=student_class)

            # Автоматически логиним пользователя после регистрации
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('homeworks:profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'homeworks/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль пользователя с основной информацией"""
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        student_class = student_profile.student_class
    except StudentProfile.DoesNotExist:
        student_class = "Не указан"

    # Последние сданные задания
    recent_submissions = HomeworkSubmission.objects.filter(
        student=request.user
    ).select_related('homework', 'homework__subject')[:5]

    # Последние оценки
    recent_grades = Grade.objects.filter(
        submission__student=request.user
    ).select_related('submission', 'submission__homework')[:5]

    context = {
        'student_class': student_class,
        'recent_submissions': recent_submissions,
        'recent_grades': recent_grades,
    }
    return render(request, 'homeworks/profile.html', context)


@login_required
def homework_list(request):
    """Список всех домашних заданий"""
    homeworks = Homework.objects.all().select_related('subject', 'teacher')
    subjects = Subject.objects.all()

    # Фильтрация по предмету
    subject_id = request.GET.get('subject')
    if subject_id:
        homeworks = homeworks.filter(subject_id=subject_id)

    # Получаем submission текущего пользователя
    user_submissions = HomeworkSubmission.objects.filter(
        student=request.user
    ).select_related('homework')

    # Создаем два простых списка
    submitted_homework_ids = []  # ID заданий которые сданы
    submission_ids_dict = {}  # {homework_id: submission_id}

    for submission in user_submissions:
        submitted_homework_ids.append(submission.homework_id)
        submission_ids_dict[submission.homework_id] = submission.id

    context = {
        'homeworks': homeworks,
        'subjects': subjects,
        'submitted_homework_ids': submitted_homework_ids,  # для проверки статуса
        'submission_ids_dict': submission_ids_dict,  # для получения ID сдачи
    }
    return render(request, 'homeworks/homework_list.html', context)


@login_required
def homework_list_by_subject(request, subject_id):
    """Список заданий по конкретному предмету"""
    subject = get_object_or_404(Subject, id=subject_id)
    homeworks = Homework.objects.filter(subject=subject).select_related('teacher')

    submitted_homework_ids = HomeworkSubmission.objects.filter(
        student=request.user
    ).values_list('homework_id', flat=True)

    context = {
        'homeworks': homeworks,
        'subject': subject,
        'submitted_homework_ids': submitted_homework_ids,
    }
    return render(request, 'homeworks/homework_list_by_subject.html', context)


@login_required
def homework_detail(request, homework_id):
    """Детальная информация о домашнем задании"""
    homework = get_object_or_404(Homework, id=homework_id)

    # Проверяем, сдал ли уже пользователь это задание
    try:
        submission = HomeworkSubmission.objects.get(
            homework=homework,
            student=request.user
        )
        user_has_submitted = True
    except HomeworkSubmission.DoesNotExist:
        submission = None
        user_has_submitted = False

    context = {
        'homework': homework,
        'submission': submission,
        'user_has_submitted': user_has_submitted,
    }
    return render(request, 'homeworks/homework_detail.html', context)


@login_required
def submit_homework(request, homework_id):
    """Сдача домашнего задания"""
    homework = get_object_or_404(Homework, id=homework_id)

    # Проверяем, не сдал ли уже пользователь это задание
    if HomeworkSubmission.objects.filter(homework=homework, student=request.user).exists():
        messages.warning(request, 'Вы уже сдали это задание!')
        return redirect('homeworks:homework_detail', homework_id=homework_id)

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()

            messages.success(request, 'Задание успешно сдано!')
            return redirect('homeworks:submission_detail', submission_id=submission.id)
    else:
        form = HomeworkSubmissionForm()

    context = {
        'form': form,
        'homework': homework,
    }
    return render(request, 'homeworks/submit_homework.html', context)


@login_required
def submission_detail(request, submission_id):
    """Просмотр сданного задания"""
    submission = get_object_or_404(
        HomeworkSubmission,
        id=submission_id,
        student=request.user  # Только владелец может просматривать
    )

    # Пытаемся получить оценку, если есть
    try:
        grade = Grade.objects.get(submission=submission)
    except Grade.DoesNotExist:
        grade = None

    context = {
        'submission': submission,
        'grade': grade,
    }
    return render(request, 'homeworks/submission_detail.html', context)


@login_required
def edit_submission(request, submission_id):
    """Редактирование сданного задания"""
    submission = get_object_or_404(
        HomeworkSubmission,
        id=submission_id,
        student=request.user
    )

    # Проверяем, не оценено ли уже задание (если оценено - запрещаем редактирование)
    if hasattr(submission, 'grade'):
        messages.error(request, 'Нельзя редактировать задание, которое уже оценено!')
        return redirect('homeworks:submission_detail', submission_id=submission_id)

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задание успешно обновлено!')
            return redirect('homeworks:submission_detail', submission_id=submission_id)
    else:
        form = HomeworkSubmissionForm(instance=submission)

    context = {
        'form': form,
        'submission': submission,
    }
    return render(request, 'homeworks/edit_submission.html', context)


@login_required
def grade_list(request):
    """Список оценок текущего пользователя с пагинацией"""
    grades_list = Grade.objects.filter(
        submission__student=request.user
    ).select_related(
        'submission',
        'submission__homework',
        'submission__homework__subject'
    ).order_by('-graded_date')

    # Вычисляем средний балл
    graded_grades = [grade.grade for grade in grades_list if grade.grade is not None]
    if graded_grades:
        average_grade = sum(graded_grades) / len(graded_grades)
        average_grade = round(average_grade, 1)
    else:
        average_grade = None

    paginator = Paginator(grades_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'grades': page_obj,  # для обратной совместимости
        'average_grade': average_grade,
        'total_grades': len(graded_grades),
    }
    return render(request, 'homeworks/grade_list.html', context)


@login_required
def class_grades_table(request):
    """Таблица оценок всех учеников класса"""
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        student_class = student_profile.student_class

        # Получаем всех студентов того же класса
        classmates = StudentProfile.objects.filter(
            student_class=student_class
        ).select_related('user')

        # Получаем все задания
        homeworks = Homework.objects.all().select_related('subject')

        # Собираем данные для таблицы
        grades_data = []
        for classmate in classmates:
            student_grades = []
            for homework in homeworks:
                try:
                    submission = HomeworkSubmission.objects.get(
                        homework=homework,
                        student=classmate.user
                    )
                    grade = Grade.objects.get(submission=submission)
                    student_grades.append(grade.grade)
                except (HomeworkSubmission.DoesNotExist, Grade.DoesNotExist):
                    student_grades.append('-')

            grades_data.append({
                'student': classmate.user,
                'grades': student_grades,
            })

        context = {
            'student_class': student_class,
            'homeworks': homeworks,
            'grades_data': grades_data,
        }

    except StudentProfile.DoesNotExist:
        messages.error(request, 'Профиль студента не найден!')
        return redirect('homeworks:profile')

    return render(request, 'homeworks/class_grades_table.html', context)


@staff_member_required
def create_homework(request):
    """Создание нового домашнего задания (только для staff)"""
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.teacher = request.user
            homework.save()
            messages.success(request, 'Задание успешно создано!')
            return redirect('homeworks:homework_list')
    else:
        form = HomeworkForm()

    context = {
        'form': form,
    }
    return render(request, 'homeworks/create_homework.html', context)