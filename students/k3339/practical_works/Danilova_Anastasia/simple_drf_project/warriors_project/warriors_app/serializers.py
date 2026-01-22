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
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillOfWarrior
        fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']


class WarriorSkillSerializer(serializers.ModelSerializer):
    warrior_skill = SkillOfWarriorSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'warrior_skill']


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    warrior_skill = SkillOfWarriorSerializer(many=True, read_only=True)



    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'warrior_skill']


class WarriorSkillInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    level = serializers.IntegerField()


class WarriorCreateUpdateSerializer(serializers.ModelSerializer):
    profession_id = serializers.IntegerField(write_only=True, required=False)
    skill = WarriorSkillInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession_id', 'skill']

    def create(self, validated_data):
        skill_data = validated_data.pop('skill', [])
        profession_id = validated_data.pop('profession_id', None)

        warrior = Warrior.objects.create(**validated_data)

        if profession_id:
            warrior.profession_id = profession_id
            warrior.save()

        # создаём записи в SkillOfWarrior
        for item in skill_data:
            SkillOfWarrior.objects.create(
                warrior=warrior,
                skill_id=item['id'],
                level=item['level']
            )

        return warrior

    def update(self, instance, validated_data):
        skill_data = validated_data.pop('skill', None)
        profession_id = validated_data.pop('profession_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profession_id is not None:
            instance.profession_id = profession_id

        instance.save()

        if skill_data is not None:
            # полностью пересоздаём набор скиллов
            SkillOfWarrior.objects.filter(warrior=instance).delete()

            for item in skill_data:
                SkillOfWarrior.objects.create(
                    warrior=instance,
                    skill_id=item['id'],
                    level=item['level']
                )

        return instance
