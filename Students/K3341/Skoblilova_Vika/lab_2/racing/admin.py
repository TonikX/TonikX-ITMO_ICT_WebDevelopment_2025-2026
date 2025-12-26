"""
Админка для приложения racing.
"""
import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from .models import Team, DriverProfile, Race, Heat, HeatResult, Registration, Comment
from .forms_admin import HeatResultAdminForm


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Админка для команд."""
    list_display = ('name', 'description')
    search_fields = ('name',)


class HeatInline(admin.TabularInline):
    """Инлайн для заездов внутри гонки."""
    model = Heat
    extra = 1
    fields = ('name', 'start_time', 'laps', 'status', 'info')


class HeatResultInline(admin.TabularInline):
    """Инлайн для результатов заезда."""
    model = HeatResult
    form = HeatResultAdminForm
    extra = 0
    fields = ('driver', 'position', 'finish_time_seconds', 'status', 'notes')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Ограничиваем выбор водителей только зарегистрированными."""
        if db_field.name == "driver":
            # Получаем ID заезда из URL (при редактировании Heat)
            if request.resolver_match and 'object_id' in request.resolver_match.kwargs:
                heat_id = request.resolver_match.kwargs['object_id']
                try:
                    heat = Heat.objects.get(pk=heat_id)
                    # Получаем только зарегистрированных водителей
                    registered_drivers = Registration.objects.filter(
                        race=heat.race,
                        active=True
                    ).values_list('driver_id', flat=True)
                    
                    kwargs["queryset"] = DriverProfile.objects.filter(
                        id__in=registered_drivers
                    )
                    kwargs["help_text"] = f'Только водители, зарегистрированные на гонку "{heat.race.title}"'
                except (Heat.DoesNotExist, ValueError):
                    pass
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.action(description='Опубликовать выбранные гонки')
def make_published(modeladmin, request, queryset):
    """Действие для массовой публикации гонок."""
    queryset.update(is_published=True)


@admin.action(description='Снять с публикации выбранные гонки')
def make_unpublished(modeladmin, request, queryset):
    """Действие для снятия гонок с публикации."""
    queryset.update(is_published=False)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    """Админка для гонок."""
    list_display = ('title', 'location', 'date', 'is_published', 'registrations_count', 'heats_count')
    list_filter = ('is_published', 'date', 'location')
    search_fields = ('title', 'location')
    inlines = [HeatInline]
    actions = [make_published, make_unpublished]
    date_hierarchy = 'date'
    
    def get_queryset(self, request):
        """Добавляем аннотации для подсчета."""
        qs = super().get_queryset(request)
        return qs.annotate(
            _registrations_count=Count('registrations', distinct=True),
            _heats_count=Count('heats', distinct=True)
        )
    
    def registrations_count(self, obj):
        """Количество регистраций."""
        return obj._registrations_count
    registrations_count.short_description = 'Участников'
    registrations_count.admin_order_field = '_registrations_count'
    
    def heats_count(self, obj):
        """Количество заездов."""
        return obj._heats_count
    heats_count.short_description = 'Заездов'
    heats_count.admin_order_field = '_heats_count'


@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    """Админка для заездов."""
    list_display = ('name', 'race', 'start_time', 'laps', 'status', 'results_count', 'registered_count')
    list_filter = ('status', 'race', 'start_time')
    search_fields = ('name', 'race__title', 'info')
    date_hierarchy = 'start_time'
    inlines = [HeatResultInline]
    
    def get_queryset(self, request):
        """Добавляем аннотации."""
        qs = super().get_queryset(request)
        return qs.select_related('race').annotate(
            _results_count=Count('results', distinct=True)
        )
    
    def results_count(self, obj):
        """Количество результатов."""
        return obj._results_count
    results_count.short_description = 'Результатов'
    results_count.admin_order_field = '_results_count'
    
    def registered_count(self, obj):
        """Количество зарегистрированных на гонку."""
        count = Registration.objects.filter(race=obj.race, active=True).count()
        return f'{count} чел.'
    registered_count.short_description = 'Зарегистрировано на гонку'


@admin.action(description='Экспортировать результаты в CSV')
def export_heat_results_csv(modeladmin, request, queryset):
    """Действие для экспорта результатов заездов в CSV."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="heat_results.csv"'
    response.write('\ufeff')  # BOM для правильного отображения в Excel
    
    writer = csv.writer(response)
    writer.writerow(['Заезд', 'Водитель', 'Команда', 'Позиция', 'Время (сек)', 'Статус', 'Примечания'])
    
    for result in queryset:
        writer.writerow([
            str(result.heat),
            result.driver.full_name,
            result.driver.team.name if result.driver.team else '',
            result.position or '',
            result.finish_time_seconds or '',
            result.get_status_display(),
            result.notes
        ])
    
    return response


@admin.register(HeatResult)
class HeatResultAdmin(admin.ModelAdmin):
    """Админка для результатов заездов."""
    form = HeatResultAdminForm
    list_display = ('heat', 'driver', 'position', 'finish_time_seconds', 'status', 'is_registered')
    list_filter = ('status', 'heat__race', 'heat')
    search_fields = ('driver__full_name', 'heat__name', 'heat__race__title')
    raw_id_fields = ('heat', 'driver')
    actions = [export_heat_results_csv]
    
    def is_registered(self, obj):
        """Проверка, зарегистрирован ли водитель на гонку."""
        is_reg = Registration.objects.filter(
            driver=obj.driver,
            race=obj.heat.race,
            active=True
        ).exists()
        if is_reg:
            return '✓ Да'
        return '✗ НЕТ'
    is_registered.short_description = 'Зарегистрирован'
    is_registered.boolean = False
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Ограничиваем выбор водителей только зарегистрированными."""
        if db_field.name == "driver":
            # При редактировании существующего результата
            if request.resolver_match and 'object_id' in request.resolver_match.kwargs:
                result_id = request.resolver_match.kwargs['object_id']
                try:
                    result = HeatResult.objects.get(pk=result_id)
                    heat = result.heat
                    
                    registered_drivers = Registration.objects.filter(
                        race=heat.race,
                        active=True
                    ).values_list('driver_id', flat=True)
                    
                    kwargs["queryset"] = DriverProfile.objects.filter(
                        id__in=registered_drivers
                    )
                    kwargs["help_text"] = f'Только водители, зарегистрированные на "{heat.race.title}"'
                except (HeatResult.DoesNotExist, ValueError):
                    pass
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    """Админка для профилей водителей."""
    list_display = ('full_name', 'user', 'driver_class', 'team', 'experience_years')
    list_filter = ('driver_class', 'team')
    search_fields = ('full_name', 'user__username', 'user__email')
    raw_id_fields = ('user',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Админка для регистраций."""
    list_display = ('driver', 'race', 'car_number', 'created_at', 'active')
    list_filter = ('active', 'race', 'created_at')
    search_fields = ('driver__full_name', 'race__title')
    raw_id_fields = ('driver', 'race')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""
    list_display = ('author', 'race', 'kind', 'rating', 'heat_date', 'created_at')
    list_filter = ('kind', 'rating', 'heat_date', 'created_at')
    search_fields = ('author__username', 'race__title', 'text')
    raw_id_fields = ('author', 'race')
    date_hierarchy = 'created_at'

