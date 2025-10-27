# Формы приложения `conferences`

## RegistrationForm

```
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['presentation_title', 'abstract']
        widgets = {
            'presentation_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название доклада',
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'input textarea',
                'rows': 6,
                'placeholder': 'Тезисы…',
                'style': 'resize:none;',
            }),
        }
```

**Назначение:** форма для подачи заявки на участие/выступление в конференции.

**Что заполняет пользователь:**

* `presentation_title` — название доклада;
* `abstract` — краткие тезисы.

**Что не даём менять пользователю:**

* `user`, `conference`, `result`, `created` заполняются автоматически во вьюхе.
  Это не даёт подделать владельца заявки или статус модерации.

---

## ReviewForm

```
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10, help_text="Оценка 1–10")

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Ваш отзыв…",
                "style": "resize:none;",
            })
        }
```

**Назначение:** форма для добавления отзыва о конференции.

**Что вводит пользователь:**

* `text` — текст отзыва;
* `rating` — оценка конференции (1–10), проверяется валидатором `min_value` / `max_value`.

**Остальное (автор отзыва, дата проведения конференции, дата публикации):**

* проставляется автоматически перед сохранением.

---

## Итог

* `RegistrationForm` — регистрация докладчика на конференцию.
* `ReviewForm` — отзыв и рейтинг по конференции.
  Обе формы основаны на `ModelForm` и сразу пишут валидные данные в базу.
