from rest_framework import serializers
from .models import *

# Для старых эндпоинтов
class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession.objects.create(**validated_data)
        return profession


class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        skill = Skill.objects.create(**validated_data)
        return skill


class ProfessionSerializer(serializers.ModelSerializer):
    """Сериализатор для профессии"""

    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для умения"""

    class Meta:
        model = Skill
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    """Сериализатор для связи воин-умение с уровнем"""
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level"]


# Основные сериализаторы для Warrior
class WarriorProfessionSerializer(serializers.ModelSerializer):
    """Сериализатор для воина с информацией о профессии"""
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "profession"]


class WarriorSkillSerializer(serializers.ModelSerializer):
    """Сериализатор для воина с информацией о скилах"""
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "skill"]

    def get_skill(self, warrior):
        # Получаем все связи воина с умениями через промежуточную таблицу
        skills_of_warrior = SkillOfWarrior.objects.filter(warrior=warrior)
        return SkillOfWarriorSerializer(skills_of_warrior, many=True).data


class WarriorFullSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о воине (профессия + скилы)"""
    profession = ProfessionSerializer(read_only=True)
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "profession", "skill"]

    def get_skill(self, warrior):
        # Получаем все связи воина с умениями через промежуточную таблицу
        skills_of_warrior = SkillOfWarrior.objects.filter(warrior=warrior)
        return SkillOfWarriorSerializer(skills_of_warrior, many=True).data


class WarriorUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления информации о воине"""

    class Meta:
        model = Warrior
        fields = ["race", "name", "level", "profession"]