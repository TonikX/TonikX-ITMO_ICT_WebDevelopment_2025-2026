from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View, CreateView
from django.db.models import Q
from .models import Homework, Submission, Subject
from .forms import SubmissionForm, HomeworkForm, SubjectForm
from accounts.models import User
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from .forms import SubmissionForm, HomeworkForm, SubjectForm

# 9.1 Список ДЗ + поиск + пагинация
class HomeworkListView(ListView):
    model = Homework
    template_name = "board/homework_list.html"
    context_object_name = "homeworks"
    paginate_by = 5  # на страницу по 5 штук

    def get_queryset(self):
        qs = Homework.objects.select_related("subject", "teacher").order_by("due_date")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(subject__name__icontains=q) |
                Q(teacher__username__icontains=q) |
                Q(text__icontains=q)
            )
        return qs

# 9.2 Детали ДЗ (форма сдачи показывается студенту)
class HomeworkDetailView(DetailView):
    model = Homework
    template_name = "board/homework_detail.html"
    context_object_name = "homework"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        existing = None
        if self.request.user.is_authenticated and self.request.user.role == 'student':
            existing = Submission.objects.filter(
                homework=self.object, student=self.request.user
            ).first()
        ctx["existing_submission"] = existing
        ctx["form"] = SubmissionForm()
        return ctx

# 9.3 Отправка/обновление сдачи (только студент)
@method_decorator(login_required, name='dispatch')
class SubmitHomeworkView(View):
    def post(self, request, pk):
        hw = get_object_or_404(Homework, pk=pk)
        if request.user.role != 'student':
            return redirect("homework_detail", pk=pk)

        form = SubmissionForm(request.POST)
        if form.is_valid():
            sub, created = Submission.objects.get_or_create(
                homework=hw, student=request.user,
                defaults={"content": form.cleaned_data["content"]}
            )
            if not created:
                sub.content = form.cleaned_data["content"]
                sub.save()
        return redirect("homework_detail", pk=pk)

# 9.4 Таблица оценок (видит только teacher/staff)
@login_required
def gradebook_view(request):
    if not (request.user.is_staff or request.user.role == 'teacher'):
        return redirect("homework_list")

    students = User.objects.filter(role='student').order_by("username")
    homeworks = Homework.objects.select_related("subject").order_by("due_date")

    # подготовим строки для удобного шаблона
    # rows = [ {student: User, grades: [grade or None aligned to homeworks]} ]
    subs = Submission.objects.filter(student__in=students, homework__in=homeworks)\
                             .values("student_id", "homework_id", "grade")
    # словарь для быстрого доступа
    lookup = {}
    for s in subs:
        lookup[(s["student_id"], s["homework_id"])] = s["grade"]

    rows = []
    for st in students:
        row_grades = []
        for hw in homeworks:
            row_grades.append(lookup.get((st.id, hw.id)))
        rows.append({"student": st, "grades": row_grades})

    return render(request, "board/gradebook.html", {
        "students": students,
        "homeworks": homeworks,
        "rows": rows,
    })

class OnlyTeacherMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_staff or getattr(u, "role", "") == "teacher"

class HomeworkCreateView(OnlyTeacherMixin, CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = "board/homework_form.html"

    def form_valid(self, form):
        form.instance.teacher = self.request.user  # кто создал — тот и преподаватель
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("homework_detail", args=[self.object.pk])

class SubjectCreateView(OnlyTeacherMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "board/subject_form.html"

    def get_success_url(self):
        return reverse("homework_create")  # после создания предмета вернёмся к форме ДЗ

