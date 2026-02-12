# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse_lazy
# from django.views.generic import DetailView, ListView, UpdateView

# from .forms import CarOwnerForm
# from .models import Car, CarOwner


# def add_owner(request):
#     if request.method == 'POST':
#         form = CarOwnerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("owners_list")
#     else:
#         form = CarOwnerForm()
#     return render(request, "add_owner.html", {"form": form})

# def owner_detail(request, owner_id):
#     owner = get_object_or_404(CarOwner, pk=owner_id)
#     return render(request, "owner.html", {"owner": owner})

# def owners_list(request):
#     owners = CarOwner.objects.all()
#     return render(request, "owners_list.html", {"owners": owners})

# class CarListView(ListView):
#     model = Car
#     template_name = "car_list.html"
#     context_object_name = "cars"

# class CarDetailView(DetailView):
#     model = Car
#     template_name = "car_detail.html"
#     context_object_name = "car"

# class CarUpdateView(UpdateView):
#     model = Car
#     fields = ["state_number", "brand", "model", "color"]
#     template_name = "car_update.html"
#     success_url = reverse_lazy("car_list")