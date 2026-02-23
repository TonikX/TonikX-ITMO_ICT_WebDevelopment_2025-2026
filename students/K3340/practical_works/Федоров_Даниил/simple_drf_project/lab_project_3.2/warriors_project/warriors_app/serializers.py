from rest_framework import serializers
from .models import *

#____________________________________________________________________________
class WarriorSerializer(serializers.ModelSerializer):

  class Meta:
     model = Warrior
     fields = "__all__"

#____________________________________________________________________________
class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
      model = Profession
      fields = "__all__"

#____________________________________________________________________________
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

#____________________________________________________________________________
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    class Meta:
        model = Warrior
        fields = "__all__"

#____________________________________________________________________________

class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level"]

class WarriorSkillsSerializer(serializers.ModelSerializer):
    skills_info = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills_info"]


class WarriorAllSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skills_info = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)
    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills_info", 'profession']