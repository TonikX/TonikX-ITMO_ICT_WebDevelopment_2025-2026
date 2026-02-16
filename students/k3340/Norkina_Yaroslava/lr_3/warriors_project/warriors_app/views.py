from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView,
    DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer, ProfessionSerializer, SkillSerializer,
    WarriorProfessionSerializer, WarriorSkillsSerializer,
    WarriorFullSerializer, ProfessionCreateSerializer,
    SkillCreateSerializer, SkillOfWarriorCreateSerializer,
    WarriorCreateSerializer
)


# Ендпоинты для добавления и просмотра скилов через APIView
# класс APIView служит каркасом для контроллера


class SkillAPIView(APIView):

    # почему не используется???
    def get(self, request):
        skills = Skill.objects.all() # Подготовить набор записей.

        # Создать экземпляр сериалайзера, который может обрабатывать не отдельную запись, а их набор (many=True).
        serializer = SkillSerializer(skills, many=True) 

        # Отрендерить в json-формат данные, полученные от сериалайзера.
        # Работа рендера описана под внутри класса-родителя APIView
        return Response({"Skills": serializer.data}) 


# простой контроллер на основе класса APIView - дописана логика метода post.    
# instance=queryset,  # Передаём набор записей

class SkillCreateView(APIView):
    # Метод: POST

    def post(self, request):
        # Получаем данные из запроса
        skill_data = request.data.get("skill")
        
        # Создаём сериализатор и проверяем данные
        serializer = SkillCreateSerializer(data=skill_data)
        
        # Если данные валидны, сохраняем
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        
        # Возвращаем успешный ответ
        return Response({
            "Success": "Skill '{}' created successfully.".format(skill_saved.title)
        })
    
# Контроллеры для Generic сериализаторов

class WarriorListAPIView(ListAPIView):
    # Вывод всех воинов
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class WarriorProfessionListAPIView(ListAPIView):
    # Вывод воинов с профессиями
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()

class WarriorSkillsListAPIView(ListAPIView):
    # Вывод воинов с умениями
    serializer_class = WarriorSkillsSerializer
    queryset = Warrior.objects.all()

class WarriorDetailAPIView(RetrieveAPIView):
    # Вывод воинов с профессией и умениями
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'pk'

class WarriorDeleteAPIView(DestroyAPIView):
    # Удаление война по id
    queryset = Warrior.objects.all()
    lookup_field = 'pk'

class WarriorUpdateAPIView(UpdateAPIView):
    # Редактирование война по id
    serializer_class = WarriorCreateSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'pk'


