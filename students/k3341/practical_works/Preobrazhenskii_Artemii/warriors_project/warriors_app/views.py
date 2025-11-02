from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView, Response

from .models import Profession, Skill, SkillOfWarrior, Warrior
from .serializers import (
   ProfessionCreateSerializer,
   ProfessionSerializer,
   SkillCreateSerializer,
   SkillSerializer,
   WarriorFullSerializer,
   WarriorProfessionSerializer,
   WarriorSerializer,
)


class WarriorListAPIView(generics.ListAPIView):
   serializer_class = WarriorSerializer
   queryset = Warrior.objects.all()

class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()

class WarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = WarriorSerializer
   queryset = Warrior.objects.all()
   # permission_classes = [permissions.AllowAny]

class ProfessionListAPIView(generics.ListAPIView):
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()

class SkillAPIView(APIView):
    """
    Просмотр всех умений
    """
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

class AddSkillToWarriorView(APIView):
    def post(self, request, pk):
        try:
            warrior = Warrior.objects.get(pk=pk)
        except Warrior.DoesNotExist:
            return Response({"error": "Warrior not found"}, status=status.HTTP_404_NOT_FOUND)

        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)
        serializer.is_valid(raise_exception=True)
        skill = serializer.save()
        SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=1)

        return Response({"success": f"Skill '{skill.title}' added to warrior '{warrior.name}'"})
    
class WarriorWithProfessionListView(generics.ListAPIView):
    queryset = Warrior.objects.select_related("profession").all()
    serializer_class = WarriorProfessionSerializer

class WarriorWithSkillsListView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer

class WarriorFullDetailView(generics.RetrieveAPIView):
    queryset = Warrior.objects.select_related("profession").all() 
    serializer_class = WarriorFullSerializer
    lookup_field = "id"

class WarriorDeleteView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = "id"

class WarriorUpdateView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = "id"