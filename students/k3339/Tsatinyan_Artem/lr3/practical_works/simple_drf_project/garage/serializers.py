from rest_framework import serializers
from .models import Owner, Car, DriverLicense, Ownership


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = "__all__"


class OwnerSerializer(serializers.ModelSerializer):
    license = DriverLicenseSerializer(read_only=True)

    class Meta:
        model = Owner
        fields = ["id", "first_name", "last_name", "middle_name", "birth_date", "license"]


class OwnershipSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = Ownership
        fields = "__all__"


class OwnerWithCarsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(source="ownerships__car", many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ["id", "first_name", "last_name", "cars"]
