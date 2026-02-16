# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import generics
# from .models import Warrior
# from .serializers import *
# from .models import Warrior, Skill
#
# class WarriorAPIView(APIView):
#     def get(self, request):
#         warriors = Warrior.objects.all()
#         serializer = WarriorSerializer(warriors, many=True)
#         return Response({"Warriors": serializer.data})
#
#
# class ProfessionCreateView(APIView):
#     def post(self, request):
#         profession = request.data.get("profession")
#         serializer = ProfessionCreateSerializer(data=profession)
#         if serializer.is_valid(raise_exception=True):
#             profession_saved = serializer.save()
#         return Response({"Success": f"Profession '{profession_saved.title}' created successfully."})
#
# # Создать эндпоинты для GET (список скиллов) и POST (создание скилла) на основе APIView
# class SkillAPIView(APIView):
#     def get(self, request):
#         skills = Skill.objects.all()
#         serializer = SkillSerializer(skills, many=True)
#         return Response({"Skills": serializer.data})
#
#     def post(self, request):
#         skill = request.data.get("skill")
#         serializer = SkillSerializer(data=skill)
#         if serializer.is_valid(raise_exception=True):
#             skill_saved = serializer.save()
#         return Response({"Success": f"Skill '{skill_saved.title}' created."})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Warrior, Skill, Profession
from .serializers import *


# 1. Список воинов (Generic)
class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


# 2. Создание профессии (Generic)
class ProfessionCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfessionCreateSerializer
    queryset = Profession.objects.all()


# 3. Список скиллов (APIView — оставляем как в задании)
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
        return Response({"Success": f"Skill '{skill_saved.title}' created."})


# 4. Практическое задание из пункта 5
# Создадим Generic-представления для вывода воинов с профессиями, скиллами, детального просмотра, удаления и обновления

# 1. Воины с профессиями
class WarriorProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorProfessionSerializer


# 2. Воины со скиллами
class WarriorSkillListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer


# 3. Детальная информация о воине по id
class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer


# 4. Удаление воина
class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


# 5. Обновление воина
class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()
