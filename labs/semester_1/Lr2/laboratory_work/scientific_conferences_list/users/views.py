from django.views.generic import CreateView, TemplateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .forms import SignUpForm, EditUserForm
from .models import User


class CustomSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('conferences_list')


class ConfirmLogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'users/logout.html'


class WelcomeView(TemplateView):
    template_name = 'users/welcome.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


class EditUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'users/edit_user.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        if user != self.request.user:
            raise PermissionDenied("Вы можете изменять данные только своего профиля")
        return user
    
    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.kwargs['pk']})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/edit_password.html'
    
    def get_success_url(self):
        return reverse_lazy('edit_user', kwargs={'pk': self.kwargs['pk']})
