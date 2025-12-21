import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from collections import defaultdict
from .models import *

def pagination_main(request):
    queryset = Article.objects.filter(article_status=True).order_by('-article_date')
    paginate_by = 10
    return render(request, 'pagination.html', {"page": 1})