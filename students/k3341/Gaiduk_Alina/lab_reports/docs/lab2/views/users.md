# Views приложения `users`

## `register`

```
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт создан. Теперь войдите.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
```

Регистрация нового пользователя.

* Если `POST`: берётся `RegisterForm`, проверяется валидность, создаётся новый `User`.
* После успешной регистрации показывается сообщение и идёт редирект на страницу логина.
* Если `GET`: просто отрисовывается форма.
* Это покрывает требование лабораторной «Регистрация новых пользователей».

## `profile`

```
@login_required
def profile(request):
    regs = (
        Registration.objects
        .filter(user=request.user)
        .select_related("conference", "conference__place")
        .order_by("-created")
    )

    reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related("conference")
        .order_by("-date_posted")
    )

    return render(
        request,
        "users/profile.html",
        {
            "regs": regs,
            "reviews": reviews,
        },
    )
```

Личный кабинет пользователя.

* `login_required`: доступ только после входа.
* `regs`: все регистрации текущего пользователя на конференции (с конференцией, местом проведения, статусом). Новые сверху.
* `reviews`: все отзывы пользователя по конференциям. Новые сверху.
* Страница `profile.html` показывает пользователю его активность: где он выступает и какие отзывы оставил.
