from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Assignment, Submission
from .forms import SubmissionForm, RegisterForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    return render(request, 'homework/index.html')

def assignment_list(request):
    q = request.GET.get('q', '').strip()
    assignments = Assignment.objects.select_related('subject', 'teacher').all()
    if q:
        assignments = assignments.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(subject__name__icontains=q) |
            Q(teacher__username__icontains=q)
        )

    paginator = Paginator(assignments, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'q': q}
    return render(request, 'homework/assignment_list.html', context)

def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    user_submission = None
    if request.user.is_authenticated:
        try:
            user_submission = Submission.objects.get(assignment=assignment, student=request.user)
        except Submission.DoesNotExist:
            user_submission = None
    return render(request, 'homework/assignment_detail.html', {'assignment': assignment, 'user_submission': user_submission})

@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    # проверка: если уже сдал, редирект на страницу задания
    submission, created = Submission.objects.get_or_create(assignment=assignment, student=request.user, defaults={'text': ''})
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.instance.student = request.user
            form.instance.assignment = assignment
            form.save()
            messages.success(request, 'Ваш ответ сохранён и передан на проверку.')
            return redirect('homework:assignment_detail', pk=assignment.pk)
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'homework/submission_form.html', {'form': form, 'assignment': assignment, 'created': created})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homework:home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def grades_table(request):
    students = User.objects.filter(is_staff=False).order_by('username')
    assignments = Assignment.objects.order_by('-date_issued')
    matrix = {}
    for student in students:
        row = {}
        for a in assignments:
            sub = Submission.objects.filter(assignment=a, student=student).first()
            row[a.pk] = sub.grade if sub and sub.grade is not None else None
        matrix[student.pk] = row
    context = {'students': students, 'assignments': assignments, 'matrix': matrix}
    return render(request, 'homework/grades_table.html', context)
