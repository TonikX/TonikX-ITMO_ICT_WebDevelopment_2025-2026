from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'aircraft_count', 'employee_count']
    search_fields = ['name', 'code']
    list_per_page = 20
    
    def aircraft_count(self, obj):
        return obj.aircraft_set.count()
    aircraft_count.short_description = 'Кол-во самолетов'
    
    def employee_count(self, obj):
        return obj.employee_set.count()
    employee_count.short_description = 'Кол-во сотрудников'


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ['tail_number', 'aircraft_type', 'company', 'capacity', 
                    'speed', 'status', 'flight_count']
    list_filter = ['company', 'status', 'aircraft_type']
    search_fields = ['tail_number', 'aircraft_type']
    list_editable = ['status']
    list_per_page = 30
    
    def flight_count(self, obj):
        return obj.flight_set.count()
    flight_count.short_description = 'Рейсов'


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'departure_count', 'arrival_count']
    search_fields = ['code', 'name', 'city']
    list_per_page = 30
    
    def departure_count(self, obj):
        return obj.departures.count()
    departure_count.short_description = 'Вылетов'
    
    def arrival_count(self, obj):
        return obj.arrivals.count()
    arrival_count.short_description = 'Прилетов'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'company', 'position_display', 
                    'age', 'experience', 'is_active', 'crew_status']
    list_filter = ['company', 'position', 'is_active']
    search_fields = ['last_name', 'first_name', 'passport']
    list_editable = ['is_active']
    list_per_page = 50
    
    def position_display(self, obj):
        return dict(Employee.POSITION_CHOICES).get(obj.position, obj.position)
    position_display.short_description = 'Должность'
    
    def crew_status(self, obj):
        crews = CrewMember.objects.filter(employee=obj)
        if not crews.exists():
            return "Не в экипаже"
        
        active_crews = crews.filter(crew__is_active=True)
        if active_crews.exists():
            crew_names = ", ".join([cm.crew.name for cm in active_crews])
            return f"В экипаже: {crew_names}"
        return "В неактивном экипаже"
    crew_status.short_description = 'Статус в экипаже'


class CrewMemberInline(admin.TabularInline):
    model = CrewMember
    extra = 1
    autocomplete_fields = ['employee']


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_active', 'member_count', 
                    'flight_count', 'created_at']
    list_filter = ['company', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']
    inlines = [CrewMemberInline]
    list_per_page = 30
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Членов'
    
    def flight_count(self, obj):
        return obj.flights.count()
    flight_count.short_description = 'Рейсов'


class TransitStopInline(admin.TabularInline):
    model = TransitStop
    extra = 0
    autocomplete_fields = ['airport']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'route_display', 'departure_datetime', 
                    'arrival_datetime', 'aircraft', 'load_percentage_display', 
                    'crew_display', 'tickets_sold']
    list_filter = ['departure_airport', 'arrival_airport', 'aircraft__company',
                   'departure_datetime']
    search_fields = ['flight_number']
    date_hierarchy = 'departure_datetime'
    autocomplete_fields = ['departure_airport', 'arrival_airport', 'aircraft', 'crew']
    inlines = [TransitStopInline]
    list_per_page = 50
    readonly_fields = ['duration_display']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('flight_number', 'distance', 'departure_airport', 
                      'arrival_airport', 'aircraft', 'crew')
        }),
        ('Время', {
            'fields': ('departure_datetime', 'arrival_datetime', 'duration_display')
        }),
        ('Билеты', {
            'fields': ('tickets_sold',)
        }),
    )
    
    def route_display(self, obj):
        return f"{obj.departure_airport.code} → {obj.arrival_airport.code}"
    route_display.short_description = 'Маршрут'
    
    def load_percentage_display(self, obj):
        if obj.aircraft and obj.aircraft.capacity > 0:
            percentage = (obj.tickets_sold / obj.aircraft.capacity) * 100
            
            if percentage >= 90:
                color = 'red'
            elif percentage >= 70:
                color = 'orange'
            elif percentage >= 50:
                color = 'yellow'
            else:
                color = 'green'
            percentage_str = f"{percentage:.1f}%"
            
            return format_html(
                '<span style="color: {};">{} ({}/{})</span>',
                color, percentage_str, obj.tickets_sold, obj.aircraft.capacity
            )
        return '—'
    load_percentage_display.short_description = 'Загрузка'
    
    def crew_display(self, obj):
        if obj.crew:
            return format_html(
                '<a href="/admin/your_app/crew/{}/change/">{}</a>',
                obj.crew.id, obj.crew.name
            )
        return '—'
    crew_display.short_description = 'Экипаж'
    
    def duration_display(self, obj):
        if obj.departure_datetime and obj.arrival_datetime:
            duration = obj.arrival_datetime - obj.departure_datetime
            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() % 3600) // 60
            return f"{int(hours)} ч {int(minutes)} мин"
        return '—'
    duration_display.short_description = 'Длительность полета'


@admin.register(TransitStop)
class TransitStopAdmin(admin.ModelAdmin):
    list_display = ['flight', 'airport', 'arrival_datetime', 'departure_datetime', 
                    'stop_duration']
    list_filter = ['airport', 'flight']
    autocomplete_fields = ['flight', 'airport']
    list_per_page = 30
    
    def stop_duration(self, obj):
        if obj.arrival_datetime and obj.departure_datetime:
            duration = obj.departure_datetime - obj.arrival_datetime
            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() % 3600) // 60
            return f"{int(hours)} ч {int(minutes)} мин"
        return '—'
    stop_duration.short_description = 'Время стоянки'


admin.site.site_header = 'Администрирование авиакомпании'
admin.site.site_title = 'Авиакомпания'
admin.site.index_title = 'Управление данными авиакомпании'