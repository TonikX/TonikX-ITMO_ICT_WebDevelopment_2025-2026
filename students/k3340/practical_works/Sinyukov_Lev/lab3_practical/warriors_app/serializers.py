from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ["id", "skill", "level"]


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    race = serializers.CharField(source="get_race_display", read_only=True)
    skills = SkillOfWarriorSerializer(source="skillofwarrior_set", many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "profession", "skills"]


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)
    skills = SkillOfWarriorSerializer(source="skillofwarrior_set", many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "profession", "skills"]