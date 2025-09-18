from django.shortcuts import render
from django.http import Http404
from .models import Owner

def owner_detail(request, owner_id):
    """Метод выводит информации об Автовладельце"""

    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})
