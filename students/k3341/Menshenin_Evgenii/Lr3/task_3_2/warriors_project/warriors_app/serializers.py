from rest_framework import serializers
from .models import *

class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        skill = Skill(**validated_data)
        skill.save()
        return skill

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field="title")
    
    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = serializers.SlugRelatedField(read_only=True, slug_field="title")
    
    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorProfessionSkillsSerializer(serializers.ModelSerializer):
    profession = serializers.SlugRelatedField(read_only=True, slug_field="title")
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field="title")
    
    class Meta:
        model = Warrior
        fields = "__all__"