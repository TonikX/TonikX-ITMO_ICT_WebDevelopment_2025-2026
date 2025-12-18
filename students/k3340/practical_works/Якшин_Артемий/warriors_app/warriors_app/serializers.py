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
    Детальный сериализатор для SkillOfWarrior с информацией о скиле
    """
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Warrior с вложенной информацией о профессии
    """
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Warrior с вложенной информацией о скилах
    """
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'skills']

    def get_skills(self, obj):
        skill_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        return SkillOfWarriorDetailSerializer(skill_of_warrior, many=True).data


class WarriorDetailSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для Warrior с профессией и скилами
    """
    profession = ProfessionSerializer()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skills']

    def get_skills(self, obj):
        skill_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        return SkillOfWarriorDetailSerializer(skill_of_warrior, many=True).data

