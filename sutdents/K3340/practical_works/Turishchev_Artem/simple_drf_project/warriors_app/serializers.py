from rest_framework import serializers
from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class WarriorCreateSerializer(serializers.ModelSerializer):
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Warrior
        fields = ['race', 'name', 'level', 'profession']

class WarriorsWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorsWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class SkillOfWarriorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    level = serializers.IntegerField(min_value=1)

class WarriorUpdateSerializer(serializers.ModelSerializer):
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False, allow_null=True)
    skills = SkillOfWarriorSerializer(many=True, required=False)

    class Meta:
        model = Warrior
        fields = ['name', 'race', 'level', 'profession', 'skills']
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.race = validated_data.get('race', instance.race)
        instance.level = validated_data.get('level', instance.level)
        instance.profession = validated_data.get('profession', instance.profession)
        instance.save()

        skills_data = validated_data.get('skills')
        if skills_data is not None:
            SkillOfWarrior.objects.filter(warrior=instance).delete()
            for skill_item in skills_data:
                skill_id = skill_item['id']
                skill_level = skill_item['level']
                if not Skill.objects.filter(id=skill_id).exists():
                    raise serializers.ValidationError(f"Skill с id={skill_id} не существует.")
                SkillOfWarrior.objects.create(
                    warrior=instance,
                    skill_id=skill_id,
                    level=skill_level
                )
        return instance