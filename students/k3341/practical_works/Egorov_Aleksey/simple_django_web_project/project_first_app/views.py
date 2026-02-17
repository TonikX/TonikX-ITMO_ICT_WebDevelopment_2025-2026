from django.shortcuts import render
from django.http import Http404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView

from project_first_app.models import CarOwner
from project_first_app.models import Car
from project_first_app.forms import CarOwnerForm

# Create your views here.

def owner(request, owner_id):
    try:
        p = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'project_first_app/owner.html', {'owner': p})


def get_owners(request):
    context = {}
    context['dataset'] = CarOwner.objects.all()
    return render(request, 'project_first_app/list_owners.html', context)
    
    
class CarList(ListView):
    model = Car
    

class CarRetrieveView(DetailView):
    model = Car
    
    
def create_view(request):
    context = {}
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'project_first_app/create_view.html', context)
    
    
class CarCreateView(CreateView):
    model = Car
    fields = ['state_number', 'brand', 'model', 'colour']
    success_url = '/car/list/'
    
    
class CarUpdateView(UpdateView):
    model = Car
    fields = ['state_number', 'brand', 'model', 'colour']
    success_url = '/car/list/'
    

class CarDeleteView(DeleteView):
    model = Car
    success_url='/car/list/'