from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from .models import (
    AdminUser, Client, Car, CarSpecification, Fleet, CarFleet,
    Lease, LeaseApplication, Maintenance, MaintenanceCompany
)

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = AdminUser
        fields = ('id','username','email','first_name','last_name','phone','position')


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = AdminUser
        fields = ('id','username', "password", 'email','first_name','last_name','phone','position')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id", "company_name", "inn", "email",
            "phone", "address", "contact_person",
            "created_at", "is_active",
        ]
        read_only_fields = ["id", "created_at"]


class CarSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSpecification
        fields = "__all__"


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ["id", "name", "address", "created_at"]


class CarFleetSerializer(serializers.ModelSerializer):
    fleet = serializers.PrimaryKeyRelatedField(
        queryset=Fleet.objects.all()
    )
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all()
    )

    class Meta:
        model = CarFleet
        fields = ["id", "car", "fleet", "assigned_at"]
        read_only_fields = ["id"]


class CarSerializer(serializers.ModelSerializer):
    specification = CarSpecificationSerializer(required=False, read_only=True)
    class Meta:
        model = Car
        fields = [
            "id", "make", "model", "year", "vin",
            "license_plate", "status", "current_mileage", "created_at",
            "specification"
        ]
{
  "make": "toyota",
  "model": "3",
  "year": 2020,
  "vin": "3",
  "license_plate": "3",
  "status": "available",
  "current_mileage": 0
}
{
"lease_id": 1,
  "start_date": "2025-05-05",
  "end_date": "2025-10-05",
  "monthly_payment": "100",
  "status": "active",
  "created_by_admin": 0
}

class CarDetailSerializer(serializers.ModelSerializer):
    specification = CarSpecificationSerializer(required=False, read_only=True)
    car_fleet = CarFleetSerializer(required=False, read_only=True)

    class Meta:
        model = Car
        fields = [
            "id", "vin", "make", "model", "year",
            "license_plate", "status", "current_mileage",
            "purchase_date", "created_at",
            "specification", "car_fleet",
        ]

class MaintenanceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceCompany
        fields = ["id", "name", "phone", "address", "created_at"]



class MaintenanceSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    maintenance_company = serializers.PrimaryKeyRelatedField(
        queryset=MaintenanceCompany.objects.all()
    )

    class Meta:
        model = Maintenance
        fields = [
            "id", "car", "maintenance_company", "date",
            "service", "cost", "description",
            "created_by_admin", "created_at"
        ]



class LeaseSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Lease
        fields = [
            "id", "car", "client",
            "start_date", "end_date",
            "monthly_payment", "status",
            "created_by_admin", "created_at"
        ]



class LeaseStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = [
            "car",
            "client",
            "start_date",
            "end_date",
            "monthly_payment",
            "status",
        ]


class LeaseApplicationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = LeaseApplication
        fields = ["id", "car", "client", "created_at"]


class PublicLeaseApplicationSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    inn = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    contact_person = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_inn(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("ИНН некорректный")
        return value
