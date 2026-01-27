from rest_framework import serializers
from .models import Skill, Warrior, Profession, SkillOfWarrior


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level"]


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]


class WarriorSkillsSerializer(serializers.ModelSerializer):
    skills_info = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills_info"]


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skills_info = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession", "skills_info"]


class WarriorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"
