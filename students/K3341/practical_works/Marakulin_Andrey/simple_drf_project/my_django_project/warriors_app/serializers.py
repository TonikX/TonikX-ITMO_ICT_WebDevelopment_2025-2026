from rest_framework import serializers
from .models import Skill, Warrior, Profession, SkillOfWarrior

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('title',)


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('title', 'description')


# Сериализатор для SkillOfWarrior (нужен для связи Many-to-Many с доп. полем 'level')
class SkillOfWarriorSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='skill.title', read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ('title', 'level')


# 1. Вывод полной информации о всех войнах и их профессиях (в одном запросе)
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = '__all__'



class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = '__all__'


class WarriorDetailSerializer(serializers.ModelSerializer):
    # Используем вложенность
    profession = ProfessionSerializer()
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    race_display = serializers.CharField(source='get_race_display', read_only=True)

    class Meta:
        model = Warrior
        fields = '__all__'