from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Skill, Warrior, Profession, SkillOfWarrior

from .serializers import (
    SkillSerializer,
    WarriorWithProfessionSerializer,
    WarriorWithSkillsSerializer,
    WarriorFullSerializer,
    WarriorSerializer,
    ProfessionSerializer
)


# APIView: просмотр всех скилов
class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


# APIView: добавление скила
class SkillCreateAPIView(APIView):
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        skill_saved = serializer.save()
        return Response(
            {"Success": f"Skill '{skill_saved.title}' created successfully."},
            status=status.HTTP_201_CREATED,
        )

# 1) Все воины + профессии
class WarriorListWithProfessionsAPIView(generics.ListAPIView):
    queryset = Warrior.objects.select_related("profession").all()
    serializer_class = WarriorWithProfessionSerializer


# 2) Все воины + скилы
class WarriorListWithSkillsAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorWithSkillsSerializer


# 3) Один воин по id + профессия + скилы
class WarriorRetrieveFullAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.select_related("profession").all()
    serializer_class = WarriorFullSerializer


# 4) Удаление воина по id
class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()


# 5) Редактирование воина
class WarriorUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class ProfessionCreateAPIView(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class WarriorCreateAPIView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer