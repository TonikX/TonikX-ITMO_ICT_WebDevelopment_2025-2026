from .forms import UserRegisterForm
from .models import User, StudentProfile, Subject, Homework, HomeworkSubmission, Grade
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, timedelta


def pageNotFound(request, exception):
    return render(request, 'not_found.html')


def index(request):
    return render(request, 'index.html')


def base(request):
    return render(request, 'main.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def teacher_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == User.TEACHER,
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required
def dashboard(request):
    if request.user.role == User.STUDENT:
        if hasattr(request.user, 'student_profile'):
            return redirect('grade_table')
        else:
            messages.error(request, "Профиль ученика не найден")
            return redirect('login')

    elif request.user.role == User.TEACHER:
        if hasattr(request.user, 'teacher_profile'):
            return redirect('teacher_page')
        else:
            messages.error(request, "Профиль преподавателя не найден")
            return redirect('login')


@teacher_required
def teacher_page(request):
    try:
        teacher_profile = request.user.teacher_profile
    except:
        messages.error(request, "Профиль преподавателя не найден")
        return redirect('login')

    context = {'teacher_profile': teacher_profile,}
    return render(request, 'teacher_page.html', context)


@login_required
def student_dashboard(request):
    if request.user.role != User.STUDENT:
        return redirect('login')

    return redirect('grade_table')  # Редирект сразу на таблицу оценок


@login_required
def grade_table(request):
    if request.user.role != 'student':
        messages.error(request, "Эта страница доступна только ученикам")
        return redirect('login')

    try:
        student_profile = request.user.student_profile
    except:
        messages.error(request, "Профиль ученика не найден")
        return redirect('login')

    class_name = student_profile.class_name
    classmates = StudentProfile.objects.filter(class_name=class_name).select_related('user')
    subjects = Subject.objects.filter(homework__for_class=class_name).distinct()
    subject_filter = request.GET.get('subject')
    if subject_filter:
        filtered_subjects = [subject_filter]
    else:
        filtered_subjects = [s.name for s in subjects]

    all_grades = Grade.objects.filter(submission__student__class_name=class_name).select_related(
                                      'submission__student__user', 'submission__homework__subject')

    student_subject_grades = []
    student_subject_avg = []
    student_total_avg = {}
    for grade in all_grades:
        student_id = grade.submission.student.id
        subject_name = grade.submission.homework.subject.name
        grade_value = grade.grade
        student_subject_grades.append({
            'student_id': student_id,
            'subject': subject_name,
            'grade': grade_value
        })

    for classmate in classmates:
        student_id = classmate.id
        student_grades = [g for g in student_subject_grades if g['student_id'] == student_id]
        if student_grades:
            grades_by_subject = {}
            for grade_data in student_grades:
                subject = grade_data['subject']
                if subject not in grades_by_subject:
                    grades_by_subject[subject] = []
                grades_by_subject[subject].append(grade_data['grade'])

            all_student_grades = []
            for subject, grades in grades_by_subject.items():
                avg = sum(grades) / len(grades)
                student_subject_avg.append({
                    'student_id': student_id,
                    'subject': subject,
                    'average': round(avg, 1),
                    'count': len(grades),
                    'grades': grades
                })
                all_student_grades.extend(grades)

            if all_student_grades:
                total_avg = sum(all_student_grades) / len(all_student_grades)
                student_total_avg[student_id] = round(total_avg, 1)

    user_average_grade = student_total_avg.get(student_profile.id)

    context = {
        'class_name': class_name,
        'classmates': classmates,
        'subjects': subjects,
        'filtered_subjects': filtered_subjects,
        'student_subject_grades': student_subject_grades,
        'student_subject_avg': student_subject_avg,
        'student_total_avg': student_total_avg,
        'current_user_profile': student_profile,
        'user_average_grade': user_average_grade,
        'selected_subject': subject_filter,
    }

    return render(request, 'table.html', context)


@login_required
def active_homeworks(request):
    if request.user.role != User.STUDENT:
        return redirect('login')

    student_profile = request.user.student_profile
    today = date.today()
    homeworks = Homework.objects.filter(
        for_class=student_profile.class_name,
        due_date__gte=today,
        is_active=True
    ).select_related('subject', 'teacher__user').order_by('due_date')

    selected_subject = request.GET.get('subject')
    if selected_subject:
        homeworks = homeworks.filter(subject_id=selected_subject)

    selected_status = request.GET.get('status')
    submitted_homework_ids = HomeworkSubmission.objects.filter(student=student_profile).values_list('homework_id', flat=True)
    if selected_status == 'submitted':
        homeworks = homeworks.filter(id__in=submitted_homework_ids)
    elif selected_status == 'not_submitted':
        homeworks = homeworks.exclude(id__in=submitted_homework_ids)
    elif selected_status == 'urgent':
        homeworks = homeworks.filter(due_date__lte=today + timedelta(days=2))

    subjects = Subject.objects.filter(homework__for_class=student_profile.class_name).distinct()
    paginator = Paginator(homeworks, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    for hw in page_obj:
        hw.is_submitted = hw.id in submitted_homework_ids
        hw.days_left = (hw.due_date - today).days

    context = {
        'page_obj': page_obj,
        'student_profile': student_profile,
        'today': today,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'selected_status': selected_status,
    }

    return render(request, 'active_homeworks.html', context)


@login_required
def submit_homework(request, homework_id):
    try:
        homework = Homework.objects.get(id=homework_id)
    except Homework.DoesNotExist:
        return redirect('page_not_found_url')

    student_profile = request.user.student_profile

    if homework.for_class != student_profile.class_name:
        messages.error(request, "Это задание не для вашего класса")
        return redirect('active_homeworks')

    if request.method == 'POST':
        submission_text = request.POST.get('submission_text')

        if len(submission_text) < 1:
            messages.error(request, "Решение не должно быть пустым")
            return render(request, 'submit_homework.html', {
                'homework': homework,
                'student_profile': student_profile,
            })

        existing_submission = HomeworkSubmission.objects.filter(
            homework=homework,
            student=student_profile
        ).first()

        if existing_submission:
            existing_submission.submission_text = submission_text
            existing_submission.save()
            messages.success(request, "Задание обновлено!")
        else:
            submission = HomeworkSubmission.objects.create(
                homework=homework,
                student=student_profile,
                submission_text=submission_text,
            )
            messages.success(request, "Задание сдано успешно!")

        return redirect('active_homeworks')

    context = {
        'homework': homework,
        'student_profile': student_profile,
    }

    return render(request, 'submit_homework.html', context)


@login_required
def student_profile_view(request):
    if request.user.role != User.STUDENT:
        return redirect('login')

    student_profile = request.user.student_profile
    total_submitted = HomeworkSubmission.objects.filter(student=student_profile).count()
    total_graded = Grade.objects.filter(submission__student=student_profile).count()
    avg_grade = Grade.objects.filter(
        submission__student=student_profile
    ).aggregate(avg=Avg('grade'))['avg']

    context = {
        'student_profile': student_profile,
        'total_submitted': total_submitted,
        'total_graded': total_graded,
        'avg_grade': avg_grade,
    }

    return render(request, 'student_profile.html', context)