from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


class ProfessionSerializer(serializers.ModelSerializer):
    """Сериализатор для профессии"""

    class Meta:
        model = Profession
        fields = "__all__"


class ProfessionCreateSerializer(serializers.Serializer):
    """Сериализатор для создания профессии"""

    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return profession


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для умения"""

    class Meta:
        model = Skill
        fields = "__all__"


class SkillCreateSerializer(serializers.Serializer):
    """Сериализатор для создания умения"""

    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        skill = Skill(**validated_data)
        skill.save()
        return skill


class WarriorSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для воина"""

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания воина"""

    class Meta:
        model = Warrior
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    """Сериализатор для связи воин-умение"""

    class Meta:
        model = SkillOfWarrior
        fields = "__all__"


class WarriorProfessionSerializer(serializers.ModelSerializer):
    """Сериализатор воина с профессией"""

    profession = ProfessionSerializer(read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorSkillSerializer(serializers.ModelSerializer):
    """Сериализатор воина с умениями"""

    skill = SkillSerializer(many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор воина с профессией и умениями"""

    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"
