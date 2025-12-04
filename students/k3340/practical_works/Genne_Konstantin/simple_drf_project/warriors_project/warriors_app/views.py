from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import *

class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})
   

class SkillAPIView(APIView):
   def get(self, request):
       skills = Skill.objects.all()
       serializer = SkillSerializer(skills, many=True)
       return Response({"Skills": serializer.data})
   

class SkillCreateView(APIView):

   def post(self, request):
       skill = request.data.get("skill")
       serializer = SkillCreateSerializer(data=skill)

       if serializer.is_valid(raise_exception=True):
           skill_saved = serializer.save()

       return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})


class WarriorWithProfessionAPIView(ListAPIView):
    serializer_class = WarriorsWithProfessionSerializer
    queryset = Warrior.objects.select_related('profession').all()


class WarriorWithSkillsAPIView(ListAPIView):
    serializer_class = WarriorsWithSkillsSerializer
    queryset = Warrior.objects.prefetch_related('skill').all()


class WarriorWithProfessionAndSkillsRetrieveAPIView(RetrieveAPIView):
    serializer_class = WarriorWithProfessionAndSkillsSerializer
    queryset = Warrior.objects.prefetch_related('skill').select_related('profession')


class WarriorDestroyAPIView(DestroyAPIView):
    queryset = Warrior.objects.all()


class WarriorRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Warrior.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WarriorUpdateSerializer
        return WarriorWithProfessionAndSkillsSerializer
