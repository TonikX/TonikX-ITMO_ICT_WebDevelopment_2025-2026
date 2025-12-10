from rest_framework import serializers
from .models import *

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
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

class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']

class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']

class WarriorCreateUpdateSerializer(serializers.ModelSerializer):
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, write_only=True, source='skill'
    )

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill_ids']
