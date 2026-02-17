from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Warrior
from .serializers import *

class WarriorListAPIView(generics.ListAPIView):
   serializer_class = WarriorSerializer
   queryset = Warrior.objects.all()

class WarriorProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorProfessionSerializer

class WarriorSkillListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer

class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer

class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()
   
class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillSerializer(data=skill)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"Success": "Skill '{}' created".format(skill_saved.title)})