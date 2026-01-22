from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


# class ProfessionCreateView(APIView):
#
#     def post(self, request):
#         profession = request.data.get("profession")
#         serializer = ProfessionCreateSerializer(data=profession)
#
#         if serializer.is_valid(raise_exception=True):
#             profession_saved = serializer.save()
#
#         return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


# class SkillCreateView(APIView):
#     def post(self, request):
#         skill = request.data.get("skill")
#         serializer = SkillSerializer(data=skill)
#
#         if serializer.is_valid(raise_exception=True):
#             skill_saved = serializer.save()
#
#         return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})

class WarriorListAPIView(generics.ListAPIView):
   serializer_class = WarriorSerializer
   queryset = Warrior.objects.all()

class SkillCreateAPIView(generics.CreateAPIView):
    serializer_class = SkillCreateSerializer
    queryset = Skill.objects.all()

class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()

class WarriorProfessionListAPIView(generics.ListAPIView):
   serializer_class = WarriorProfessionSerializer
   queryset = Warrior.objects.all().select_related("profession")

class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all().prefetch_related("warrior_skill__skill")

class WarriorDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all().select_related("profession").prefetch_related("warrior_skill__skill")
    lookup_field = 'id'

class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    lookup_field = 'id'

class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorCreateUpdateSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'id'

class WarriorCreateAPIView(generics.CreateAPIView):
    serializer_class = WarriorCreateUpdateSerializer
    queryset = Warrior.objects.all()