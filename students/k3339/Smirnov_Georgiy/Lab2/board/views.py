from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Homework, Submission

User = get_user_model()


def homework_list(request):
    homeworks = Homework.objects.select_related('subject').all()
    return render(request, 'board/homework_list.html', {'homeworks': homeworks})


def homework_detail(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    submissions = homework.submissions.select_related('student').all()
    return render(request, 'board/homework_detail.html', {
        'homework': homework,
        'submissions': submissions,
    })


@login_required
def submit_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)

    if request.method == 'POST':
        answer_text = request.POST.get('answer_text', '').strip()
        if answer_text:
            Submission.objects.update_or_create(
                homework=homework,
                student=request.user,
                defaults={'answer_text': answer_text},
            )
            return redirect('homework_detail', pk=homework.pk)

    existing = Submission.objects.filter(
        homework=homework,
        student=request.user,
    ).first()

    return render(request, 'board/submit_homework.html', {
        'homework': homework,
        'existing': existing,
    })


def grades_table(request):
    submissions = Submission.objects.select_related('student', 'homework', 'homework__subject')\
                                    .exclude(grade__isnull=True)
    return render(request, 'board/grades_table.html', {'submissions': submissions})
