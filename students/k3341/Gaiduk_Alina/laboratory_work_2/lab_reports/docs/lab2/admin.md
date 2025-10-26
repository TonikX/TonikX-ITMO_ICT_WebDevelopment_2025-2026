# Django admin (приложение `conferences`)


## TopicAdmin

```
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("name",)
```

Админка для тематик конференций. Можно искать тему по названию.

## PlaceAdmin

```
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address", "description")
```

Отображает список площадок (мест проведения) с названием и адресом. Есть поиск по названию, адресу и описанию.

## ConferenceAdmin

```
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "place", "start_date", "end_date")
    list_filter = ("start_date", "end_date", "topics", "place")
    search_fields = ("title", "description", "participation_terms", "place__name")
    filter_horizontal = ("topics",)
```

Управление конференциями:

* таблица показывает название, место и даты;
* фильтрация по датам, темам и месту;
* поиск по названию, описанию и условиям участия;
* удобный выбор тематик через `filter_horizontal`.

Это отвечает за наполнение каталога конференций.

## RegistrationAdmin

```
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "presentation_title", "result", "created")
    list_filter = ("result", "conference")
    search_fields = ("user__username", "presentation_title", "conference__title")
    list_editable = ("result",)
```

Заявки докладчиков:

* выводятся пользователь, конференция, тема доклада, статус, дата подачи;
* можно фильтровать по статусу и конференции;
* поиск по автору и названию доклада;
* самое главное — поле `result` редактируется прямо из списка.

Это закрывает требование лабораторной:

> администратор должен иметь возможность указания результата выступления (“рекомендован к публикации / не рекомендован”).

## ReviewAdmin

```
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("conference", "user", "rating", "date_posted")
    list_filter = ("rating", "conference")
    search_fields = ("user__username", "conference__title", "text")
```

Отзывы к конференциям:

* отображаются конференция, автор, рейтинг и когда оставлен отзыв;
* можно фильтровать по рейтингу и конференции;
* поиск по тексту отзыва и пользователю.

---

## Итог

`admin.py` настраивает удобную админку для всех ключевых сущностей:

* темы,
* места,
* конференции,
*
