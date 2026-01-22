# views/teacher_views.py
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Teacher, Homework, HomeworkSubmission, Subject, SchoolClass
from django.utils import timezone
from django.db.models import F, Avg
from django.core.paginator import Paginator


def get_group_metrics(teacher, group):
    critical_hws = Homework.objects.filter(
        subject__in=teacher.subjects.all(),
        school_class=group,
        due_date__lte=timezone.now().date() + timedelta(days=3),
    ).count()

    total_submissions = HomeworkSubmission.objects.filter(
        homework__school_class=group,
        homework__subject__in=teacher.subjects.all(),
    ).count()

    overdue_submissions = HomeworkSubmission.objects.filter(
        homework__school_class=group,
        homework__subject__in=teacher.subjects.all(),
        date_submitted__gt=F('homework__due_date'),
    ).count()

    overdue_percent = (overdue_submissions / total_submissions) * 100 if total_submissions > 0 else 0

    ungraded = teacher.get_ungraded_submissions().filter(
        homework__school_class=group, ).count()

    avg_grade = HomeworkSubmission.objects.filter(
        homework__school_class=group,
        homework__subject__in=teacher.subjects.all(),
        grade__isnull=False,
    ).aggregate(Avg('grade'))['grade__avg'] or 0

    # higher performance_score - more problems school_class has and needs more attention
    performance_score = (critical_hws * 2) + (overdue_percent * 0.5) + (ungraded * 0.3) + ((5 - avg_grade) * 10)

    if performance_score > 20:
        performance_level = 'High'
    elif performance_score > 10:
        performance_level = 'Medium'
    else:
        performance_level = 'Low'

    return {
        'class': group,
        'students': group.students.count(),
        'critical_hws': critical_hws,
        'overdue_percent': overdue_percent,
        'ungraded': ungraded,
        'avg_grade': avg_grade,
        'performance_level': performance_level,
    }


def get_subject_metrics(teacher, subject):
    groups = subject.get_classes_with_subject()
    groups_with_data = []
    for group in groups:
        groups_with_data.append(get_group_metrics(teacher, group))
    students = [student for group in groups for student in group.get_all_students()]
    homeworks = subject.homeworks.all()
    submitted_homeworks = [homework.submissions for homework in homeworks]
    ungraded_homeworks = [homework.get_ungraded_submissions() for homework in homeworks]
    if len(homeworks) == 0 or len(submitted_homeworks) == 0:
        rate = None
    else:
        rate = len(submitted_homeworks) / len(homeworks) * 100
    return {
        'groups': groups,
        'groups_with_data': groups_with_data,
        'students': students,
        'subject': subject,
        'homeworks': homeworks,
        'submitted_homeworks': submitted_homeworks,
        'ungraded_homeworks': ungraded_homeworks,
        'rate': rate,
    }


@login_required
def teacher_profile(request):
    """Teacher's profile page"""
    if request.user.role != "teacher":
        return redirect('login')
    try:
        teacher = request.user.teacher
        has_profile = True
        subject_data = []
        today_submissions = HomeworkSubmission.objects.filter(
            homework__subject__in=teacher.subjects.all(),
            last_edited__date=timezone.now().date(),
        )
        today_submissions_data = []
        groups_with_data = []
        for submission in today_submissions:
            today_submissions_data.append({
                'submission': submission,
                'submission_status': submission.student.get_homework_status(submission.homework),
            })

        today_submissions_exist = True if len(today_submissions_data) > 0 else False
        for group in teacher.get_teaching_classes():
            groups_with_data.append(get_group_metrics(teacher, group))
        for subject in teacher.subjects.all():
            subject_metrics = get_subject_metrics(teacher, subject)
            subject_data.append({
                'subject': subject,
                'groups': subject_metrics['groups'],
                'students': subject_metrics['students'],
                'homeworks': subject_metrics['homeworks'],
                'submitted_homeworks': subject_metrics['submitted_homeworks'],
                'ungraded_homeworks': subject_metrics['ungraded_homeworks'],
                'rate': subject_metrics['rate'],
            })
    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        subject_data = []
        today_submissions_data = []
        groups_with_data = []
        today_submissions_exist = False

    context = {
        'user': request.user,
        'has_profile': has_profile,
        'teacher': teacher,
        'groups_with_data': groups_with_data,
        'subject_data': subject_data,
        'today_submissions_data': today_submissions_data,
        'today_submissions_exist': today_submissions_exist,
    }
    return render(request, 'board/teacher_profile.html', context)


@login_required
def teacher_records(request):
    """Teacher records page"""
    if request.user.role != "teacher":
        return redirect('login')

    try:
        teacher = request.user.teacher
        has_profile = True
        subjects = teacher.get_taught_subjects()
        subjects_with_filters = []
        for subject in subjects:
            subjects_with_filters.append(get_subject_metrics(teacher, subject))
    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        subjects = []
        subjects_with_filters = []

    context = {
        'user': request.user,
        'teacher': teacher,
        'has_profile': has_profile,
        'subjects': subjects,
        'subjects_with_filters': subjects_with_filters,

    }

    return render(request, 'board/teacher_record.html', context)


@login_required
def teacher_subject(request, subject_id):
    """Teacher's subjects page"""
    if request.user.role != "teacher":
        return redirect('login')

    try:
        teacher = request.user.teacher
        has_profile = True
        subject = get_object_or_404(Subject, id=subject_id)
        groups = subject.get_classes_with_subject()
        subject_data = get_subject_metrics(teacher, subject)
    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        subject = None
        groups = []
        subject_data = None

    context = {
        'user': request.user,
        'teacher': teacher,
        'has_profile': has_profile,
        'subject': subject,
        'groups': groups,
        'subject_data': subject_data,
    }
    return render(request, 'board/teacher_subject.html', context)


def get_all_submissions(teacher):
    assignment_data = []
    homeworks = teacher.get_assigned_homeworks()
    for homework in homeworks:
        for submission in homework.submissions.all():
            assignment_data.append({
                'submission': submission,
                'submission_status': submission.student.get_homework_status(submission.homework),
                'homework': homework,
                'student': submission.student,
                'group': homework.school_class,
                'date_assigned': homework.date_assigned,
            })

    return assignment_data


@login_required
def teacher_assignments(request):
    """All assignments page"""
    if request.user.role != "teacher":
        return redirect('login')

    try:
        teacher = request.user.teacher
        has_profile = True
        assignments = get_all_submissions(teacher)

        # pagination
        paginator = Paginator(assignments, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Apply filters from GET parameters
        subject_filter = request.GET.get('subject', '')
        status_filter = request.GET.get('status', '')
        date_filter = request.GET.get('date', '')
        sort_by = request.GET.get('sort', '')

        # Subject filter
        if subject_filter:
            assignments = [a for a in assignments if a['homework'].subject.name == subject_filter]

        # Status filter
        if status_filter:
            assignments = [a for a in assignments if a['submission_status'] == status_filter]

        # Date filter
        if date_filter:
            today = timezone.now().date()
            if date_filter == 'today':
                assignments = [a for a in assignments if a['submission'].last_edited.date() == today]
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                assignments = [a for a in assignments if a['submission'].last_edited.date() >= week_ago]
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                assignments = [a for a in assignments if a['submission'].last_edited.date() >= month_ago]
            elif date_filter == 'overdue':
                assignments = [a for a in assignments if a['homework'].due_date < today]

        # Sorting
        if sort_by == 'subject':
            assignments.sort(key=lambda x: x['homework'].subject.name)
        elif sort_by == 'last_edited':
            assignments.sort(key=lambda x: x['submission'].last_edited, reverse=True)
        elif sort_by == 'due_date':
            assignments.sort(key=lambda x: x['homework'].due_date)

    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        assignments = []

    context = {
        'user': request.user,
        'teacher': teacher,
        'has_profile': has_profile,
        'assignments': assignments,
        'assignments': page_obj,  # obj instead of assignments
        'page_obj': page_obj,  # for pagination pattern
    }
    return render(request, 'board/teacher_assignments.html', context)


@login_required
def teacher_assignment_detail(request, submission_id):
    """Teacher's assignment detail page with grading functionality"""
    if request.user.role != "teacher":
        return redirect('login')

    try:
        teacher = request.user.teacher
        has_profile = True
        submission = get_object_or_404(HomeworkSubmission, id=submission_id)

        # Check if teacher can grade this submission
        if not submission.can_be_graded_by(teacher):
            messages.error(request, "You don't have permission to grade this submission.")
            return redirect('teacher_assignments')

        homework = submission.homework
        student = submission.student

        if request.method == 'POST':
            grade = request.POST.get('grade')
            feedback = request.POST.get('feedback', '').strip()

            if not grade:
                messages.error(request, "Please select a grade.")
            else:
                try:
                    grade_int = int(grade)
                    if grade_int not in [2, 3, 4, 5]:
                        messages.error(request, "Please select a valid grade.")
                    else:
                        submission.mark_as_graded(grade_int, feedback)
                        messages.success(request, "Assignment graded successfully!")
                        return redirect('teacher_assignment_detail', submission_id=submission.id)
                except ValueError:
                    messages.error(request, "Invalid grade format.")

    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        submission = None
        homework = None
        student = None

    context = {
        'user': request.user,
        'teacher': teacher,
        'has_profile': has_profile,
        'submission': submission,
        'homework': homework,
        'student': student,
    }
    return render(request, 'board/teacher_assignment_detail.html', context)


@login_required
def teacher_school_class(request, school_class_id, subject_id):
    """Teacher's school class page with grading functionality"""
    if request.user.role != "teacher":
        return redirect('login')
    try:
        teacher = request.user.teacher
        has_profile = True
        subject = get_object_or_404(Subject, id=subject_id)
        school_class = get_object_or_404(SchoolClass, id=school_class_id)
        students = school_class.get_all_students()
        students_with_data = []

        # Получаем все домашние задания один раз для оптимизации
        homeworks = Homework.objects.filter(subject=subject, school_class=school_class)

        for student in students:
            homework_data = []

            for homework in homeworks:
                submission = student.get_homework_submission(homework)

                homework_data.append({
                    'homework': homework,
                    'submission': submission,  # Теперь сабмишн доступен в шаблоне
                    'assignment': True if submission else False,
                    'status': student.get_homework_status(homework),
                })

            students_with_data.append({
                'student': student,
                'gpa': student.get_average_grade(subject),
                'homework_data': homework_data,
                'records': student.get_subject_records(subject),
                'submitted': student.get_submitted_homeworks().filter(homework__subject=subject).count(),
            })
    except Teacher.DoesNotExist:
        teacher = None
        has_profile = False
        school_class = None
        students = []
        subject = None
        students_with_data = []

    context = {
        'user': request.user,
        'teacher': teacher,
        'has_profile': has_profile,
        'school_class': school_class,
        'students': students,
        'subject': subject,
        'students_with_data': students_with_data,
    }
    return render(request, 'board/teacher_school_class.html', context)
