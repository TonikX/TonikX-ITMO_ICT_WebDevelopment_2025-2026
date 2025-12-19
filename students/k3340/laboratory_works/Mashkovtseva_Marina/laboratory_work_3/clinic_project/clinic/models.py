from django.db import models
from django.conf import settings


class Patient(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    passport_data = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Пациент: {self.last_name} {self.first_name}"

class Doctor(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100)
    education = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    work_start_date = models.DateField()
    work_end_date = models.DateField(blank=True, null=True)
    contract_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Врач: {self.last_name} {self.first_name} — {self.specialty}"

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    work_date = models.DateField()
    is_working = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'work_date')

    def __str__(self):
        return f"График: {self.doctor} — {self.work_date} ({'рабочий день' if self.is_working else 'выходной'})"

class Room(models.Model):
    room_number = models.CharField(max_length=20)
    work_time_start = models.TimeField()
    work_time_end = models.TimeField()
    responsible_person = models.CharField(max_length=100, blank=True, null=True)
    internal_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Кабинет №{self.room_number}"

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_record')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Медицинская карта пациента: {self.patient}"

class Visit(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='visits')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits')
    visit_datetime = models.DateTimeField()
    diagnosis = models.TextField(blank=True, null=True)
    patient_condition = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Приём №{self.id} — {self.record.patient} ({self.visit_datetime})"

class Payment(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='payment')
    payment_datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Оплата №{self.id} за приём №{self.visit_id}"
