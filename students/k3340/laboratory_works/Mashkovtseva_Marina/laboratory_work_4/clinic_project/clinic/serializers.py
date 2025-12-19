from rest_framework import serializers
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment

class PatientSerializer(serializers.ModelSerializer):
    medical_record_id = serializers.IntegerField(
        source="medical_record.id",
        read_only=True
    )

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
    doctor_detail = DoctorSerializer(source="doctor", read_only=True)
    room_detail = RoomSerializer(source="room", read_only=True)
    is_paid = serializers.BooleanField(read_only=True)

    record_id = serializers.PrimaryKeyRelatedField(
        queryset=MedicalRecord.objects.all(),
        source="record",
        write_only=True
    )

    class Meta:
        model = Visit
        fields = [
            "id",
            "record",
            "record_id",
            "doctor",
            "doctor_detail",
            "room",
            "room_detail",
            "visit_datetime",
            "diagnosis",
            "patient_condition",
            "recommendations",
            "price",
            "is_paid",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    visit = VisitSerializer(read_only=True)
    visit_id = serializers.PrimaryKeyRelatedField(
        queryset=Visit.objects.all(),
        source="visit",
        write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "visit",
            "visit_id",
            "payment_datetime",
            "payment_method",
            "amount",
        ]
        read_only_fields = ["amount"]

    def create(self, validated_data):
        visit = validated_data["visit"]
        validated_data["amount"] = visit.price
        return super().create(validated_data)

