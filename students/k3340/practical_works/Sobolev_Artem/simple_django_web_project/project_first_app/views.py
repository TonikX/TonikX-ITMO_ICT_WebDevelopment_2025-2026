from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from .forms import CarForm, OwnerForm
from .models import Car, CarOwner, Owner


class CarListView(ListView):
    model = Car
    queryset = Car.objects.all()
    template_name = "car/car_list.html"

class CarDetailView(DetailView):
    model = Car
    queryset = Car.objects.all()
    template_name = "car/car_detail.html"

class CarUpdateView(UpdateView):
    model = Car
    fields = ["state_number", "brand", "model", "color"]
    template_name = "car/car_form.html"

    def get_success_url(self):
        return reverse_lazy("car-detail", kwargs={"pk": self.object.pk})

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = "car/car_form.html"
    success_url = reverse_lazy("car-list")

class CarDeleteView(DeleteView):
    model = Car
    success_url = reverse_lazy("car-list")
    template_name = "car/car_delete.html"

def owner_list(request):
    owners = CarOwner.objects.all()
    return render(request, "owner/owner_list.html", {"owners": owners})

def car_owners(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        raise Http404("Car does not exist")

    owners = Owner.objects.filter(car_id=car).select_related("owner")

    owners = [o.owner for o in owners]

    return render(request, "owner/owner_by_car.html", {"owners": owners})

def add_owner(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("owner-list")
    else:
        form = OwnerForm()
    return render(request, "owner/create_owner.html", {"form": form})