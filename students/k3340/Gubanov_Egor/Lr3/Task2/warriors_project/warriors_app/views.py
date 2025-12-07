from rest_framework import generics
from .models import Warrior
from .serializers import (
    WarriorSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorDetailSerializer
)

# 1. Вывод воинов с профессиями [cite: 230]
# Используем ListAPIView (только чтение списка) [cite: 192]
class WarriorListProfessionView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorProfessionSerializer

# 2. Вывод воинов со скиллами [cite: 231]
class WarriorListSkillView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer

# 3, 4, 5. Просмотр, Удаление, Редактирование воина по ID [cite: 232, 233, 234]
# Используем RetrieveUpdateDestroyAPIView — это "комбайн" 3 в 1 [cite: 219]
class WarriorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.all()

    # Переопределяем метод выбора сериализатора
    def get_serializer_class(self):
        # Если мы просто смотрим (GET) — показываем полную структуру (с вложенностью)
        if self.request.method == 'GET':
            return WarriorDetailSerializer
        # Если редактируем или удаляем — используем обычный плоский сериализатор
        return WarriorSerializer