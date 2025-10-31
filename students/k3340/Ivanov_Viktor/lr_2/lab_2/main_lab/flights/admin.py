from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Flight, Reservation, Review


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """кастомная админка для расширенной модели пользователя"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone_number', 'passport_number', 'date_of_birth')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 
                      'passport_number', 'date_of_birth')
        }),
    )


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """админка для рейсов"""
    
    list_display = (
        'flight_number', 
        'airline', 
        'departure_city', 
        'arrival_city', 
        'departure_time', 
        'flight_type', 
        'gate_number',
        'available_seats_display'
    )
    list_filter = ('flight_type', 'airline', 'departure_city', 'arrival_city')
    search_fields = ('flight_number', 'airline', 'departure_city', 'arrival_city')
    ordering = ('-departure_time',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('flight_number', 'airline', 'flight_type')
        }),
        ('Маршрут', {
            'fields': ('departure_city', 'arrival_city', 'departure_time', 'arrival_time')
        }),
        ('Дополнительно', {
            'fields': ('gate_number', 'total_seats', 'price')
        }),
    )
    
    def available_seats_display(self, obj):
        return f"{obj.available_seats}/{obj.total_seats}"
    available_seats_display.short_description = 'Свободных мест'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """админка для резервирований"""
    
    list_display = (
        'id',
        'user',
        'flight',
        'ticket_number',
        'seat_number',
        'status',
        'is_confirmed',
        'created_at'
    )
    list_filter = ('status', 'is_confirmed', 'created_at')
    search_fields = ('user__username', 'flight__flight_number', 'ticket_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'flight')
        }),
        ('Детали резервирования', {
            'fields': ('ticket_number', 'seat_number', 'status', 'is_confirmed')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['confirm_reservations', 'cancel_reservations']
    
    def confirm_reservations(self, request, queryset):
        """подтвердить выбранные резервирования"""
        updated = queryset.update(is_confirmed=True, status='confirmed')
        self.message_user(request, f'Подтверждено резервирований: {updated}')
    confirm_reservations.short_description = 'Подтвердить выбранные резервирования'
    
    def cancel_reservations(self, request, queryset):
        """отменить выбранные резервирования"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'Отменено резервирований: {updated}')
    cancel_reservations.short_description = 'Отменить выбранные резервирования'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """админка для отзывов"""
    
    list_display = (
        'id',
        'user',
        'flight',
        'rating',
        'flight_date',
        'created_at',
        'text_preview'
    )
    list_filter = ('rating', 'created_at', 'flight_date')
    search_fields = ('user__username', 'flight__flight_number', 'text')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'flight', 'flight_date', 'rating')
        }),
        ('Отзыв', {
            'fields': ('text',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def text_preview(self, obj):
        """предпросмотр текста отзыва"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст отзыва'
