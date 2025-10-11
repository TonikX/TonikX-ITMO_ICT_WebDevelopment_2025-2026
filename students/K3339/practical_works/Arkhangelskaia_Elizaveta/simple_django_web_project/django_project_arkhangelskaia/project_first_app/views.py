from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render
from project_first_app.models import CarOwner, Ownership


def owner_list(request, car_id):
    try:
        owners = Ownership.objects.filter(car_id=car_id).first()
    except Ownership.DoesNotExist:
        raise Http404("owners does not exist")
    return render(request, 'owner_list.html', {'owners': owners})