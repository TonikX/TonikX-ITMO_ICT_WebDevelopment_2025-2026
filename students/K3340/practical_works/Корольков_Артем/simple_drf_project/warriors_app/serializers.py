from rest_framework import serializers
from .models import Warrior, Profession, Skill

class SkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Skill
    Преобразует объекты Skill в JSON и обратно
    """
    class Meta:
        model = Skill
        fields = "__all__"  # Включаем все поля модели


class WarriorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Warrior
    """
    class Meta:
        model = Warrior
        fields = "__all__"  # Все поля модели Warrior


class ProfessionCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания профессий
    """
    class Meta:
        model = Profession
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["title", "description"]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["title"]


# Специализированные сериализаторы для воинов
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]


class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skill"]


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"