#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warriors_project.settings")
django.setup()

from warriors_app.models import Profession, Skill, Warrior, SkillOfWarrior


def populate():
    # Очищаем старые данные
    SkillOfWarrior.objects.all().delete()
    Warrior.objects.all().delete()
    Skill.objects.all().delete()
    Profession.objects.all().delete()

    # Создаём профессии
    professions = [
        Profession.objects.create(
            title="Backend Developer",
            description="Разрабатывает серверную часть приложений",
        ),
        Profession.objects.create(
            title="Frontend Developer",
            description="Создаёт пользовательские интерфейсы",
        ),
        Profession.objects.create(
            title="DevOps Engineer", description="Настраивает CI/CD и инфраструктуру"
        ),
        Profession.objects.create(
            title="Data Scientist", description="Анализирует данные и строит ML модели"
        ),
    ]
    print(f"Создано профессий: {len(professions)}")

    # Создаём скиллы
    skills = [
        Skill.objects.create(title="Python"),
        Skill.objects.create(title="JavaScript"),
        Skill.objects.create(title="Docker"),
        Skill.objects.create(title="SQL"),
        Skill.objects.create(title="Git"),
        Skill.objects.create(title="Linux"),
        Skill.objects.create(title="REST API"),
        Skill.objects.create(title="React"),
    ]
    print(f"Создано скиллов: {len(skills)}")

    # Создаём воинов
    warriors_data = [
        {"name": "Артём", "race": "s", "level": 5, "profession": professions[0]},
        {"name": "Максим", "race": "d", "level": 42, "profession": professions[0]},
        {"name": "Анна", "race": "d", "level": 35, "profession": professions[1]},
        {"name": "Иван", "race": "t", "level": 99, "profession": professions[2]},
        {"name": "Мария", "race": "s", "level": 12, "profession": professions[3]},
        {"name": "Дмитрий", "race": "d", "level": 50, "profession": professions[1]},
    ]

    warriors = []
    for data in warriors_data:
        warrior = Warrior.objects.create(**data)
        warriors.append(warrior)
    print(f"Создано воинов: {len(warriors)}")

    # Назначаем скиллы воинам
    skill_assignments = [
        # Артём (студент backend)
        (warriors[0], skills[0], 3),  # Python
        (warriors[0], skills[3], 2),  # SQL
        (warriors[0], skills[4], 2),  # Git
        # Максим (developer backend)
        (warriors[1], skills[0], 8),  # Python
        (warriors[1], skills[3], 7),  # SQL
        (warriors[1], skills[4], 6),  # Git
        (warriors[1], skills[6], 8),  # REST API
        (warriors[1], skills[2], 5),  # Docker
        # Анна (developer frontend)
        (warriors[2], skills[1], 9),  # JavaScript
        (warriors[2], skills[7], 8),  # React
        (warriors[2], skills[4], 5),  # Git
        # Иван (teamlead devops)
        (warriors[3], skills[2], 10),  # Docker
        (warriors[3], skills[5], 10),  # Linux
        (warriors[3], skills[4], 9),  # Git
        (warriors[3], skills[0], 7),  # Python
        # Мария (студент data science)
        (warriors[4], skills[0], 4),  # Python
        (warriors[4], skills[3], 3),  # SQL
        # Дмитрий (developer frontend)
        (warriors[5], skills[1], 8),  # JavaScript
        (warriors[5], skills[7], 7),  # React
        (warriors[5], skills[4], 6),  # Git
        (warriors[5], skills[6], 5),  # REST API
    ]

    for warrior, skill, level in skill_assignments:
        SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=level)
    print(f"Назначено скиллов: {len(skill_assignments)}")

    print("\nГотово! База данных заполнена тестовыми данными.")


if __name__ == "__main__":
    populate()
