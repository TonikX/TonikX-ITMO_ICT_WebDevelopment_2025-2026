from rest_framework import serializers
from .models import *

class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_info'] = CarInfoSerializer(instance.car_info).data
        return representation

    class Meta:
        model = Car
        fields = "__all__"

class FineSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    class Meta:
        model = Fine
        fields = "__all__"

class CarCrashSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    class Meta:
        model = CarCrash
        fields = "__all__"

class CarInstanceSerializer(serializers.ModelSerializer):
    fines = FineSerializer(many=True, read_only=True)
    crashes = CarCrashSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car'] = CarSerializer(instance.car).data
        representation['fines'] = list(map(lambda el: el["description"], representation['fines']))
        representation['crashes'] = list(map(lambda el: el["info"], representation['crashes']))
        return representation
    
    def validate(self, data):
        if  (data.get('capacity') and data.get('capacity') <= 0) or\
            (data.get('engine_volume') and data.get('engine_volume') <= 0) or\
            (data.get('horsepower') and data.get('horsepower') <= 0) or\
            (data.get('clearance') and data.get('clearance') <= 0) or\
            (data.get('trunk_volume') and data.get('trunk_volume') <= 0) or\
            (data.get('tank_volume') and data.get('tank_volume') <= 0) or\
            (data.get('fuel_consumption') and data.get('fuel_consumption') <= 0):
            raise serializers.ValidationError("Некорректные данные")
              
        return data

    class Meta:
        model = CarInstance
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=representation['user'])
        representation['user_id'] = user.id
        representation['user'] = UserSerializer(user).data
        return representation
        
    class Meta:
        model = Client
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = "__all__"
        exclude = ('password',)
        read_only_fields = ('date_joined', 'user_permissions', 'groups', 'last_login')

class WorkerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=representation['user'])
        representation['user_id'] = user.id
        representation['user'] = UserSerializer(user).data
        return representation
    
    def validate(self, data):
        if data.get('salary') and data.get('salary') <= 0:
            raise serializers.ValidationError("Некорректная зарплата")
              
        return data

    class Meta:
        model = Worker
        fields = "__all__"

class RentContractSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['worker'] = WorkerSerializer(instance.worker).data
        representation['client'] = ClientSerializer(instance.client).data
        representation['car_instance_id'] = instance.car_instance.id
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    def validate(self, data):
        if (data.get('car_instance')):
            if RentContract.objects.filter(real_return_date=None, car_instance__id=data.get('car_instance').id).exists():
                raise serializers.ValidationError("Автомобиль уже в прокате")
            
            if RentContract.objects.filter(return_date__gt=data.get('start_date'), car_instance__id=data.get('car_instance').id).exists():
                raise serializers.ValidationError("Некорректная начальная дата")
        if (data.get('start_date') and data.get('return_date')):
            if data.get('start_date') >= data.get('return_date'):
                raise serializers.ValidationError("Некорректные даты проката")
              
        return data

    class Meta:
        model = RentContract
        fields = "__all__"