from django.contrib import admin
from .models import (
    BusType,
    Bus,
    Route,
    Driver,
    DriverAssignment,
    BusStatus,
)

admin.site.register(BusType)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Driver)
admin.site.register(DriverAssignment)
admin.site.register(BusStatus)
