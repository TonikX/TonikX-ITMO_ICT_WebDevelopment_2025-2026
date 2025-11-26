from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warrior
        fields = "__all__"

    def validate_level(self, level):
        if level < 0:
            raise serializers.ValidationError('Уровень не может быть меньше 0')
        return level


class ProfessionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class SkillOfWarriorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillOfWarrior
        fields = '__all__'

    def validate_level(self, level):
        if level < 0:
            raise serializers.ValidationError('Уровень не может быть меньше 0')
        return level


class ProfessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profession
        fields = '__all__'


class WarriorProfessionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода война с информацией о профессии
    """
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorSkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода война с информацией о скилах
    """
    warrior_skills = SkillOfWarriorSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorFullSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода полной информации о войне: профессия и скилы
    """
    profession = ProfessionSerializer(read_only=True)
    warrior_skills = SkillOfWarriorSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"
