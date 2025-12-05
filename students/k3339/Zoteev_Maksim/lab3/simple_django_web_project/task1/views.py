from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CarOwner, Car
from .forms import CarOwnerRegistrationForm, CarForm


def owners_list(request):
    """Контроллер для отображения списка всех владельцев"""
    owners = CarOwner.objects.all()
    return render(request, "owners_list.html", {"owners": owners})


def owner_detail(request, owner_id):
    """Контроллер для отображения детальной информации о владельце автомобиля"""
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("CarOwner does not exist")

    return render(request, "owner_detail.html", {"owner": owner})


def create_owner(request):
    """Function-based view для регистрации нового владельца (пользователя) через форму"""
    if request.method == "POST":
        form = CarOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"Пользователь {user.username} успешно зарегистрирован!"
            )
            return redirect("owners_list")
    else:
        form = CarOwnerRegistrationForm()

    return render(
        request, "owner_form.html", {"form": form, "title": "Регистрация владельца"}
    )


class CarListView(ListView):
    """Class-based view для отображения списка всех автомобилей"""

    model = Car
    template_name = "cars_list.html"
    context_object_name = "cars"


class CarDetailView(DetailView):
    """Class-based view для отображения детальной информации об автомобиле"""

    model = Car
    template_name = "car_detail.html"
    context_object_name = "car"
    pk_url_kwarg = "car_id"


class CarCreateView(CreateView):
    """Class-based view для создания автомобиля"""

    model = Car
    form_class = CarForm
    template_name = "car_form.html"
    success_url = reverse_lazy("cars_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить автомобиль"
        return context


class CarUpdateView(UpdateView):
    """Class-based view для редактирования автомобиля"""

    model = Car
    form_class = CarForm
    template_name = "car_form.html"
    success_url = reverse_lazy("cars_list")
    pk_url_kwarg = "car_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать автомобиль"
        return context


class CarDeleteView(DeleteView):
    """Class-based view для удаления автомобиля"""

    model = Car
    template_name = "car_confirm_delete.html"
    success_url = reverse_lazy("cars_list")
    pk_url_kwarg = "car_id"
