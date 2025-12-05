from rest_framework import serializers
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = "__all__"

class VisitSerializer(serializers.ModelSerializer):
    record = MedicalRecordSerializer(read_only=True)
    record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='record', write_only=True)
    class Meta:
        model = Visit
        fields = ["id","record","record_id","doctor","room","visit_datetime","diagnosis","patient_condition","recommendations","price"]

class PaymentSerializer(serializers.ModelSerializer):
    visit = VisitSerializer(read_only=True)
    visit_id = serializers.PrimaryKeyRelatedField(queryset=Visit.objects.all(), source='visit', write_only=True)
    class Meta:
        model = Payment
        fields = ["id","visit","visit_id","payment_datetime","amount","payment_method"]
