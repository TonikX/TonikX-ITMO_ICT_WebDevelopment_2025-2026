from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Warrior, Profession, Skill
from .serializers import (
    WarriorSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorFullSerializer,
)

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

        return Response({"Success": f"Profession '{profession_saved.title}' created succesfully."})

class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateAPIView(APIView):
    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": f"Skill '{skill_saved.title}' created succesfully."})

class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer

    def get_queryset(self):
        return Warrior.objects.select_related("profession").all()

class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer

    def get_queryset(self):
        return Warrior.objects.prefetch_related("skill").all()


class WarriorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()
    lookup_field = "pk"