from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, SubmissionForm
from .models import Homework, Submission

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homework_list")
    else:
        form = RegisterForm()
    return render(request, "board/register.html", {"form": form})

def is_teacher(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def homework_list(request):
    homeworks = Homework.objects.order_by("-issued_date", "due_date")
    my_submissions = {}
    if request.user.is_authenticated:
        subs = Submission.objects.filter(student=request.user)
        my_submissions = {s.homework_id: s for s in subs}
    return render(request, "board/homework_list.html", {"homeworks": homeworks, "my_submissions": my_submissions})

def homework_detail(request, homework_id):
    hw = get_object_or_404(Homework, id=homework_id)
    my_submission = None
    if request.user.is_authenticated:
        my_submission = Submission.objects.filter(student=request.user, homework=hw).first()
    return render(request, "board/homework_detail.html", {"hw": hw, "my_submission": my_submission})

@login_required
def submit_homework(request, homework_id):
    hw = get_object_or_404(Homework, id=homework_id)
    submission = Submission.objects.filter(student=request.user, homework=hw).first()

    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.student = request.user
            sub.homework = hw
            sub.save()
            return redirect("homework_detail", homework_id=hw.id)
    else:
        form = SubmissionForm(instance=submission)

    return render(request, "board/submit_homework.html", {"hw": hw, "form": form, "submission": submission})

@user_passes_test(is_teacher)
def class_grades_table(request):
    homeworks = Homework.objects.order_by("issued_date", "id")
    students = User.objects.filter(is_staff=False, is_superuser=False).order_by("username")
    submissions = Submission.objects.select_related("student", "homework").all()

    grade_map = {}
    for s in submissions:
        grade_map[f"{s.student_id}:{s.homework_id}"] = s.grade

    return render(
        request,
        "board/class_grades_table.html",
        {"homeworks": homeworks, "students": students, "grade_map": grade_map},
    )

@login_required
def my_grades(request):
    homeworks = Homework.objects.order_by("issued_date", "id")
    subs = Submission.objects.filter(student=request.user).select_related("homework")

    my_grade_map = {s.homework_id: s.grade for s in subs}
    return render(
        request,
        "board/my_grades.html",
        {"homeworks": homeworks, "my_grade_map": my_grade_map},
    )
