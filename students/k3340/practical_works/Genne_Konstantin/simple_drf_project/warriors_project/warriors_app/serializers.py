from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):

  class Meta:
     model = Warrior
     fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Profession
      fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):

  class Meta:
     model = Skill
     fields = "__all__"


class SkillCreateSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Skill
      fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Profession
      fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='skill.id')
    title = serializers.CharField(source='skill.title')
    
    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'title', 'level']


class WarriorsWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorsWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillOfWarriorSerializer(many=True, read_only=True, source='skillofwarrior_set')

    class Meta:
       model = Warrior
       fields = "__all__"


class WarriorWithProfessionAndSkillsSerializer(serializers.ModelSerializer):
    skill = SkillOfWarriorSerializer(many=True, read_only=True, source='skillofwarrior_set')
    profession = ProfessionSerializer(read_only=True)

    class Meta:
       model = Warrior
       fields = "__all__"


class SkillUpdateItemSerializer(serializers.Serializer):
    skill_id = serializers.IntegerField()
    level = serializers.IntegerField(min_value=1, max_value=100)


class WarriorUpdateSerializer(serializers.ModelSerializer):
    profession = serializers.PrimaryKeyRelatedField(
        queryset=Profession.objects.all(),
        required=False,
        allow_null=True
    )
    skill = SkillUpdateItemSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']

    def update(self, instance, validated_data):
        # Обновляем основные поля
        print("validated_data:", validated_data)
        instance.name = validated_data.get('name', instance.name)
        instance.race = validated_data.get('race', instance.race)
        instance.level = validated_data.get('level', instance.level)
        instance.profession = validated_data.get('profession', instance.profession)
        
        # Обработка навыков (если переданы)
        skill_data = validated_data.get('skill')
        if skill_data is not None:
            # Удаляем старые связи
            SkillOfWarrior.objects.filter(warrior=instance).delete()
            # Создаём новые
            for item in skill_data:
                skill_id = item.get('skill_id')
                level = item.get('level')
                if skill_id is not None and level is not None:
                    try:
                        skill = Skill.objects.get(id=skill_id)
                        SkillOfWarrior.objects.create(
                            warrior=instance,
                            skill=skill,
                            level=level
                        )
                    except Skill.DoesNotExist:
                        raise serializers.ValidationError(f"Skill with id={skill_id} does not exist.")
        
        instance.save()
        return instance
