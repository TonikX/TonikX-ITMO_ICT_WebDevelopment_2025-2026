from django.contrib import admin
from .models import User, Race, Racer, RaceResult, Comment


# ===== АДМИН-ПАНЕЛЬ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ =====
class UserAdmin(admin.ModelAdmin):
    """Кастомная админка для модели User"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality')
    list_filter = ('nationality',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'passport_number')

    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )


# ===== АДМИН-ПАНЕЛЬ ДЛЯ ГОНОК =====
class RaceAdmin(admin.ModelAdmin):
    """Админка для гонок"""
    list_display = ('name', 'date', 'location', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('name', 'location', 'description')
    date_hierarchy = 'date'  # Навигация по датам в админке


# ===== АДМИН-ПАНЕЛЬ ДЛЯ ГОНЩИКОВ =====
class RacerAdmin(admin.ModelAdmin):
    """Админка для регистраций гонщиков"""
    list_display = ('user', 'race', 'team_name', 'experience', 'racer_class', 'registered_at')
    list_filter = ('experience', 'racer_class', 'race')
    search_fields = ('user__username', 'team_name', 'car_description')
    raw_id_fields = ('user', 'race')  # Оптимизация для ForeignKey


# ===== АДМИН-ПАНЕЛЬ ДЛЯ РЕЗУЛЬТАТОВ =====
class RaceResultAdmin(admin.ModelAdmin):
    """Админка для результатов гонок"""
    list_display = ('racer', 'race_time', 'result', 'created_at')
    list_filter = ('result', 'created_at')
    search_fields = ('racer__user__username', 'result', 'notes')
    raw_id_fields = ('racer',)

    def get_queryset(self, request):
        """Оптимизация запросов с select_related"""
        return super().get_queryset(request).select_related('racer__user', 'racer__race')


# ===== АДМИН-ПАНЕЛЬ ДЛЯ КОММЕНТАРИЕВ =====
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев"""
    list_display = ('user', 'race', 'comment_type', 'rating', 'created_at')
    list_filter = ('comment_type', 'rating', 'created_at')
    search_fields = ('text', 'user__username', 'race__name')
    raw_id_fields = ('user', 'race')


# ===== РЕГИСТРАЦИЯ МОДЕЛЕЙ В АДМИНКЕ =====
admin.site.register(User, UserAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Racer, RacerAdmin)
admin.site.register(RaceResult, RaceResultAdmin)
admin.site.register(Comment, CommentAdmin)
