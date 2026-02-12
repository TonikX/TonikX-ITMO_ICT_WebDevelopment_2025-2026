from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
  class Meta:
     model = Warrior
     fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
	    model = Profession
	    fields = ["title", "description"]


class WarriorFullSerializer(serializers.ModelSerializer):
    professions = ProfessionSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    level = serializers.IntegerField()
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), many=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    def create(self, validated_data):
        professions = validated_data.pop("profession")
        skills = validated_data.pop("skills")

        warrior = Warrior.objects.create(**validated_data)

        warrior.profession.set(professions)
        warrior.skills.set(skills)

        return warrior

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return Profession(**validated_data)




class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("title",)


