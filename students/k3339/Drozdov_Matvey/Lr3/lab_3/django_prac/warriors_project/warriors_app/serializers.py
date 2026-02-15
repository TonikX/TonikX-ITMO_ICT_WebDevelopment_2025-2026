from rest_framework import serializers
from .models import Warrior, Profession, Skill


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


# 1. Все воины + профессии
class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


# 2. Все воины + скилы
class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


# 3. Один воин + профессия + скилы
class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


# 5. Редактирование воина
class WarriorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"
