from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RegistrationForm, ReviewForm
from .models import Conference, Registration, Review

class ConferenceListView(ListView):
    model = Conference
    template_name = 'core/conference_list.html'
    context_object_name = 'conferences'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('venue').prefetch_related('topics')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(venue__name__icontains=q) |
                Q(topics__name__icontains=q)
            ).distinct()
        return qs

class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'core/conference_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        conf = self.object
        user = self.request.user
        ctx['registrations'] = conf.registrations.select_related('user')
        ctx['reviews'] = conf.reviews.select_related('user')
        ctx['reg_form'] = RegistrationForm()
        ctx['review_form'] = ReviewForm()
        if user.is_authenticated:
            ctx['my_registration'] = Registration.objects.filter(user=user, conference=conf).first()
        return ctx

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return getattr(obj, 'user_id', None) == self.request.user.id

class RegistrationCreateView(LoginRequiredMixin, CreateView):
    model = Registration
    form_class = RegistrationForm

    def form_valid(self, form):
        conference_id = self.kwargs['pk']
        form.instance.user = self.request.user
        form.instance.conference_id = conference_id
        return super().form_valid(form)

class RegistrationUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm

class RegistrationDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Registration
    success_url = reverse_lazy('conference_list')

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.conference_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.conference.get_absolute_url()

class ReviewUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        return self.object.conference.get_absolute_url()

class ReviewDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Review

    def get_success_url(self):
        return self.object.conference.get_absolute_url()

class ParticipantsTableView(ListView):
    template_name = 'core/participants.html'
    context_object_name = 'conferences'
    model = Conference

    def get_queryset(self):
        return (Conference.objects
                .select_related('venue')
                .prefetch_related('registrations__user')
                .annotate(participants_count=Count('registrations'))
                .order_by('-participants_count', 'title'))

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')