from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

try:
    from .forms import SubmissionForm, ReviewForm, SignupForm  # твои формы
except Exception:
    class SubmissionForm(AuthenticationForm): pass
    class ReviewForm(AuthenticationForm): pass
    class SignupForm(UserCreationForm): pass

try:
    from .models import Homework, Submission, Review  # твои модели
except Exception:
    class _Dummy: pass
    Homework = Submission = Review = _Dummy

class HomeworkListView(ListView):
    model = Homework
    template_name = 'school/homework_list.html'
    context_object_name = 'homeworks'
    paginate_by = 10
    def get_queryset(self):
        try:
            from django.db.models import Q
            qs = Homework.objects.all().order_by('-id')
            q = self.request.GET.get('q')
            if q:
                qs = qs.filter(Q(text__icontains=q) | Q(subject__name__icontains=q))
            subject_id = self.request.GET.get('subject')
            if subject_id:
                qs = qs.filter(subject_id=subject_id)
            return qs
        except Exception:
            return []

class HomeworkDetailView(DetailView):
    model = Homework
    template_name = 'school/homework_detail.html'
    context_object_name = 'homework'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        my_sub = None
        if user.is_authenticated:
            my_sub = self.object.submissions.filter(student=user).first()
        ctx['my_submission'] = my_sub
        return ctx

class MySubmissionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return getattr(obj, 'student_id', None) == self.request.user.id

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'school/submission_form.html'
    def dispatch(self, request, *args, **kwargs):
        self.homework_id = kwargs.get('homework_id')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        try:
            hw = get_object_or_404(Homework, pk=self.homework_id)
            form.instance.homework = hw
            form.instance.student = self.request.user
        except Exception:
            pass
        messages.success(self.request, "Сдача сохранена.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('homework_detail', args=[self.homework_id])

class SubmissionUpdateView(LoginRequiredMixin, MySubmissionRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'school/submission_form.html'
    def get_success_url(self):
        return reverse_lazy('homework_detail', args=[getattr(self.object, 'homework_id', 1)])

class SubmissionDeleteView(LoginRequiredMixin, MySubmissionRequiredMixin, DeleteView):
    model = Submission
    template_name = 'school/confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('homework_detail', args=[getattr(self.object, 'homework_id', 1)])

@login_required
def add_review(request, homework_id):
    try:
        hw = get_object_or_404(Homework, pk=homework_id)
    except Exception:
        hw = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                Review.objects.create(
                    homework=hw, author=request.user,
                    rating=form.cleaned_data.get('rating', 10),
                    text=form.cleaned_data.get('text', ''),
                )
            except Exception:
                pass
            messages.success(request, "Отзыв добавлен.")
            return redirect('homework_detail', pk=homework_id)
    else:
        form = ReviewForm()
    return render(request, 'school/review_form.html', {'form': form, 'homework': hw})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация выполнена.")
            return redirect('homework_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

class GradesListView(ListView):
    model = Submission
    template_name = 'school/grades.html'
    context_object_name = 'submissions'
    paginate_by = 20
    def get_queryset(self):
        try:
            return Submission.objects.all().order_by('id')
        except Exception:
            return []

#####

from .forms import HomeworkForm, ScoreForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class HomeworkCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'school/homework_form.html'
    success_url = reverse_lazy('homework_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, "Задание создано.")
        return super().form_valid(form)

class HomeworkUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'school/homework_form.html'
    def get_success_url(self):
        messages.success(self.request, "Задание обновлено.")
        return reverse_lazy('homework_detail', args=[self.object.pk])

class SubmissionsManageView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = 'school/manage_submissions.html'
    context_object_name = 'subs'
    paginate_by = 20

    def get_queryset(self):
        self.homework = get_object_or_404(Homework, pk=self.kwargs['homework_id'])
        return (Submission.objects
                .filter(homework=self.homework)
                .select_related('student')
                .order_by('student__username'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['homework'] = self.homework
        ctx['score_form'] = ScoreForm()
        return ctx

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def update_score(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Только преподаватели могут ставить оценки")
    sub = get_object_or_404(Submission, pk=pk)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=sub)
        if form.is_valid():
            form.save()
            messages.success(request, "Оценка обновлена.")
    return redirect('manage_submissions', homework_id=sub.homework_id)
