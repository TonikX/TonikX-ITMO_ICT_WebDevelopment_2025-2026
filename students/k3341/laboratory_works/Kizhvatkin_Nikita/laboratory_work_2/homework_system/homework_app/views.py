from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Case, When, Value, BooleanField
from django.utils import timezone
from .models import Homework, HomeworkSubmission, User
from .forms import UserRegisterForm, HomeworkSubmissionForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homework_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homework_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def homework_list(request):
    homeworks = Homework.objects.all().order_by('-due_date')
    today = timezone.now().date()
    if not request.user.is_staff:
        submitted_ids = HomeworkSubmission.objects.filter(
            student=request.user
        ).values_list('homework_id', flat=True)
        for homework in homeworks:
            homework.is_submitted = homework.id in submitted_ids
            homework.is_overdue = homework.due_date < today
    context = {
        'homeworks': homeworks,
        'is_teacher': request.user.is_staff,
        'today': today,
    }
    return render(request, 'homework_list.html', context)


@login_required
def submit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    submission, created = HomeworkSubmission.objects.get_or_create(
        homework=homework,
        student=request.user,
        defaults={'submission_text': ''}
    )
    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('homework_list')
    else:
        form = HomeworkSubmissionForm(instance=submission)
    context = {
        'form': form,
        'homework': homework,
        'submission': submission,
    }
    return render(request, 'submit_homework.html', context)


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Avg, Count
from django.contrib import messages

@login_required
def grades_table(request):
    students = User.objects.filter(is_staff=False).order_by('last_name', 'first_name')
    homeworks = Homework.objects.all().order_by('subject', 'due_date')
    grades_data = []
    for student in students:
        student_grades = []
        for homework in homeworks:
            try:
                submission = HomeworkSubmission.objects.get(
                    homework=homework,
                    student=student
                )
                grade = submission.grade if submission.grade else 'Не оценено'
                status = 'Сдано' if submission.submission_text else 'Не сдано'
                submission_exists = True
            except HomeworkSubmission.DoesNotExist:
                grade = 'Не сдано'
                status = 'Не сдано'
                submission = None
                submission_exists = False
            
            student_grades.append({
                'grade': grade,
                'status': status,
                'submission_id': submission.id if submission_exists else None,
                'homework_id': homework.id,
                'has_submission': submission_exists,
            })
        student_submissions = HomeworkSubmission.objects.filter(student=student)
        graded_submissions = student_submissions.exclude(grade__isnull=True)
        if graded_submissions.exists():
            average_grade = graded_submissions.aggregate(Avg('grade'))['grade__avg']
            average_grade = round(average_grade, 2)
        else:
            average_grade = 'Нет оценок'
        grades_data.append({
            'student': student,
            'grades': student_grades,
            'average_grade': average_grade,
            'total_submitted': student_submissions.count(),
            'total_graded': graded_submissions.count(),
        })
    context = {
        'students': students,
        'homeworks': homeworks,
        'grades_data': grades_data,
        'is_teacher': request.user.is_staff,
    }
    return render(request, 'grades_table.html', context)


@login_required
def view_submission(request, submission_id):
    submission = get_object_or_404(HomeworkSubmission, id=submission_id)
    if not request.user.is_staff and submission.student != request.user:
        messages.error(request, "У вас нет прав для просмотра этой работы")
        return redirect('grades_table')
    context = {
        'submission': submission,
        'is_teacher': request.user.is_staff,
    }
    return render(request, 'view_submission.html', context)
