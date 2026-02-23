from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from .models import Racer, Race, User, Results, Comments
from .forms import UserRegisterForm, RaceForm, RacerCreateForm, RacerUpdateForm, commentForm
from django.contrib.auth.views import LoginView



#работа с регистрациями
def hello_function(request):
    if request.user.is_authenticated:
        return redirect('race_list')

    else:
        return redirect('Hello')

class HelloView(TemplateView):
    template_name = 'hello.html'

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('race_list')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('race_list')



class RaceListView(ListView):
    model = Race
    template_name = 'race_list.html'
    context_object_name = 'races'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(date__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context




class RaceCreateView(CreateView):
    model = Race
    template_name = 'race_form.html'
    form_class = RaceForm

    def get_success_url(self):
        return reverse_lazy('race_list')


class RaceDeleteView(DeleteView):
    model = Race
    context_object_name = 'race'
    success_url = reverse_lazy('race_list')


# внутри Гонки

class RaceDetailView(TemplateView):
    template_name = 'race_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = get_object_or_404(Race, pk=kwargs['pk'])
        context['race'] = race
        comments = Comments.objects.filter(race=race)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(comments, 5)
        try:
            page_comments = paginator.page(page)
        except PageNotAnInteger:
            page_comments = paginator.page(1)
        except EmptyPage:
            page_comments = paginator.page(paginator.num_pages)
        context['comments'] = page_comments
        context['racers'] = race.racers.all()
        context['race_results'] = Results.objects.filter(race=race)

        if self.request.user.is_authenticated:
            user_is_registered = race.racers.filter(user=self.request.user).exists()
        else:
            user_is_registered = False

        context['user_is_registered'] = user_is_registered

        context['race_has_occurred'] = race.has_occurred

        if not user_is_registered and not race.has_occurred and self.request.user.is_authenticated:
            context['racer_form'] = RacerCreateForm()
        else:
            context['racer_form'] = None

        if self.request.user.is_authenticated:
            context['comment_form'] = commentForm()
        else:
            context['comment_form'] = None

        return context

    def post(self, request, *args, **kwargs):
        race = get_object_or_404(Race, pk=kwargs['pk'])

        if 'register' in request.POST:
            racer_form = RacerCreateForm(request.POST)
            if racer_form.is_valid():
                racer = racer_form.save(commit=False)
                racer.user = request.user
                racer.race = race
                racer.save()
                return redirect('race_detail', pk=race.pk)

        if 'send_comment' in request.POST:
            comment_form = commentForm(request.POST)
            if comment_form.is_valid():
                existing_comment = Comments.objects.filter(user=request.user, race=race, comment=comment_form.cleaned_data['comment'])
                if existing_comment.exists():
                    return redirect('race_detail', pk=race.pk)
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.race = race
                comment.save()

                return redirect('race_detail', pk=race.pk)




class RacerDeleteView(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            racer = get_object_or_404(Racer, pk=self.kwargs['pk'])
        else:
            racer = get_object_or_404(Racer, pk=self.kwargs['pk'], user=request.user)
        race_pk = racer.race.pk
        racer.delete()
        return redirect('race_detail', pk=race_pk)

class RacerUpdateView(UpdateView):
    model = Racer
    form_class = RacerUpdateForm
    template_name = 'racer_update.html'

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            return get_object_or_404(Racer, pk=self.kwargs['pk'])
        else:
            return get_object_or_404(Racer, pk=self.kwargs['pk'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = self.object.race
        return context

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.object.race.pk})