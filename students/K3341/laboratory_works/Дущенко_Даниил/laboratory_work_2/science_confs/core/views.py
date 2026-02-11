from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conference, Participation, Review
from .forms import RegisterForm, ParticipationForm, ReviewForm


def index(request):
    query = request.GET.get('q', '') 
    confs_list = Conference.objects.all()

    if query:
        
        confs_list = confs_list.filter(
            Q(title__icontains=query) | Q(topics__icontains=query)
        )

    
    paginator = Paginator(confs_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/index.html', {
        'page_obj': page_obj, 
        'query': query
    })


def conference_detail(request, pk):
    conf = get_object_or_404(Conference, pk=pk)
    
 
    participants = Participation.objects.filter(conference=conf)
    reviews = Review.objects.filter(conference=conf)


    user_part = None
    if request.user.is_authenticated:
        user_part = Participation.objects.filter(user=request.user, conference=conf).first()


    if request.method == 'POST' and 'review_submit' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.conference = conf
            rev.save()
            return redirect('conference_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'core/detail.html', {
        'conf': conf,
        'participants': participants,
        'reviews': reviews,
        'user_part': user_part,
        'form': form
    })


@login_required
def participate(request, pk):
    conf = get_object_or_404(Conference, pk=pk)
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            part.user = request.user
            part.conference = conf
            part.save()
            return redirect('conference_detail', pk=pk)
    else:
        form = ParticipationForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Подача заявки'})


@login_required
def edit_participation(request, pk):
    part = get_object_or_404(Participation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ParticipationForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('conference_detail', pk=part.conference.pk)
    else:
        form = ParticipationForm(instance=part)
    return render(request, 'core/form.html', {'form': form, 'title': 'Редактирование'})


@login_required
def delete_participation(request, pk):
    part = get_object_or_404(Participation, pk=pk, user=request.user)
    conf_id = part.conference.pk
    part.delete()
    return redirect('conference_detail', pk=conf_id)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})