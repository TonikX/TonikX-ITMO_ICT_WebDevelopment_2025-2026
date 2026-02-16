from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

    def update(self, instance, validated_data):
        skills_data = self.initial_data.get('skill')
        
        instance = super().update(instance, validated_data)

        if skills_data:
            instance.skill.clear()
            for skill_id in skills_data:
                SkillOfWarrior.objects.create(
                    warrior=instance,
                    skill_id=skill_id,
                    level=1
                )
        return instance

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        return Profession.objects.create(**validated_data)
    
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["title", "description"]

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Warrior
        fields = "__all__"

