from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Reservation, Review, Tour


class TourAdminForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label="Фото")
    clear_image = forms.BooleanField(required=False, label="Удалить фото")

    class Meta:
        model = Tour
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.image:
            self.fields["image_file"].help_text = "Загрузите новый файл, чтобы заменить текущее фото."
        else:
            self.fields["clear_image"].widget = forms.HiddenInput()

    def save(self, commit=True):
        image_file = self.cleaned_data.pop("image_file", None)
        clear_image = self.cleaned_data.pop("clear_image", False)
        if clear_image:
            self.instance.image = None
            self.instance.image_mime = ""
        elif image_file:
            self.instance.image = image_file.read()
            self.instance.image_mime = image_file.content_type or "image/jpeg"
        return super().save(commit=commit)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    form = TourAdminForm
    list_display = ("name", "agency", "country", "start_date", "end_date")
    search_fields = ("name", "agency", "country")
    list_filter = ("country", "start_date")
    readonly_fields = ("image_preview",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "agency",
                    "description",
                    "country",
                    ("start_date", "end_date"),
                    "payment_terms",
                )
            },
        ),
        ("Фото", {"fields": ("image_preview", "image_file", "clear_image")}),
    )

    def image_preview(self, obj):
        if obj.image_data_url:
            return format_html('<img src="{}" style="max-width:200px;">', obj.image_data_url)
        return "нет"
    image_preview.short_description = "Текущее фото"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("tour", "user", "status", "travel_start", "travel_end", "reserved_at")
    list_filter = ("status", "tour__country")
    search_fields = ("tour__name", "user__username")
    autocomplete_fields = ("tour", "user")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("tour", "author", "rating", "created_at")
    list_filter = ("rating", "tour__country")
    search_fields = ("tour__name", "author__username", "text")
