from django.contrib import admin
from .models import (
    Breed, Diet, BreedDiet,
    Hen, HenEggs, Cage, HenCage,
    Employee, EmployeeCage, Employment
)

# =============== ПОРДЫ И ДИЕТЫ ===============

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'efficiency', 'mean_weight', 'hens_count')
    search_fields = ('name',)
    readonly_fields = ('hens_count',)

    def hens_count(self, obj):
        return obj.hens.count()
    hens_count.short_description = 'Количество кур'

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('number', 'structure_preview', 'breeds_count')
    search_fields = ('number', 'structure')
    readonly_fields = ('breeds_count',)

    def structure_preview(self, obj):
        return (obj.structure[:60] + '...') if len(obj.structure) > 60 else obj.structure
    structure_preview.short_description = 'Описание'

    def breeds_count(self, obj):
        return obj.breeds.count()
    breeds_count.short_description = 'Пород на диете'

class BreedDietInline(admin.TabularInline):
    model = BreedDiet
    extra = 1

@admin.register(BreedDiet)
class BreedDietAdmin(admin.ModelAdmin):
    list_display = ('breed', 'diet', 'season')
    list_filter = ('season', 'breed', 'diet')
    search_fields = ('breed__name', 'diet__number')

# =============== КУРИЦЫ И КЛЕТКИ ===============

class HenEggsInline(admin.TabularInline):
    model = HenEggs
    extra = 0
    readonly_fields = ('date',)
    can_delete = True

class HenCageInline(admin.TabularInline):
    model = HenCage
    extra = 0
    readonly_fields = ('date_start', 'date_end')
    can_delete = False  # удаление разрешено только через API/логику

@admin.register(Hen)
class HenAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed', 'weight', 'birth_date', 'death_date', 'is_alive')
    list_filter = ('breed', 'death_date', 'birth_date')
    search_fields = ('breed__name',)
    date_hierarchy = 'birth_date'
    inlines = [HenEggsInline, HenCageInline]
    readonly_fields = ('is_alive',)

    def is_alive(self, obj):
        return obj.death_date is None
    is_alive.boolean = True
    is_alive.short_description = 'Жива?'

@admin.register(Cage)
class CageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hens_count', 'employees_count')
    list_filter = ('workshop_number',)
    search_fields = ('workshop_number', 'row_number', 'in_row_number')
    readonly_fields = ('hens_count', 'employees_count')

    def hens_count(self, obj):
        today = admin.utils.timezone.now().date()
        return obj.hen_cages.filter(
            date_start__lte=today
        ).filter(
            admin.models.Q(date_end__isnull=True) | admin.models.Q(date_end__gte=today)
        ).count()
    hens_count.short_description = 'Текущих кур'

    def employees_count(self, obj):
        today = admin.utils.timezone.now().date()
        return obj.employee_cages.filter(
            date_start__lte=today
        ).filter(
            admin.models.Q(date_end__isnull=True) | admin.models.Q(date_end__gte=today)
        ).count()
    employees_count.short_description = 'Текущих работников'

# =============== СОТРУДНИКИ ===============

class EmploymentInline(admin.TabularInline):
    model = Employment
    extra = 0
    readonly_fields = ('date_start', 'date_end')
    can_delete = False

class EmployeeCageInline(admin.TabularInline):
    model = EmployeeCage
    extra = 0
    readonly_fields = ('date_start', 'date_end')
    can_delete = False

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_series', 'passport_number', 'active_employment')
    search_fields = ('full_name', 'passport_series', 'passport_number')
    inlines = [EmploymentInline, EmployeeCageInline]
    readonly_fields = ('active_employment',)

    def active_employment(self, obj):
        return obj.employments.filter(date_end__isnull=True).exists()
    active_employment.boolean = True
    active_employment.short_description = 'Работает?'

# =============== ИСТОРИЯ РАЗМЕЩЕНИЯ ===============

@admin.register(HenCage)
class HenCageAdmin(admin.ModelAdmin):
    list_display = ('hen', 'cage', 'date_start', 'date_end', 'is_current')
    list_filter = ('cage__workshop_number', 'date_start', 'hen__breed')
    search_fields = ('hen__id', 'cage__workshop_number')
    date_hierarchy = 'date_start'

    def is_current(self, obj):
        today = admin.utils.timezone.now().date()
        return obj.date_end is None or obj.date_end >= today
    is_current.boolean = True
    is_current.short_description = 'Текущее?'

@admin.register(EmployeeCage)
class EmployeeCageAdmin(admin.ModelAdmin):
    list_display = ('employee', 'cage', 'date_start', 'date_end', 'is_current')
    list_filter = ('cage__workshop_number', 'employee', 'date_start')
    search_fields = ('employee__full_name', 'cage__workshop_number')
    date_hierarchy = 'date_start'

    def is_current(self, obj):
        today = admin.utils.timezone.now().date()
        return obj.date_end is None or obj.date_end >= today
    is_current.boolean = True
    is_current.short_description = 'Текущее?'

# =============== ТРУДОУСТРОЙСТВО ===============

@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position', 'contract', 'date_start', 'date_end', 'is_active')
    list_filter = ('position', 'date_start', 'date_end')
    search_fields = ('employee__full_name', 'contract')
    date_hierarchy = 'date_start'

    def is_active(self, obj):
        return obj.date_end is None
    is_active.boolean = True
    is_active.short_description = 'Активно?'

# =============== ЯЙЦЕНОСКОСТЬ ===============

@admin.register(HenEggs)
class HenEggsAdmin(admin.ModelAdmin):
    list_display = ('hen', 'count_eggs', 'date')
    list_filter = ('date', 'hen__breed')
    search_fields = ('hen__id',)
    date_hierarchy = 'date'