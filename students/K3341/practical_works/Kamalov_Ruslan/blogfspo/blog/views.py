from django.shortcuts import render, get_object_or_404
from .models import Owner, Ownership

def owner_detail(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)

    owner_ownerships = Ownership.objects.filter(owner=owner)

    context = {
        'owner': owner,
        'owner_ownerships': owner_ownerships,
    }
    return render(request, 'blog/owner_detail.html', context)
