from rest_framework import serializers
from .models import Skill, Profession, Warrior, SkillOfWarrior


class SkillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Skill
		fields = '__all__'


class ProfessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profession
		fields = '__all__'


class SkillOfWarriorSerializer(serializers.ModelSerializer):
	skill_title = serializers.CharField(source='skill.title', read_only=True)
	
	class Meta:
		model = SkillOfWarrior
		fields = ('id', 'skill', 'skill_title', 'level')


class WarriorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Warrior
		fields = '__all__'


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
	profession = ProfessionSerializer(read_only=True)
	race_display = serializers.CharField(source='get_race_display', read_only=True)
	
	class Meta:
		model = Warrior
		fields = ('id', 'name', 'race', 'race_display', 'level', 'profession')


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
	warrior_skills = SkillOfWarriorSerializer(many=True, read_only=True)
	race_display = serializers.CharField(source='get_race_display', read_only=True)
	
	class Meta:
		model = Warrior
		fields = ('id', 'name', 'race', 'race_display', 'level', 'warrior_skills')


class WarriorDetailSerializer(serializers.ModelSerializer):
	profession = ProfessionSerializer(read_only=True)
	warrior_skills = SkillOfWarriorSerializer(many=True, read_only=True)
	race_display = serializers.CharField(source='get_race_display', read_only=True)
	
	class Meta:
		model = Warrior
		fields = ('id', 'name', 'race', 'race_display', 'level', 'profession', 'warrior_skills')
