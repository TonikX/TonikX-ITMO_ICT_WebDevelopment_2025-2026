from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q 

from .models import Race, Registration, Comment
from .forms import RaceRegistrationForm, CommentForm, UserRegisterForm


class RaceListView(ListView):
    model = Race
    template_name = 'race_app/race_list.html'
    context_object_name = 'races'

class RaceDetailView(DetailView):
    model = Race
    template_name = 'race_app/race_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        participants_all = Registration.objects.filter(race=self.object).order_by('result_place')
        
        query = self.request.GET.get('q')
        context['last_search'] = "" 
        if query:
            participants_all = participants_all.filter(team_name__icontains=query)
            context['last_search'] = f"&q={query}"

        paginator = Paginator(participants_all, 5)
        
        page_number = self.request.GET.get('page')
        
        try:
            participants_page_obj = paginator.get_page(page_number)
        except (PageNotAnInteger, EmptyPage):
            participants_page_obj = paginator.page(1)

        context['participants'] = participants_page_obj
        
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        
        if self.request.user.is_authenticated:
            context['user_registration'] = Registration.objects.filter(
                race=self.object, user=self.request.user
            ).first()
            
        return context
    
def add_comment(request, pk):
    if request.method == "POST" and request.user.is_authenticated:
        race = Race.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
    return redirect('race_detail', pk=pk)

class RegisterToRaceView(LoginRequiredMixin, CreateView):
    model = Registration
    form_class = RaceRegistrationForm
    template_name = 'race_app/register_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.race = Race.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.kwargs['pk']})
    

class RegistrationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Registration
    fields = ['team_name', 'car_description']
    template_name = 'race_app/registration_form.html'

    def test_func(self):
        registration = self.get_object()
        return self.request.user == registration.user

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.object.race.id})

class RegistrationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Registration
    template_name = 'race_app/registration_confirm_delete.html'

    def test_func(self):
        registration = self.get_object()
        return self.request.user == registration.user

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.object.race.id})
    

class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'