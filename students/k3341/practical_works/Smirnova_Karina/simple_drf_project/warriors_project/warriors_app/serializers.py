from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
  class Meta:
     model = Warrior
     fields = "__all__"

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
       profession = Profession(**validated_data)
       profession.save()
       return Profession(**validated_data)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class WarriorFullSerializer(serializers.ModelSerializer):
    """
    Для вывода полной информации о воине с вложенными профессией и скиллами
    """
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    class Meta:
        model = Warrior
        fields = ('id', 'name', 'race', 'level', 'profession')

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    class Meta:
        model = Warrior
        fields = ('id', 'name', 'race', 'level', 'skill')