from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import RegistrationForm, ReviewForm
from .models import Conference, Registration, Review

class ConferenceListView(ListView):
    model = Conference
    template_name = 'conferences/conf_list.html'
    context_object_name = 'confs'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = Conference.objects.select_related('venue').prefetch_related('topics')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(participation_terms__icontains=q) |
                Q(venue__name__icontains=q) |
                Q(venue__city__icontains=q) |
                Q(topics__name__icontains=q)
            ).distinct()
        return qs

class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conferences/conf_detail.html'
    context_object_name = 'conf'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        conf = self.object
        ctx['registrations'] = conf.registrations.select_related('author').all()
        ctx['reviews'] = conf.reviews.select_related('reviewer').all()
        ctx['can_register'] = self.request.user.is_authenticated
        return ctx

class RegistrationCreateView(LoginRequiredMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'conferences/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.conference = get_object_or_404(Conference, pk=kwargs['conf_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.conference = self.conference
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.conference.get_absolute_url() if hasattr(self.conference, 'get_absolute_url') else reverse_lazy('conf_detail', kwargs={'pk': self.conference.pk})

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id or self.request.user.is_staff

class RegistrationUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'conferences/registration_form.html'

    def get_success_url(self):
        return reverse_lazy('conf_detail', kwargs={'pk': self.object.conference_id})

class RegistrationDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Registration
    template_name = 'conferences/registration_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('conf_detail', kwargs={'pk': self.object.conference_id})

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'conferences/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.conference = get_object_or_404(Conference, pk=kwargs['conf_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.conference = self.conference
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('conf_detail', kwargs={'pk': self.conference.pk})

class ParticipantsTableView(TemplateView):
    template_name = 'conferences/participants.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        confs = Conference.objects.select_related('venue').prefetch_related(
            Prefetch('registrations', queryset=Registration.objects.select_related('author'))
        )
        ctx['confs'] = confs
        return ctx