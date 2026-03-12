
from rest_framework import serializers
from .models import Owner, Car, DriverLicense, Ownership

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = '__all__'

class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = '__all__'


class SimpleOwnerWithCarsSerializer(serializers.ModelSerializer):
    cars = serializers.SerializerMethodField()
    cars_count = serializers.SerializerMethodField()
    class Meta:
        model = Owner
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'cars',
            'cars_count'
        ]

    def get_cars(self, obj):
        # Получаем все машины через ownerships
        cars = [ownership.car for ownership in obj.ownerships.all()]
        return CarSerializer(cars, many=True).data

    def get_cars_count(self, obj):
        return obj.ownerships.count()