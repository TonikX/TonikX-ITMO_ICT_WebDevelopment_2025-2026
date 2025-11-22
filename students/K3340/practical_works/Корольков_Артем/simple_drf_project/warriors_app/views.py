from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Warrior, Profession, Skill
from rest_framework import generics
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer
from .serializers import WarriorProfessionSerializer, WarriorSkillSerializer, WarriorFullSerializer

# Вывод всех воинов с их профессиями
class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()

# Вывод всех воинов с их навыками
class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all()

# Вывод полной информации о воине по ID
class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()

# Удаление воина по ID
class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()

# Редактирование информации о воине
class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()

class HomeAPIView(APIView):
    """
    Главная страница API - показывает доступные эндпоинты
    """

    def get(self, request):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Warriors API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; margin-right: 10px; }
                .get { background: #61affe; }
                .post { background: #49cc90; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .post-info { color: #666; font-style: italic; }
            </style>
        </head>
        <body>
            <h1>Warriors API</h1>
            <p>Добро пожаловать в API для управления воинами, профессиями и навыками!</p>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong><a href="/warriors/">/warriors/</a></strong>
                <p>Просмотр всех воинов</p>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong><a href="/skills/">/skills/</a></strong>
                <p>Просмотр всех навыков</p>
                <p class="post-info">Для создания навыка перейдите по ссылке и используйте форму внизу страницы</p>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong><a href="/profession/create/">/profession/create/</a></strong>
                <p>Создание новой профессии</p>
                <p class="post-info">Для создания профессии перейдите по ссылке и используйте форму внизу страницы</p>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong><a href="/admin/">/admin/</a></strong>
                <p>Админ-панель Django</p>
            </div>

            <hr>
            <p><strong>Практическое задание 3.2 выполнено!</strong></p>
            <p>Эндпоинты для навыков (GET и POST) готовы к использованию.</p>
            
        

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
    <h2 style="color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px;">Ссылки для тестирования API</h2>
    
    <div style="margin: 20px 0;">
        <h3 style="color: #495057;">Главная страница и базовые эндпоинты</h3>
        <div class="endpoint">
            <strong><a href="/">Главная страница API</a></strong><br>
            <strong><a href="/admin/">Админ-панель Django</a></strong>
        </div>
    </div>

    <div style="margin: 20px 0;">
        <h3 style="color: #495057;">Эндпоинты для воинов (Warriors)</h3>
        
        <h4 style="color: #6c757d; margin-left: 20px;">GET запросы (просмотр данных):</h4>
        <div class="endpoint" style="margin-left: 40px;">
            <strong><a href="/warriors/">Все воины</a></strong><br>
            <strong><a href="/warriors/professions/">Все воины с профессиями</a></strong><br>
            <strong><a href="/warriors/skills/">Все воины с навыками</a></strong><br>
            <strong><a href="/warriors/1/">Конкретный воин (ID=1)</a></strong><br>
            <strong><a href="/warriors/2/">Конкретный воин (ID=2)</a></strong><br>
            <strong><a href="/warriors/3/">Конкретный воин (ID=3)</a></strong>
        </div>

        <h4 style="color: #6c757d; margin-left: 20px;">DELETE запросы (удаление):</h4>
        <div class="endpoint" style="margin-left: 40px;">
            <strong><a href="/warriors/1/delete/">Удалить воина ID=1</a></strong><br>
            <strong><a href="/warriors/2/delete/">Удалить воина ID=2</a></strong>
            <p style="color: #666; font-style: italic; margin: 5px 0;">
                DELETE запросы нужно отправлять через curl или Postman
            </p>
        </div>

        <h4 style="color: #6c757d; margin-left: 20px;">PUT/PATCH запросы (обновление):</h4>
        <div class="endpoint" style="margin-left: 40px;">
            <strong><a href="/warriors/1/update/">Обновить воина ID=1</a></strong><br>
            <strong><a href="/warriors/2/update/">Обновить воина ID=2</a></strong>
            <p style="color: #666; font-style: italic; margin: 5px 0;">
                Используйте форму внизу страницы для отправки PUT/PATCH запроса
            </p>
        </div>
    </div>

    <div style="margin: 20px 0;">
        <h3 style="color: #495057;">Эндпоинты для навыков (Skills)</h3>
        <div class="endpoint">
            <strong><a href="/skills/">Все навыки (GET)</a></strong><br>
            <strong><a href="/skills/">Создать навык (POST)</a></strong>
            <p style="color: #666; font-style: italic; margin: 5px 0;">
                Для создания навыка перейдите по ссылке и используйте форму внизу страницы
            </p>
        </div>
    </div>

    <div style="margin: 20px 0;">
        <h3 style="color: #495057;">Эндпоинты для профессий (Professions)</h3>
        <div class="endpoint">
            <strong><a href="/profession/create/">Создать профессию (GET)</a></strong>
            <p style="color: #666; font-style: italic; margin: 5px 0;">
                Для создания профессии перейдите по ссылке и используйте форму внизу страницы
            </p>
        </div>
    </div>

    <div style="background: #e9ecef; padding: 15px; border-radius: 5px; margin-top: 20px;">
        <h4 style="color: #495057; margin-top: 0;">Как тестировать:</h4>
        <ul style="color: #666; margin-bottom: 0;">
            <li><strong>GET запросы</strong> - просто перейдите по ссылке</li>
            <li><strong>POST запросы</strong> - перейдите по ссылке и используйте форму внизу страницы</li>
            <li><strong>PUT/PATCH запросы</strong> - перейдите по ссылке и используйте форму внизу страницы</li>
            <li><strong>DELETE запросы</strong> - используйте curl: <code>curl -X DELETE http://127.0.0.1:8000/warriors/1/delete/</code></li>
        </ul>
    </div>
</div>
            
        </body>
        </html>
        """
        return HttpResponse(html_content)

class WarriorAPIView(APIView):
    """
    APIView для работы с воинами
    Обрабатывает GET запросы для получения списка воинов
    """

    def get(self, request):
        # Получаем всех воинов из базы данных
        warriors = Warrior.objects.all()

        # Сериализуем данные (many=True для списка объектов)
        serializer = WarriorSerializer(warriors, many=True)

        # Возвращаем JSON ответ
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    """
    APIView для создания профессий
    Обрабатывает POST запросы
    """

    def post(self, request):
        # Получаем данные из тела запроса
        profession_data = request.data.get("profession")

        # Создаем сериализатор с полученными данными
        serializer = ProfessionCreateSerializer(data=profession_data)

        # Проверяем валидность данных
        if serializer.is_valid(raise_exception=True):
            # Сохраняем новый объект в базу данных
            profession_saved = serializer.save()

            # Возвращаем успешный ответ
            return Response({"Success": "Profession '{}' created successfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    """
    APIView для работы с навыками (Skill)
    Обрабатывает GET и POST запросы
    """

    def get(self, request):
        """
        Обработчик GET запроса - возвращает список всех навыков
        """
        # Получаем все объекты Skill из базы данных
        skills = Skill.objects.all()

        # Сериализуем данные в JSON
        serializer = SkillSerializer(skills, many=True)

        # Возвращаем JSON ответ
        return Response({"Skills": serializer.data})

    def post(self, request):
        """
        Обработчик POST запроса - создает новый навык
        """
        # Получаем данные из тела запроса
        skill_data = request.data.get("skill")

        # Создаем сериализатор с полученными данными
        serializer = SkillSerializer(data=skill_data)

        # Проверяем валидность данных
        if serializer.is_valid(raise_exception=True):
            # Сохраняем новый объект в базу данных
            skill_saved = serializer.save()

            # Возвращаем успешный ответ со статусом 201 Created
            return Response(
                {"Success": "Skill '{}' created successfully.".format(skill_saved.title)},
                status=status.HTTP_201_CREATED
            )
