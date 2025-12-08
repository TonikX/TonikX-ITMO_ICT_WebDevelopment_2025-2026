from rest_framework import serializers
from .models import Warrior, Profession, Skill


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return profession


# --- наш сериализатор для скиллов ---

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
    # вложенный объект профессии, а не просто id
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorSkillSerializer(serializers.ModelSerializer):
    # вместо списка id получим список названий скиллов
    skill = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='title'
    )

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorNestedSerializer(serializers.ModelSerializer):
    # вложенная профессия
    profession = ProfessionSerializer()
    # вложенные скиллы как объекты (id + title)
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"