from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Skill, Warrior
from .serializers import SkillSerializer, SkillCreateSerializer, WarriorProfessionSerializer, WarriorSkillSerializer, WarriorDetailSerializer


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response({"Success": f"Skill '{skill_saved.title}' created successfully."})

        return Response(serializer.errors, status=400)

class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()


class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all()


class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorDetailSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'pk' # Ищем по ID


class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorDetailSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'pk'


class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    lookup_field = 'pk'