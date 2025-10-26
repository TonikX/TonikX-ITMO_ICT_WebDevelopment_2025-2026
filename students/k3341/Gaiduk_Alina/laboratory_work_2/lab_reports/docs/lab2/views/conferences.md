# Views приложения `conferences`

## `conference_list`

```
def conference_list(request):
    topic_id = request.GET.get('topic')
    q = request.GET.get('q', '')

    conferences = (Conference.objects
                   .select_related('place')
                   .prefetch_related('topics')
                   .order_by('-start_date'))

    if topic_id:
        conferences = conferences.filter(topics__id=topic_id)

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
```

Отвечает за страницу со списком конференций.

* Поддерживает фильтрацию по тематике (`topic`) и полнотекстовый поиск (`q`) по названию, описанию, условиям участия, месту проведения.
* Делает `select_related` и `prefetch_related`, чтобы не было лишних запросов к БД.
* Делает пагинацию (по 3 конференции на страницу).
* Передаёт на шаблон ещё список всех тематик (`topics`) для фильтра.

Закрывает требования:

* «просмотр конференций»
* «пагинация»
* «поиск по объектам».

## `conference_detail`

```
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
        ).first()

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
```

Показывает детальную страницу одной конференции.

На шаблон отдаётся:

* сама конференция,
* все заявки (докладчики) с этой конференции,
* все отзывы,
* форма отзыва,
* текущая заявка пользователя (если он уже зарегистрирован).


## `register_for_conference`

```
@login_required
def register_for_conference(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    registration, _ = Registration.objects.get_or_create(
        user=request.user, conference=conference
    )

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.conference = conference
            obj.save()
            return redirect('conference_detail', pk=pk)
    else:
        form = RegistrationForm(instance=registration)

    return render(request, 'conferences/registration_form.html', {'form': form})
```

Позволяет пользователю зарегистрироваться как докладчик.

* `login_required`: только авторизованные.
* `get_or_create`: один пользователь не может создать две разные регистрации на одну и ту же конференцию.
* Пользователь может отредактировать свою заявку (название доклада, тезисы), потому что форма заполняется через `instance=registration`.

Реализует требование:

* «Регистрация авторов для выступлений»
* «Пользователь должен иметь возможность редактирования своей регистрации».

## `delete_registration`

```
@login_required
def delete_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    conference_pk = registration.conference.pk
    registration.delete()
    return redirect('conference_detail', pk=conference_pk)
```

Удаление своей регистрации.

* Можно удалить только свою (`pk=pk, user=request.user`).
* После удаления идёт редирект обратно на страницу конференции.

Реализует требование:

* «Пользователь должен иметь возможность удаления своих регистраций».

## `add_review`

```
@login_required
def add_review(request, pk):
    conference = get_object_or_404(Conference, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.conf_start_date = conference.start_date
            review.conf_end_date = conference.end_date
            try:
                review.save()
            except IntegrityError:
                form.add_error(None, "Вы уже оставляли отзыв на эту конференцию.")
                return render(request, 'conferences/review_form.html', {'form': form})
            return redirect('conference_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'conferences/review_form.html', {'form': form})
```

Добавление отзыва к конференции.

* Только для авторизованных.
* На сохранение дополняется служебная информация:

  * кто оставил отзыв (`user`),
  * к какой конференции (`conference`),
  * даты проведения конференции на момент отзыва.
* `IntegrityError` ловится, чтобы не дать одному и тому же пользователю оставить второй отзыв на ту же конференцию (уникальность `conference+user`).

Реализует:

* «Написание отзывов к конференциям (дата конференции, текст, рейтинг, информация о комментаторе)».

---

### Итого

* `conference_list` → список конференций + фильтр + поиск + пагинация.
* `conference_detail` → страница конференции + участники + отзывы.
* `register_for_conference` → создать/обновить свою регистрацию.
* `delete_registration` → удалить свою регистрацию.
* `add_review` → оставить отзыв с рейтингом (1–10), один раз на конференцию.

Все эти вьюхи вместе полностью покрывают функциональные требования лабораторной.
