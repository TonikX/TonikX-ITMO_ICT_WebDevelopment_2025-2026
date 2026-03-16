from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


# Базовые сериализаторы
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'description']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'title']


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']


# Сериализаторы для воинов
class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skill']


class WarriorProfessionSerializer(serializers.ModelSerializer):
    """Воин с информацией о профессии"""
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession']


class WarriorSkillSerializer(serializers.ModelSerializer):
    """Воин с информацией об умениях"""
    skill = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='title'
    )
    # Альтернатива: вывод читаемого значения расы вместо ключа
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'skill']


class WarriorDetailSerializer(serializers.ModelSerializer):
    """Полная информация о воине с профессией и умениями"""
    profession = ProfessionSerializer(read_only=True)
    skill_details = serializers.SerializerMethodField()
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skill_details']

    def get_skill_details(self, obj):
        """Получаем умения с уровнями через промежуточную модель"""
        skills = SkillOfWarrior.objects.filter(warrior=obj).select_related('skill')
        return [{
            'id': skill.skill.id,
            'title': skill.skill.title,
            'level': skill.level
        } for skill in skills]


# Для создания/обновления
class WarriorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ['race', 'name', 'level', 'profession', 'skill']


class WarriorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ['race', 'name', 'level', 'profession']