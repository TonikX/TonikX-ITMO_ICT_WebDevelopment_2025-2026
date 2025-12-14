from rest_framework import serializers
from .models import (
    Newspaper, PrintingHouse, PostOffice, PrintingRun, Distribution
)


class NewspaperSerializer(serializers.ModelSerializer):
    """Сериализатор для газеты"""
    editor_full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Newspaper
        fields = ['id', 'title', 'publication_index', 'editor_first_name', 
                 'editor_last_name', 'editor_middle_name', 'editor_full_name', 
                 'price_per_copy']


class PrintingHouseSerializer(serializers.ModelSerializer):
    """Сериализатор для типографии"""
    
    class Meta:
        model = PrintingHouse
        fields = ['id', 'name', 'address', 'is_active']


class PostOfficeSerializer(serializers.ModelSerializer):
    """Сериализатор для почтового отделения"""
    
    class Meta:
        model = PostOffice
        fields = ['id', 'number', 'address']


class PrintingRunSerializer(serializers.ModelSerializer):
    """Сериализатор для тиража"""
    printing_house_name = serializers.CharField(source='printing_house.name', read_only=True)
    newspaper_title = serializers.CharField(source='newspaper.title', read_only=True)
    
    class Meta:
        model = PrintingRun
        fields = ['id', 'printing_house', 'printing_house_name', 'newspaper', 
                 'newspaper_title', 'circulation']


class DistributionSerializer(serializers.ModelSerializer):
    """Сериализатор для распределения"""
    post_office_number = serializers.CharField(source='post_office.number', read_only=True)
    post_office_address = serializers.CharField(source='post_office.address', read_only=True)
    newspaper_title = serializers.CharField(source='newspaper.title', read_only=True)
    newspaper_index = serializers.CharField(source='newspaper.publication_index', read_only=True)
    printing_house_name = serializers.CharField(source='printing_house.name', read_only=True)
    printing_house_address = serializers.CharField(source='printing_house.address', read_only=True)
    
    class Meta:
        model = Distribution
        fields = ['id', 'post_office', 'post_office_number', 'post_office_address',
                 'newspaper', 'newspaper_title', 'newspaper_index',
                 'printing_house', 'printing_house_name', 'printing_house_address',
                 'quantity']


# Сериализаторы с вложенными объектами для связей один-ко-многим и многие-ко-многим

class PrintingRunNestedSerializer(serializers.ModelSerializer):
    """Сериализатор тиража с вложенной газетой"""
    newspaper = NewspaperSerializer(read_only=True)
    
    class Meta:
        model = PrintingRun
        fields = ['id', 'newspaper', 'circulation']


class DistributionNestedSerializer(serializers.ModelSerializer):
    """Сериализатор распределения с вложенными объектами"""
    newspaper = NewspaperSerializer(read_only=True)
    printing_house = PrintingHouseSerializer(read_only=True)
    
    class Meta:
        model = Distribution
        fields = ['id', 'newspaper', 'printing_house', 'quantity']


class PrintingHouseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор типографии с вложенными тиражами (one-to-many)"""
    printing_runs = serializers.SerializerMethodField()
    
    class Meta:
        model = PrintingHouse
        fields = ['id', 'name', 'address', 'is_active', 'printing_runs']
    
    def get_printing_runs(self, obj):
        printing_runs = obj.printingrun_set.select_related('newspaper').all()
        return PrintingRunNestedSerializer(printing_runs, many=True).data


class PostOfficeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор почтового отделения с вложенными распределениями (one-to-many)"""
    distributions = serializers.SerializerMethodField()
    
    class Meta:
        model = PostOffice
        fields = ['id', 'number', 'address', 'distributions']
    
    def get_distributions(self, obj):
        distributions = obj.distribution_set.select_related('newspaper', 'printing_house').all()
        return DistributionNestedSerializer(distributions, many=True).data


class NewspaperDetailSerializer(serializers.ModelSerializer):
    """Сериализатор газеты с вложенными тиражами и распределениями (many-to-many)"""
    editor_full_name = serializers.ReadOnlyField()
    printing_runs = serializers.SerializerMethodField()
    distributions = serializers.SerializerMethodField()
    
    class Meta:
        model = Newspaper
        fields = ['id', 'title', 'publication_index', 'editor_first_name', 
                 'editor_last_name', 'editor_middle_name', 'editor_full_name', 
                 'price_per_copy', 'printing_runs', 'distributions']
    
    def get_printing_runs(self, obj):
        printing_runs = obj.printingrun_set.select_related('newspaper').all()
        return PrintingRunNestedSerializer(printing_runs, many=True).data
    
    def get_distributions(self, obj):
        distributions = obj.distribution_set.select_related('newspaper', 'printing_house').all()
        return DistributionNestedSerializer(distributions, many=True).data

