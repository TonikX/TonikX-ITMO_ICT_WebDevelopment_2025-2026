from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from .models import Hotel, RoomType, Room, Reservation, Review

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    actions = ['make_staff', 'remove_staff']
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} пользователей назначены персоналом', messages.SUCCESS)
    make_staff.short_description = "Назначить выбранных пользователей персоналом"
    
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} пользователей сняты с персонала', messages.SUCCESS)
    remove_staff.short_description = "Снять выбранных пользователей с персонала"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address']
    list_filter = ['owner']
    search_fields = ['name', 'owner', 'address']

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'price', 'capacity']
    list_filter = ['hotel', 'capacity']
    search_fields = ['name', 'hotel__name']
    

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'type', 'type__hotel']
    list_filter = ['type', 'type__hotel']
    search_fields = ['number', 'type__name']
    
    def hotel(self, obj):
        return obj.type.hotel.name
    hotel.short_description = 'Отель'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'check_in', 'check_out', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'room__type__hotel']
    search_fields = ['user__first_name', 'user__last_name', 'room__number', 'room__type__name']
    list_editable = ['status']
    
    actions = ['check_in_guests', 'check_out_guests', 'cancel_reservations']
    
    def check_in_guests(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='checked_in')
        self.message_user(request, f'{updated} гостей заселено', messages.SUCCESS)
    check_in_guests.short_description = "Заселить выбранных гостей"
    
    def check_out_guests(self, request, queryset):
        updated = queryset.filter(status='checked_in').update(status='checked_out')
        self.message_user(request, f'{updated} гостей выселено', messages.SUCCESS)
    check_out_guests.short_description = "Выселить выбранных гостей"
    
    def cancel_reservations(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='cancelled')
        self.message_user(request, f'{updated} бронирований отменено', messages.SUCCESS)
    cancel_reservations.short_description = "Отменить выбранные бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['get_guest_name', 'get_hotel_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reservation__user__first_name', 'reservation__user__last_name', 'reservation__room__type__hotel__name']
    
    def get_guest_name(self, obj):
        return obj.reservation.user.username
    get_guest_name.short_description = 'Гость'
    
    def get_hotel_name(self, obj):
        return obj.reservation.room.type.hotel.name
    get_hotel_name.short_description = 'Отель'


admin.site.site_header = "HotelSystem - Администрирование отелей"
admin.site.site_title = "HotelSystem Admin"
admin.site.index_title = "Панель управления отелями"