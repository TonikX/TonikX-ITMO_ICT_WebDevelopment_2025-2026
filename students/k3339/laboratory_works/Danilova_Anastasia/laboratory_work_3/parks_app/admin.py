from django.contrib import admin
from .models import Services, Enterprise, Object, Contract, Decorator, ObjectZone, Plant, \
    PlantPlacement, LifeForm, Species, PlantWateringSchedule, Worker, PlantWorkerAssignment, ObjectWorkerAssignment


# Register your models here.

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "legal_address", "ogrn")
    search_fields = ("name", "legal_address", "ogrn")


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_serviced_display")
    search_fields = ("name",)
    list_filter = ("contracts__is_active",)

    def is_serviced_display(self, obj):
        return obj.is_serviced

    is_serviced_boolean = True
    is_serviced_display.short_description = "Is Serviced"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "enterprise_id", "object_id", "contract_number", "contract_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("enterprise__name", "object__name", "contract_number", "contract_date",)


@admin.register(Decorator)
class DecoratorAdmin(admin.ModelAdmin):
    list_display = ("id", "short_name", "phone_number", "education", "category", "phone_number")
    list_filter = ("category",)
    search_fields = ("phone_number", "graduated_from", "first_name", "last_name", "middle_name",)

    def full_name(self, obj):
        return obj.full_name

    full_name.admin_order_field = "last_name"


@admin.register(ObjectZone)
class ObjectZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "object_id", "number",)
    search_fields = ("object_id__name", "number",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("id", "initial_age", "get_species_name", "get_life_form", "current_age")
    list_filter = ("species__life_form", "species", "initial_age")
    search_fields = ("species__name", "description", "species__life_form__name")

    def get_species_name(self, obj):
        return obj.species.name if obj.species else "-"

    get_species_name.admin_order_field = "species__name"  # for sorting

    def get_life_form(self, obj):
        return obj.species.life_form.name if obj.species and obj.species.life_form else "-"

    get_life_form.admin_order_field = "species__life_form__name"


@admin.register(PlantPlacement)
class PlantPlacementAdmin(admin.ModelAdmin):
    list_display = ("id", "plant_id", "zone_id", "unique_number", "planted_date")
    list_filter = ("planted_date",)
    search_fields = ("planted_date", "plant__species__name", "zone__object_id__name",)


@admin.register(LifeForm)
class LifeFormAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("possible_planting_period_from", "possible_planting_period_to", "flowering_period_from",
                   "flowering_period_to")
    search_fields = ("name", "life_form__name",)

@admin.register(PlantWateringSchedule)
class PlantWateringScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "plant_id", "frequency", "watering_time_period", "current_water_norm_liters")
    list_filter = ("plant_id", "time_watering_end", "time_watering_start",)
    search_fields = ("plant__species__name", )

    def get_current_water_norm_liters(self, obj):
        return obj.current_water_norm_liters

    get_current_water_norm_liters.admin_order_field = "current_water_norm_liters"

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "short_name", "phone_number", "address")
    search_fields = ("phone_number", "address", "first_name", "last_name",)

    def get_full_name(self, obj):
        return obj.full_name

    get_full_name.admin_order_field = "full_name"

@admin.register(PlantWorkerAssignment)
class PlantWorkerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "plant_id", "worker_id", "date")
    list_filter = ("date",)
    search_fields = ("plant__species__name", "worker__first_name", "worker__last_name", "worker__middle_name",)

    def get_full_name(self, obj):
        return obj.full_name

    get_full_name.admin_order_field = "full_name"

@admin.register(ObjectWorkerAssignment)
class ObjectWorkerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("object_id", "worker_id", "start_date", "end_date")
    list_filter = ("start_date", "end_date",)
    search_fields = ("worker__first_name", "worker__last_name", "object__name", "object__address")


