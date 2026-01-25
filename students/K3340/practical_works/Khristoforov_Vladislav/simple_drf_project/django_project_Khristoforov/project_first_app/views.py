from django.shortcuts import render
from django.http import Http404
from .models import Car_Owner

def owner_detail(request, owner_id):
    try:
        owner = Car_Owner.objects.get(pk=owner_id)
    except Car_Owner.DoesNotExist:
        raise Http404("Владелец не найден")
    return render(request, 'owner.html', {'owner': owner})