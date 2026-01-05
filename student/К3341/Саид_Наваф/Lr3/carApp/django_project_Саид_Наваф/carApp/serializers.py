# app/serializers.py
from rest_framework import serializers
from .models import Owner, OwnerContact, DriverLicense, VehicleModel, Car, Ownership, InsurancePolicy, ServiceRecord, Registration

class OwnerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerContact
        fields = '__all__'

class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = '__all__'

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'

class CarListSerializer(serializers.ModelSerializer):
    vehicle_model = VehicleModelSerializer(read_only=True)
    class Meta:
        model = Car
        fields = ['id','vin','registration_number','year','color','vehicle_model']

class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'

class ServiceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class OwnershipSerializer(serializers.ModelSerializer):
    car = CarListSerializer(read_only=True)
    class Meta:
        model = Ownership
        fields = '__all__'

class OwnerDetailSerializer(serializers.ModelSerializer):
    driver_license = DriverLicenseSerializer(read_only=True)
    contacts = OwnerContactSerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ['id','first_name','last_name','patronymic','city','created_at','updated_at','driver_license','contacts','ownerships']