from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Conference, Presentation, Review
from .forms import RegisterPresentationForm, ConferenceForm

# === КОНФЕРЕНЦИИ ===

class ConferencesListView(LoginRequiredMixin, ListView):
    model = Conference
    template_name = 'conferences/conferences_list.html'
    context_object_name = 'conferences'
    paginate_by = 10


class ConferenceDetailView(LoginRequiredMixin, DetailView):
    model = Conference
    template_name = 'conferences/conference_detail.html'
    context_object_name = 'conference'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = self.object
        user_presentations = Presentation.objects.filter(
            conference=conference, 
            author=self.request.user
        )
        context['user_presentations'] = user_presentations
        return context


class AddConferenceView(LoginRequiredMixin, CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'conferences/add_conference.html'
    success_url = reverse_lazy('conferences_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Выполняет предварительную маршрутизацию и общую логику перед вызовом конкретного метода.
        """
        if not request.user.is_superuser:
            raise PermissionDenied("Создавать конференции могут только суперпользователи")
        return super().dispatch(request, *args, **kwargs)


class EditConferenceView(LoginRequiredMixin, UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'conferences/edit_conference.html'
    context_object_name = 'conference'
    success_url = reverse_lazy('conferences_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Выполняет предварительную маршрутизацию и общую логику перед вызовом конкретного метода.
        """
        if not request.user.is_superuser:
            raise PermissionDenied("Редактировать конференции могут только суперпользователи")
        return super().dispatch(request, *args, **kwargs)


class DeleteConferenceView(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = 'conferences/delete_conference.html'
    context_object_name = 'conference'
    success_url = reverse_lazy('conferences_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Выполняет предварительную маршрутизацию и общую логику перед вызовом конкретного метода.
        """
        if not request.user.is_superuser:
            raise PermissionDenied("Удалять конференции могут только суперпользователи")
        return super().dispatch(request, *args, **kwargs)


# === ВЫСТУПЛЕНИЯ ===


class RegisterPresentationView(LoginRequiredMixin, CreateView):
    model = Presentation
    form_class = RegisterPresentationForm
    template_name = 'conferences/presentations/register_presentation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['pk'])
        context['conference'] = conference
        return context

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs['pk'])
        presentation = form.save(commit=False)
        presentation.author = self.request.user
        presentation.conference = conference
        presentation.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('conference_detail', kwargs={'pk': self.kwargs['pk']})


class CancelPresentationView(LoginRequiredMixin, DeleteView):
    model = Presentation
    template_name = 'conferences/presentations/cancel_presentation.html'
    context_object_name = 'presentation'

    def get_object(self, queryset=None):
        presentation = get_object_or_404(Presentation, pk=self.kwargs['presentation_id'])
        if presentation.author != self.request.user:
            raise PermissionDenied("Вы можете отменять только свои выступления")
        return presentation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        context['conference'] = conference
        return context
    
    def get_success_url(self):
        return reverse_lazy('conference_detail', kwargs={'pk': self.kwargs['conference_id']})


class EditPresentationView(LoginRequiredMixin, UpdateView):
    model = Presentation
    fields = ['title', 'description']
    template_name = 'conferences/presentations/edit_presentation.html'
    context_object_name = 'presentation'

    def get_object(self, queryset=None):
        presentation = get_object_or_404(Presentation, pk=self.kwargs['presentation_id'])
        if presentation.author != self.request.user:
            raise PermissionDenied("Вы можете изменять только свои выступления")
        return presentation
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        context['conference'] = conference
        return context

    def get_success_url(self):
        return reverse_lazy('conference_detail', kwargs={'pk': self.kwargs['conference_id']})


class PresentationsListView(LoginRequiredMixin, ListView):
    model = Presentation
    template_name = 'conferences/presentations/presentations_list.html'
    context_object_name = 'presentations'
    paginate_by = 20

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Presentation.objects.filter(conference_id=conference_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        context['conference'] = conference
        return context


# === ОТЗЫВЫ ===


class ReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'conferences/reviews/reviews_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Review.objects.filter(conference_id=conference_id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        context['conference'] = conference
        return context


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'text']
    template_name = 'conferences/reviews/add_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        context['conference'] = conference
        return context

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs['conference_id'])
        review = form.save(commit=False)
        review.user = self.request.user
        review.conference = conference
        review.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reviews_list', kwargs={'conference_id': self.kwargs['conference_id']})
