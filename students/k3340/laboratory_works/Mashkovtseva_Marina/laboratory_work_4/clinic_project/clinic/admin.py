from django.contrib import admin
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(DoctorSchedule)
admin.site.register(Room)
admin.site.register(MedicalRecord)
admin.site.register(Visit)
admin.site.register(Payment)
