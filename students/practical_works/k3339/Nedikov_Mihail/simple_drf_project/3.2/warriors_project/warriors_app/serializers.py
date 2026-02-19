from rest_framework import serializers
from .models import Warrior, Profession, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "title"]


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "title", "description"]


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        return Profession.objects.create(**validated_data)

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"