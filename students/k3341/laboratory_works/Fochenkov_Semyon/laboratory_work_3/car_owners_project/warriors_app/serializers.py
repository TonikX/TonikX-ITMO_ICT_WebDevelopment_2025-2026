from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


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
        fields = ["skill", "level"]


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ["race", "name", "level", "profession"]


class WarriorNestedSerializer(serializers.ModelSerializer):
    # Делаем наследование
    profession = ProfessionSerializer(read_only=True)
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)
    
    # Уточняем поле
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class SkillRelatedSerializer(serializers.ModelSerializer):
    warrior_skils = WarriorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Skill
        fields = ["title", "warrior_skils"]


class WarriorRelatedSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field='title')
    # skill = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"
        # добавляем глубину
        depth = 1
