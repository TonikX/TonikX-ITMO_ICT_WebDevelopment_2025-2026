from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт создан! Теперь можно войти.")
            return redirect("login")
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = UserCreationForm()

    for f in form.fields.values():
        f.widget.attrs.update({"class": "form-control"})

    return render(request, "registration/signup.html", {"form": form})