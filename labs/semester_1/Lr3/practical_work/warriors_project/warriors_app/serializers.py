from rest_framework import serializers
from .models import (
    Warrior,
    Profession,
    Skill,
    SkillOfWarrior,
)


# Воин
class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

# Специальный serializer для обновления война
# (Основная цель - возможность обновления поля 'skill' с ManyToMany-связью)
class WarriorUpdateSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Skill.objects.all(),
        required=False
    )

    class Meta:
        model = Warrior
        fields = "__all__"
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skill', None)
        instance = super().update(instance, validated_data)
        if skills_data is not None:
            instance.skill.clear()
            for skill in skills_data:
                SkillOfWarrior.objects.create(
                    warrior=instance,
                    skill=skill,
                    level=1
                )
        return instance


# Профессия
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


# Навык
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


# Навык конкретного воина
class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level"]


# Воин с информацией о профессии
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"


# Воин с информацией о навыках
class WarriorSkillsSerializer(serializers.ModelSerializer):
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"


# Воин с информацией о профессии и навыках
class WarriorProfessionSkillsSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"
