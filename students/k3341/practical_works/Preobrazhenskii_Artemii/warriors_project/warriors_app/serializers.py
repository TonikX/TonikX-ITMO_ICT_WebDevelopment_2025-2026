from rest_framework import serializers

from .models import Profession, Skill, SkillOfWarrior, Warrior


class ProfessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profession
		fields = ["title", "description"]

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


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['title']


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

class SkillRelatedSerializer(serializers.ModelSerializer):
    warrior_skils = WarriorSerializer(many=True)
    
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

class WarriorNestedSerializer(serializers.ModelSerializer):
    # делаем наследование
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    # уточняем поле
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]


class WarriorSkillSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills"]

class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession", "skills"]

    def get_skills(self, obj):
        skills_qs = SkillOfWarrior.objects.filter(warrior=obj).select_related("skill")
        return [{"title": s.skill.title, "level": s.level} for s in skills_qs]