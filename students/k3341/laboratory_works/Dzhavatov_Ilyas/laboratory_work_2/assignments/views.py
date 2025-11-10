from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Assignment, Submission, Subject
from .forms import CustomUserCreationForm, SubmissionForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('assignment_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def assignment_list(request):
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')

    assignments = Assignment.objects.all().select_related('subject', 'teacher').order_by('-assigned_date')

    if search_query:
        assignments = assignments.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )

    if subject_filter:
        assignments = assignments.filter(subject_id=subject_filter)

    paginator = Paginator(assignments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    subjects = Subject.objects.all()

    context = {
        'page_obj': page_obj,
        'subjects': subjects,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'today': timezone.now().date(),
    }
    return render(request, 'assignments/assignment_list.html', context)


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submission = None

    if not request.user.is_staff:
        submission, created = Submission.objects.get_or_create(
            assignment=assignment,
            student=request.user,
            defaults={'submission_text': ''}
        )

    if request.method == 'POST' and submission:
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', pk=pk)
    else:
        if submission:
            form = SubmissionForm(instance=submission)
        else:
            form = None

    if request.user.is_staff:
        submissions = Submission.objects.filter(assignment=assignment).select_related('student')
    else:
        submissions = None

    context = {
        'assignment': assignment,
        'form': form,
        'submission': submission,
        'submissions': submissions,
        'today': timezone.now().date(),
    }
    return render(request, 'assignments/assignment_detail.html', context)


@login_required
def grades_table(request):
    from django.contrib.auth.models import User
    submissions = Submission.objects.filter(grade__gt=0).select_related('student', 'assignment')
    students = User.objects.filter(is_staff=False)
    assignments = Assignment.objects.all()

    context = {
        'students': students,
        'assignments': assignments,
        'submissions': submissions,
    }
    return render(request, 'assignments/grades_table.html', context)