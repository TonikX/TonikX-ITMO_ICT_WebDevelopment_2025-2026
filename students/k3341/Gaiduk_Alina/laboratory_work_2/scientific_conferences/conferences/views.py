from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Conference, Registration, Review, Topic
from .forms import RegistrationForm, ReviewForm


def conference_list(request):
    topic_id = request.GET.get('topic')
    q = request.GET.get('q', '')

    conferences = (Conference.objects
                   .select_related('place')
                   .prefetch_related('topics')
                   .order_by('-start_date')) # получаем все конференции через join

    if topic_id:
        conferences = conferences.filter(topics__id=topic_id) # фильтрация тем

    if q:
        conferences = conferences.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(participation_terms__icontains=q) |
            Q(topics__name__icontains=q) |
            Q(place__name__icontains=q) |
            Q(place__address__icontains=q)
        ).distinct()

    paginator = Paginator(conferences, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    topics = Topic.objects.all().order_by('name')

    return render(
        request,
        'conferences/conference_list.html',
        {
            'page_obj': page_obj,
            'topics': topics,
            'current_topic': int(topic_id) if topic_id else None,
            'q': q,
        },
    )


def conference_detail(request, pk):
    conference = get_object_or_404(
        Conference.objects.select_related('place').prefetch_related('topics'),
        pk=pk
    )

    registrations = (Registration.objects
                     .filter(conference=conference)
                     .select_related('user')
                     .order_by('-created'))

    reviews = (Review.objects
               .filter(conference=conference)
               .select_related('user')
               .order_by('-date_posted'))

    user_registration = None
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(
            conference=conference, user=request.user
        ).first() # получаем регистрацию пользователя

    return render(
        request,
        'conferences/conference_detail.html',
        {
            'conference': conference,
            'registrations': registrations,
            'reviews': reviews,
            'user_registration': user_registration,
            'review_form': ReviewForm(),
        },
    )


@login_required
def register_for_conference(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    # один пользователь - одна регистрация на конференцию
    registration, _ = Registration.objects.get_or_create(
        user=request.user, conference=conference
    )

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            # user/conference не даём подменить через POST
            obj = form.save(commit=False)
            obj.user = request.user
            obj.conference = conference
            obj.save()
            return redirect('conference_detail', pk=pk)
    else:
        form = RegistrationForm(instance=registration) # при гет запросе просто показываем пустую форму

    return render(request, 'conferences/registration_form.html', {'form': form})


@login_required
def delete_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    conference_pk = registration.conference.pk
    registration.delete()
    return redirect('conference_detail', pk=conference_pk)


@login_required
def add_review(request, pk):
    conference = get_object_or_404(Conference, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) # не добавляем отзыв сразу в бд
            review.user = request.user
            review.conference = conference
            # фиксируем даты конференции в момент добавления отзыва
            review.conf_start_date = conference.start_date
            review.conf_end_date = conference.end_date
            try:
                review.save()  # учтёт unique_together (conference, user)
            except IntegrityError:
                form.add_error(None, "Вы уже оставляли отзыв на эту конференцию.")
                return render(request, 'conferences/review_form.html', {'form': form})
            return redirect('conference_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'conferences/review_form.html', {'form': form})

def staff_check(user):
    return user.is_staff  # или user.is_superuser, если хочешь жёстко


@require_POST
@user_passes_test(staff_check)
def set_registration_result(request, reg_id):
    registration = get_object_or_404(Registration, pk=reg_id)

    new_status = request.POST.get("result")
    allowed = {'pending', 'recommended', 'not_recommended'}
    if new_status not in allowed:
        return HttpResponseForbidden("Недопустимый статус")

    registration.result = new_status
    registration.save()

    return redirect('conference_detail', pk=registration.conference.pk)