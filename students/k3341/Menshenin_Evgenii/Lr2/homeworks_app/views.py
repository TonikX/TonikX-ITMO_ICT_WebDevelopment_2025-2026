from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from accounts.models import Profile
from .forms import SubmissionForm
from .models import Homework, Submission, Subject


@login_required
def homework_list(request):
    subjects = Subject.objects.all()
    
    subject_id = request.GET.get('subject')
    
    if request.user.profile.group == 'teacher':
        homeworks = Homework.objects.filter(teacher=request.user)
    else:
        homeworks = Homework.objects.all()
    
    if subject_id:
        homeworks = homeworks.filter(subject_id=subject_id)
    
    paginator = Paginator(homeworks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'homeworks/homework_list.html', {
        'page_obj': page_obj,
        'subjects': subjects,
        'selected_subject': subject_id
    })


@login_required
def homework_detail(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    submissions = homework.submissions.filter(student=request.user)

    return render(request, 'homeworks/homework_detail.html', {
        'homework': homework,
        'submissions': submissions
    })


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

@login_required
def students_grades_table(request):
    homework_list_obj = Homework.objects.all()

    current_user = Profile.objects.get(user=request.user)
    if current_user.classroom is None:
        return redirect('homework_list')
    student_list = User.objects.filter(profile__group='student', profile__classroom=current_user.classroom).distinct()

    submissions = Submission.objects.all()
    return render(request, 'homeworks/students_grades.html', {
        'homework_list': homework_list_obj,
        'student_list': student_list,
        'submissions': submissions
    })