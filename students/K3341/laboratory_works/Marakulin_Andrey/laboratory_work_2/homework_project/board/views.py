from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .forms import SignUpForm, SubmissionForm, HomeworkFilterForm
from .models import Homework, Submission


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class HomeworkListView(ListView):
    model = Homework
    template_name = 'board/homework_list.html'
    context_object_name = 'homeworks'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = HomeworkFilterForm(self.request.GET)
        return context


class HomeworkDetailView(DetailView):
    model = Homework
    template_name = 'board/homework_detail.html'
    context_object_name = 'homework'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            existing_submission = Submission.objects.filter(
                homework=self.get_object(),
                student=self.request.user
            ).first()

            if existing_submission:
                context['existing_submission'] = existing_submission
            else:
                context['submission_form'] = SubmissionForm()

        return context

    def post(self, request, *args, **kwargs):
        homework = self.get_object()
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()
            return redirect('homework_detail', pk=homework.pk)

        context = self.get_context_data()
        context['submission_form'] = form
        return self.render_to_response(context)


class GradebookView(UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'board/gradebook.html'
    context_object_name = 'submissions'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Submission.objects.select_related('homework', 'student').order_by('homework__title', 'student__username')
