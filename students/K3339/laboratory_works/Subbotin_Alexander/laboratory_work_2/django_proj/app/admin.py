from django.contrib import admin
from .models import Tour, Reservation, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency', 'city', 'start_date', 'end_date', 'price')
    search_fields = ('title', 'agency', 'city')
    list_filter = ('city', 'agency')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'user', 'guests', 'confirmed', 'created_at')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('user__username', 'tour__title')
    actions = ['confirm_reservations']


    def confirm_reservations(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, f"{updated} reservation(s) confirmed.")

    confirm_reservations.short_description = 'Confirm selected reservations'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'created_at')
    search_fields = ('tour__title', 'user__username')