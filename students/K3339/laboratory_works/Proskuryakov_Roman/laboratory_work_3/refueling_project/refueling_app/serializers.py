from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import (
    FuelReference, Companies, ProducedFuel, GasStation, User,
    SoldFuel, FuelPrices, Clients, ClientCards, Sales
)


class FuelReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReference
        fields = "__all__"

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"

class ProducedFuelSerializer(serializers.ModelSerializer):
    fuel = FuelReferenceSerializer(source="id_kind_fuel", read_only=True)
    company = CompaniesSerializer(source="id_company", read_only=True)

    id_kind_fuel = serializers.PrimaryKeyRelatedField(
        queryset=FuelReference.objects.all(),
        write_only=True
    )
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = ProducedFuel
        fields = (
            "id_produced_fuel",
            "fuel",
            "company",
            "id_kind_fuel",
            "id_company",
        )

class GasStationSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer(source="id_company", read_only=True)
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = GasStation
        fields = (
            "id_station",
            "station_address",
            "company",
            "id_company",
        )

class SoldFuelSerializer(serializers.ModelSerializer):
    produced_fuel = ProducedFuelSerializer(
        source="id_produced_fuel",
        read_only=True
    )
    station = GasStationSerializer(
        source="id_station",
        read_only=True
    )

    id_produced_fuel = serializers.PrimaryKeyRelatedField(
        queryset=ProducedFuel.objects.all(),
        write_only=True
    )
    id_station = serializers.PrimaryKeyRelatedField(
        queryset=GasStation.objects.all(),
        write_only=True
    )

    class Meta:
        model = SoldFuel
        fields = (
            "id_sold_fuel",
            "produced_fuel",
            "station",
            "id_produced_fuel",
            "id_station",
        )

class FuelPricesSerializer(serializers.ModelSerializer):
    sold_fuel = SoldFuelSerializer(
        source="id_sold_fuel",
        read_only=True
    )
    id_sold_fuel = serializers.PrimaryKeyRelatedField(
        queryset=SoldFuel.objects.all(),
        write_only=True
    )

    class Meta:
        model = FuelPrices
        fields = (
            "id_fuel_price",
            "sold_fuel",
            "id_sold_fuel",
            "start_time",
            "end_time",
            "per_liter",
        )

class ClientCardsSerializer(serializers.ModelSerializer):
    client = ClientsSerializer(source="id_client", read_only=True)
    company = CompaniesSerializer(source="id_company", read_only=True)

    id_client = serializers.PrimaryKeyRelatedField(
        queryset=Clients.objects.all(),
        write_only=True
    )
    id_company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        write_only=True
    )

    class Meta:
        model = ClientCards
        fields = (
            "id_card",
            "client",
            "company",
            "id_client",
            "id_company",
            "start_date",
            "end_date",
            "balance",
            "discount_percent",
            "discount_rub",
        )

class SalesSerializer(serializers.ModelSerializer):
    fuel_price = FuelPricesSerializer(
        source="id_fuel_price",
        read_only=True
    )
    card = ClientCardsSerializer(
        source="id_card",
        read_only=True
    )

    id_fuel_price = serializers.PrimaryKeyRelatedField(
        queryset=FuelPrices.objects.all(),
        write_only=True
    )
    id_card = serializers.PrimaryKeyRelatedField(
        queryset=ClientCards.objects.all(),
        write_only=True
    )

    class Meta:
        model = Sales
        fields = (
            "id_sales",
            "fuel_price",
            "card",
            "id_fuel_price",
            "id_card",
            "sale_date",
            "sold_liters_volume",
            "amount_paid",
        )

class CustomUserCreateSerializer(UserCreateSerializer):
    id_station = serializers.PrimaryKeyRelatedField(
        queryset=GasStation.objects.all(),
        required=True,
        allow_null=False
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "password",
            "re_password",
            "email",
            "id_station",
        )

class CustomUserSerializer(UserSerializer):
    gas_station = GasStationSerializer(
        source="id_station",
        read_only=True
    )

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            # "id_station",
            "gas_station",
        )
        # fields = UserSerializer.Meta.fields + ("",)

class PaymentCalculationSerializer(serializers.Serializer):
    id_card = serializers.IntegerField()
    initial_amount = serializers.FloatField(min_value=0)

class PaymentCalculationResultSerializer(serializers.Serializer):
    final_amount = serializers.FloatField()
    sufficient_balance = serializers.BooleanField()

class FuelPurchaseCalculationSerializer(serializers.Serializer):
    id_fuel_price = serializers.IntegerField()
    liters = serializers.FloatField(min_value=0)
    id_card = serializers.IntegerField(required=False)


from decimal import Decimal

# def create_model_serializer_with_sales_summary(model_class):
#     """
#     Фабрика для создания сериализаторов с добавленными полями сводки продаж
#     """
#     class SerializerWithSalesSummary(serializers.ModelSerializer):
#         total_amount = serializers.DecimalField(
#             max_digits=10, 
#             decimal_places=2, 
#             read_only=True,
#             default=Decimal('0.00')
#         )
#         # sales_count = serializers.IntegerField(
#         #     read_only=True,
#         #     default=0
#         # )
#         # avg_liters = serializers.DecimalField(
#         #     max_digits=10, 
#         #     decimal_places=2, 
#         #     read_only=True,
#         #     default=Decimal('0.00')
#         # )
        
#         class Meta:
#             model = model_class
#             # Получаем все поля модели + наши 3 поля
#             fields = [field.name for field in model_class._meta.get_fields()] + [
#                 'total_amount', 
#                 # 'sales_count', 
#                 # 'avg_liters'
#             ]
    
#     return SerializerWithSalesSummary


# def create_model_serializer_with_sales_summary(model_class):
#     """
#     Фабрика для создания сериализаторов с добавленными полями сводки продаж
#     """
#     # Получаем только реальные поля модели (исключая обратные связи и relations)
#     model_field_names = []
    
#     for field in model_class._meta.get_fields():
#         # Исключаем обратные связи и ManyToMany relations
#         if field.auto_created or field.many_to_many:
#             continue
        
#         # Исключаем поля, которые не являются полями модели (например, методы)
#         if not hasattr(field, 'attname'):
#             continue
            
#         model_field_names.append(field.name)
    
#     class SerializerWithSalesSummary(serializers.ModelSerializer):
#         total_amount = serializers.DecimalField(
#             max_digits=10, 
#             decimal_places=2, 
#             read_only=True,
#             default=Decimal('0.00')
#         )
#         sales_count = serializers.IntegerField(
#             read_only=True,
#             default=0
#         )
#         avg_liters = serializers.DecimalField(
#             max_digits=10, 
#             decimal_places=2, 
#             read_only=True,
#             default=Decimal('0.00')
#         )
#         1
#         class Meta:
#             model = model_class
#             # Получаем только реальные поля модели + наши 3 поля
#             fields = model_field_names + [
#                 'total_amount', 
#                 'sales_count', 
#                 'avg_liters'
#             ]
    
#     return SerializerWithSalesSummary


def create_model_serializer_with_sales_summary(model_class, hidden_columns):
    """
    Фабрика для создания сериализаторов, работающих со словарями (из .values())
    """
    # Маппинг типов Django полей на сериализаторы DRF
    from django.db import models
    
    field_mapping = {
        models.AutoField: serializers.IntegerField,
        models.IntegerField: serializers.IntegerField,
        models.BigIntegerField: serializers.IntegerField,
        models.CharField: serializers.CharField,
        models.TextField: serializers.CharField,
        models.DateField: serializers.DateField,
        models.DateTimeField: serializers.DateTimeField,
        models.DecimalField: serializers.DecimalField,
        models.FloatField: serializers.FloatField,
        models.BooleanField: serializers.BooleanField,
        models.ForeignKey: serializers.IntegerField,  # Для ForeignKey используем IntegerField
    }
    
    # Собираем информацию о полях модели
    fields_dict = {}
    
    for field in model_class._meta.get_fields():
        # Пропускаем обратные связи и ManyToMany
        if field.auto_created or field.many_to_many:
            continue

        # исключаем скрытые поля
        if field.name in hidden_columns:
            continue

        # Определяем тип сериализатора для поля
        field_type = type(field)
        if field_type in field_mapping:
            if field_type == models.ForeignKey:
                fields_dict[field.name] = serializers.IntegerField()
            elif field_type == models.DecimalField:
                fields_dict[field.name] = serializers.DecimalField(
                    max_digits=field.max_digits,
                    decimal_places=field.decimal_places
                )
            elif field_type == models.CharField:
                fields_dict[field.name] = serializers.CharField(
                    max_length=field.max_length
                )
            else:
                # Для остальных типов создаем поле с параметрами по умолчанию
                fields_dict[field.name] = field_mapping[field_type]()
    
    # Добавляем поля сводки
    from decimal import Decimal
    
    fields_dict.update({
        'total_amount': serializers.DecimalField(
            max_digits=10, 
            decimal_places=2, 
            default=Decimal('0.00')
        ),
        'sales_count': serializers.IntegerField(default=0),
        'avg_liters': serializers.DecimalField(
            max_digits=10, 
            decimal_places=2, 
            default=Decimal('0.00')
        )
    })
    
    # Создаем класс сериализатора
    SerializerClass = type(
        f'{model_class.__name__}DictSerializer',
        (serializers.Serializer,),
        fields_dict
    )
    
    return SerializerClass

# Создаем сериализаторы с помощью фабрики
# FuelReferenceSerializer = create_model_serializer_with_sales_summary(FuelReference)
# CompaniesSerializer = create_model_serializer_with_sales_summary(Companies)
# ProducedFuelSerializer = create_model_serializer_with_sales_summary(ProducedFuel)
# GasStationSerializer = create_model_serializer_with_sales_summary(GasStation)
# SoldFuelSerializer = create_model_serializer_with_sales_summary(SoldFuel)
# FuelPricesSerializer = create_model_serializer_with_sales_summary(FuelPrices)
# ClientsSerializer = create_model_serializer_with_sales_summary(Clients)
# ClientCardsSerializer = create_model_serializer_with_sales_summary(ClientCards)


