from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import User, Subject, Assignment, Submission, Grade
from .forms import CustomUserCreationForm, AssignmentForm, SubmissionForm, GradeForm, AssignmentSearchForm, GradeSearchForm


def home(request):
    """Главная страница"""
    context = {
        'total_assignments': Assignment.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.count(),
        'recent_assignments': Assignment.objects.filter(is_active=True).order_by('-created_at')[:5],
    }
    
    if request.user.is_authenticated:
        if request.user.role == User.STUDENT:
            context['my_submissions'] = Submission.objects.filter(student=request.user).order_by('-submitted_at')[:5]
        elif request.user.role in [User.TEACHER, User.ADMIN]:
            context['pending_grades'] = Submission.objects.filter(grade__isnull=True).count()
    
    return render(request, 'assignments/home.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'assignments/register.html', {'form': form})


class AssignmentListView(ListView):
    """Список заданий с поиском и фильтрацией"""
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Assignment.objects.filter(is_active=True).select_related('subject', 'teacher').order_by('-created_at')
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(subject__name__icontains=search)
            )
        
        # Фильтр по предмету
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status == 'overdue':
            queryset = queryset.filter(due_date__lt=timezone.now())
        elif status == 'active':
            queryset = queryset.filter(due_date__gte=timezone.now())
        elif status == 'completed' and self.request.user.is_authenticated and self.request.user.role == User.STUDENT:
            submitted_assignments = Submission.objects.filter(student=self.request.user).values_list('assignment_id', flat=True)
            queryset = queryset.filter(id__in=submitted_assignments)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AssignmentSearchForm(self.request.GET)
        context['subjects'] = Subject.objects.all()
        return context


class AssignmentDetailView(DetailView):
    """Детальная информация о задании"""
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        
        if self.request.user.is_authenticated and self.request.user.role == User.STUDENT:
            # Проверяем, сдал ли студент это задание
            try:
                submission = Submission.objects.get(assignment=assignment, student=self.request.user)
                context['submission'] = submission
                context['grade'] = getattr(submission, 'grade', None)
            except Submission.DoesNotExist:
                context['submission'] = None
        
        return context


@login_required
def submit_assignment(request, pk):
    """Сдача задания"""
    assignment = get_object_or_404(Assignment, pk=pk, is_active=True)
    
    if request.user.role != User.STUDENT:
        messages.error(request, 'Только студенты могут сдавать задания.')
        return redirect('assignment_detail', pk=pk)
    
    # Проверяем, не сдано ли уже задание
    try:
        existing_submission = Submission.objects.get(assignment=assignment, student=request.user)
        messages.info(request, 'Вы уже сдали это задание.')
        return redirect('assignment_detail', pk=pk)
    except Submission.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, assignment=assignment)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Задание успешно сдано!')
            return redirect('assignment_detail', pk=pk)
    else:
        form = SubmissionForm(assignment=assignment)
    
    return render(request, 'assignments/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })


class GradeListView(LoginRequiredMixin, ListView):
    """Список оценок (только для преподавателей и админов)"""
    model = Grade
    template_name = 'assignments/grade_list.html'
    context_object_name = 'grades'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in [User.TEACHER, User.ADMIN]:
            messages.error(request, 'У вас нет прав для просмотра оценок.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Grade.objects.select_related('submission__student', 'submission__assignment__subject', 'graded_by').order_by('-graded_at')
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(submission__student__first_name__icontains=search) |
                Q(submission__student__last_name__icontains=search) |
                Q(submission__assignment__title__icontains=search) |
                Q(submission__student__student_id__icontains=search)
            )
        
        # Фильтр по предмету
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(submission__assignment__subject_id=subject_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = GradeSearchForm(self.request.GET)
        context['subjects'] = Subject.objects.all()
        return context


@login_required
def grade_submission(request, submission_id):
    """Оценка сдачи задания"""
    submission = get_object_or_404(Submission, pk=submission_id)
    
    if request.user.role not in [User.TEACHER, User.ADMIN]:
        messages.error(request, 'У вас нет прав для оценки заданий.')
        return redirect('home')
    
    # Проверяем, не оценено ли уже задание
    try:
        existing_grade = Grade.objects.get(submission=submission)
        messages.info(request, 'Это задание уже оценено.')
        return redirect('grade_list')
    except Grade.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = GradeForm(request.POST, submission=submission)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.graded_by = request.user
            grade.save()
            messages.success(request, 'Оценка поставлена!')
            return redirect('grade_list')
    else:
        form = GradeForm(submission=submission)
    
    return render(request, 'assignments/grade_submission.html', {
        'form': form,
        'submission': submission
    })


class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание задания (только для преподавателей и админов)"""
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignment_list')
    
    def test_func(self):
        return self.request.user.role in [User.TEACHER, User.ADMIN]
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'Задание создано!')
        return super().form_valid(form)


class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование задания"""
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignment_list')
    
    def test_func(self):
        assignment = self.get_object()
        return (self.request.user.role in [User.TEACHER, User.ADMIN] and 
                (assignment.teacher == self.request.user or self.request.user.role == User.ADMIN))


class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление задания"""
    model = Assignment
    template_name = 'assignments/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignment_list')
    
    def test_func(self):
        assignment = self.get_object()
        return (self.request.user.role in [User.TEACHER, User.ADMIN] and 
                (assignment.teacher == self.request.user or self.request.user.role == User.ADMIN))


@login_required
def my_submissions(request):
    """Мои сдачи (только для студентов)"""
    if request.user.role != User.STUDENT:
        messages.error(request, 'У вас нет прав для просмотра сдач.')
        return redirect('home')
    
    submissions = Submission.objects.filter(student=request.user).select_related('assignment__subject').order_by('-submitted_at')
    
    # Пагинация
    paginator = Paginator(submissions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'assignments/my_submissions.html', {
        'page_obj': page_obj,
        'submissions': page_obj
    })


@login_required
def statistics(request):
    """Статистика (только для преподавателей и админов)"""
    if request.user.role not in [User.TEACHER, User.ADMIN]:
        messages.error(request, 'У вас нет прав для просмотра статистики.')
        return redirect('home')
    
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()
    total_grades = Grade.objects.count()

    subject_stats = Subject.objects.annotate(
        assignment_count=Count('assignment'),
        submission_count=Count('assignment__submissions'),
        avg_grade=Avg('assignment__submissions__grade__points')
    ).order_by('-assignment_count')
    
    top_students = User.objects.filter(
        role=User.STUDENT,
        submissions__grade__isnull=False
    ).annotate(
        avg_grade=Avg('submissions__grade__points'),
        submission_count=Count('submissions')
    ).order_by('-avg_grade')[:10]
    
    context = {
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'total_grades': total_grades,
        'subject_stats': subject_stats,
        'top_students': top_students,
    }
    
    return render(request, 'assignments/statistics.html', context)


def profile(request):
    """Профиль пользователя"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_submissions = AssignmentSubmission.objects.filter(student=request.user)
    user_grades = Grade.objects.filter(submission__student=request.user)
    
    # Статистика по предметам
    subject_stats = {}
    for submission in user_submissions:
        subject = submission.assignment.subject.name
        if subject not in subject_stats:
            subject_stats[subject] = {
                'total_assignments': 0,
                'submitted': 0,
                'graded': 0,
                'avg_grade': 0
            }
        subject_stats[subject]['total_assignments'] += 1
        if submission.submitted_at:
            subject_stats[subject]['submitted'] += 1
        if submission.grade:
            subject_stats[subject]['graded'] += 1
    
    # Вычисляем средние оценки
    for subject in subject_stats:
        grades = user_grades.filter(submission__assignment__subject__name=subject)
        if grades.exists():
            subject_stats[subject]['avg_grade'] = round(
                grades.aggregate(avg=Avg('points'))['avg'], 2
            )
    
    context = {
        'user_submissions': user_submissions,
        'user_grades': user_grades,
        'subject_stats': subject_stats,
        'total_submissions': user_submissions.count(),
        'total_grades': user_grades.count(),
    }
    
    return render(request, 'assignments/profile.html', context)