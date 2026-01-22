# views/student_views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Student, Homework, HomeworkSubmission, Subject


@login_required
def student_profile(request):
    """Student's profile page"""
    if request.user.role != "student":
        return redirect('login')

    try:
        student = request.user.student
        has_profile = True
        subjects = student.get_all_subjects()

        subjects_with_stats = []

        for subject in subjects:
            subjects_with_stats.append({
                'subject': subject,
                'total': subject.get_homeworks_for_class(student.school_class).count(),
                'active': subject.get_active_homeworks().count(),
                'burning': student.get_burning_homeworks().filter(subject=subject).count(),
                'overdue': student.get_overdue_homeworks().filter(subject=subject).count(),
            })
    except Student.DoesNotExist:
        student = None
        has_profile = False
        subjects = []
        subjects_with_stats = []

    context = {
        'user': request.user,
        'subjects': subjects,
        'has_profile': has_profile,
        'student': student,
        'subjects_with_stats': subjects_with_stats,
    }
    return render(request, 'board/student_profile.html', context)


@login_required
def student_records(request):
    """Student's records page"""
    if request.user.role != "student":
        return redirect('login')
    try:
        student = request.user.student
        has_profile = True

        subjects_with_records = []

        for subject in student.get_all_subjects():
            records = student.get_subject_records(subject)
            subject_gpa = student.get_subject_gpa_with_zeros(subject)

            subjects_with_records.append({
                'subject': subject,
                'records': records,
                'gpa': subject_gpa,
                'homeworks_count': len(records),
                'submitted_count': sum(1 for grade in records.values() if grade > 0),
            })

        context = {
            'user': request.user,
            'has_profile': has_profile,
            'student': student,
            'subjects_with_records': subjects_with_records,
        }

    except Student.DoesNotExist:
        context = {
            'user': request.user,
            'has_profile': False,
            'student': None,
            'subjects_with_records': [],
        }
    return render(request, 'board/student_record.html', context)

@login_required
def student_subject(request, subject_id):
    """Student's subject page"""
    if request.user.role != "student":
        return redirect('login')
    try:
        student = request.user.student
        has_profile = True
        subject = get_object_or_404(Subject, id=subject_id)
        records = student.get_subject_records(subject)
        gpa = student.get_subject_gpa_with_zeros(subject)
        submitted = sum(1 for grade in records.values() if grade > 0)


        context = {
            'user': request.user,
            'has_profile': has_profile,
            'student': student,
            'subject': subject,
            'records': records,
            'gpa': gpa,
            'submitted': submitted,
        }

    except Student.DoesNotExist:
        context = {
            'user': request.user,
            'has_profile': False,
            'student': None,
            'subject': None,
            'records': [],
            'gpa': 0,
            'submitted': 0,
        }

    return render(request, 'board/student_subject.html', context)



@login_required
def student_homeworks(request, homework_id):
    """Homework details + edit modal"""
    if request.user.role != "student":
        return redirect('login')

    try:
        student = request.user.student
        has_profile = True
        homework = get_object_or_404(Homework,id=homework_id)
        if student.get_homework_status(homework) == 'submitted' or student.get_homework_status(homework) == 'graded':
            submission = student.submissions.get(homework=homework)
        else:
            submission = Homework.objects.none()
    except Student.DoesNotExist:
        homework = None
        submission = None
        has_profile = False
        student = None

    if request.method == 'POST':
        submitted_text = request.POST.get('submitted_text', '').strip()

        if not submitted_text:
            messages.error(request, "Text cannot be empty.")
        else:
            if submission:
                submission.reset_grade_on_edit()
                submission.submitted_text = submitted_text
                submission.save()
                messages.success(request, "Homework updated successfully.")
            else:
                HomeworkSubmission.objects.create(
                    homework=homework,
                    student=student,
                    submitted_text=submitted_text
                )
                messages.success(request, "Homework submitted successfully.")

        return redirect('student_homeworks', homework_id=homework.id)

    context = {
        'has_profile': has_profile,
        'user': request.user,
        'student': student,
        'homework': homework,
        'homework_submission': submission,
    }
    return render(request, 'board/student_homeworks.html', context)


