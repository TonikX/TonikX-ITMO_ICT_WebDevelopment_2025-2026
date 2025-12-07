from rest_framework import serializers
from .models import Warrior, Profession, Skill

# --- Базовые сериализаторы ---
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

# --- Сериализатор для создания/обновления (плоский) ---
class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

# --- Сериализаторы для GET-запросов (Вложенные) ---

# Задание: Вывод полной информации о всех воинах и их профессиях [cite: 230]
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]

# Задание: Вывод полной информации о всех воинах и их скилах [cite: 231]
class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skill"]

# Задание: Вывод полной информации о войне (по id), его профессиях и скилах [cite: 232]
class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"