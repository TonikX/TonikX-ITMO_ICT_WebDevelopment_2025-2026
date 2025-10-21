from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Ownership, Car
from .forms import CarForm
from .forms import CustomUserCreationForm

def owner_detail(request, owner_id: int):
    User = get_user_model()
    owner = get_object_or_404(User, pk=owner_id)
    ownerships = (
        Ownership.objects.select_related('car', 'owner')
        .filter(owner=owner).order_by('-start_date')
    )
    return render(request, 'owner.html', {'owner': owner, 'ownerships': ownerships})

def owners_list(request):
    User = get_user_model()
    context = {"owners": User.objects.all().order_by('last_name', 'first_name')}
    return render(request, "owners_list.html", context)

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    ordering = ['make', 'model']

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['plate_number', 'make', 'model', 'color']  # какие поля редактируем
    template_name = 'car_form.html'  # общий шаблон формы
    success_url = reverse_lazy('car_list')

def owner_create(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        # после сохранения можно вернуть на список владельцев
        return render(request, "owner_create_success.html", {"owner": form.instance})
    return render(request, "owner_create.html", {"form": form})

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm           # используем нашу форму
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('owners_list')