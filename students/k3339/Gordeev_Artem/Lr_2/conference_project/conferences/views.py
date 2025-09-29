from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView

from .models import Conference


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
