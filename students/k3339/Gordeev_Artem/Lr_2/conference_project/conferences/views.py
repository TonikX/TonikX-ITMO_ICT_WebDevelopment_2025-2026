from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .forms import ReviewForm, ParticipationForm
from .models import Conference, Participation, Review


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ConferenceListView(ListView):
    model = Conference
    template_name = 'conferences/conference_list.html'
    context_object_name = 'conferences'  # Имя переменной в шаблоне
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conferences/conference_detail.html'
    context_object_name = 'conference'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        if self.request.user.is_authenticated:
            context['user_participation'] = Participation.objects.filter(
                conference=self.object,
                participant=self.request.user
            ).first()

            context['user_has_reviewed'] = Review.objects.filter(
                conference=self.object,
                author=self.request.user
            ).exists()
        return context


class ParticipationCreateView(LoginRequiredMixin, CreateView):
    model = Participation
    form_class = ParticipationForm
    template_name = 'conferences/participation_form.html'

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs['conf_pk'])
        form.instance.participant = self.request.user
        form.instance.conference = conference
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.kwargs['conf_pk']})


class ParticipationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Participation
    form_class = ParticipationForm
    template_name = 'conferences/participation_form.html'

    def test_func(self):
        participation = self.get_object()
        return self.request.user == participation.participant

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.object.conference.pk})


class ParticipationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Participation
    template_name = 'conferences/participation_confirm_delete.html'

    def test_func(self):
        participation = self.get_object()
        return self.request.user == participation.participant

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.object.conference.pk})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs['conf_pk'])
        form.instance.author = self.request.user
        form.instance.conference = conference
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.kwargs['conf_pk']})
