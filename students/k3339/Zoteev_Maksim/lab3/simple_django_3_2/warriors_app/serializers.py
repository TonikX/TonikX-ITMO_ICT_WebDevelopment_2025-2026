from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


class WarriorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Warrior
    """

    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Profession
    """

    class Meta:
        model = Profession
        fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания Profession
    """

    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Skill
    """

    class Meta:
        model = Skill
        fields = "__all__"


class SkillCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания Skill
    """

    class Meta:
        model = Skill
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SkillOfWarrior
    """

    class Meta:
        model = SkillOfWarrior
        fields = "__all__"


class SkillOfWarriorDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации о скилах воина
    """
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']


class WarriorProfessionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для воина с информацией о профессии
    """
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession']


class WarriorSkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для воина с информацией о скилах
    """
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'skill']


class WarriorDetailSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор воина с профессией и скилами
    """
    profession = ProfessionSerializer(read_only=True)
    skills = SkillOfWarriorDetailSerializer(source='skillofwarrior_set', many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skills']
