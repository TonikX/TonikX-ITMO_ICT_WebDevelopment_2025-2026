#!/usr/bin/env python
"""
Скрипт для создания тестовых данных
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_owners_project.settings')
django.setup()

from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior


def create_test_data():
    """Создание тестовых данных"""
    
    # Создаем профессии
    professions = [
        {"title": "Программист", "description": "Разработка программного обеспечения"},
        {"title": "Веб-разработчик", "description": "Создание веб-приложений"},
        {"title": "Мобильный разработчик", "description": "Разработка мобильных приложений"},
        {"title": "DevOps инженер", "description": "Автоматизация процессов разработки"},
        {"title": "Data Scientist", "description": "Анализ данных и машинное обучение"},
    ]
    
    created_professions = []
    for prof_data in professions:
        profession, created = Profession.objects.get_or_create(
            title=prof_data["title"],
            defaults={"description": prof_data["description"]}
        )
        created_professions.append(profession)
        print(f"Профессия создана: {profession.title}")
    
    # Создаем навыки
    skills_data = [
        "Python", "Django", "JavaScript", "React", "Vue.js", "Node.js",
        "SQL", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
        "Git", "Linux", "AWS", "Machine Learning", "TensorFlow", "PyTorch"
    ]
    
    created_skills = []
    for skill_title in skills_data:
        skill, created = Skill.objects.get_or_create(title=skill_title)
        created_skills.append(skill)
        print(f"Навык создан: {skill.title}")
    
    # Создаем воинов
    warriors_data = [
        {"name": "Иван Петров", "race": "s", "level": 3, "profession": 0},
        {"name": "Мария Сидорова", "race": "d", "level": 7, "profession": 1},
        {"name": "Алексей Козлов", "race": "t", "level": 10, "profession": 2},
        {"name": "Елена Волкова", "race": "d", "level": 5, "profession": 3},
        {"name": "Дмитрий Соколов", "race": "s", "level": 2, "profession": 4},
    ]
    
    created_warriors = []
    for warrior_data in warriors_data:
        warrior, created = Warrior.objects.get_or_create(
            name=warrior_data["name"],
            defaults={
                "race": warrior_data["race"],
                "level": warrior_data["level"],
                "profession": created_professions[warrior_data["profession"]]
            }
        )
        created_warriors.append(warrior)
        print(f"Воин создан: {warrior.name}")
    
    # Создаем связи между воинами и навыками
    warrior_skills = [
        # Иван Петров
        (0, 0, 2),  # Python, уровень 2
        (0, 1, 1),  # Django, уровень 1
        (0, 2, 3),  # JavaScript, уровень 3
        # Мария Сидорова
        (1, 0, 5),  # Python, уровень 5
        (1, 1, 4),  # Django, уровень 4
        (1, 3, 3),  # React, уровень 3
        (1, 6, 2),  # SQL, уровень 2
        # Алексей Козлов
        (2, 0, 8),  # Python, уровень 8
        (2, 1, 7),  # Django, уровень 7
        (2, 2, 6),  # JavaScript, уровень 6
        (2, 3, 5),  # React, уровень 5
        (2, 10, 4), # Docker, уровень 4
        (2, 11, 3), # Kubernetes, уровень 3
        # Елена Волкова
        (3, 0, 4),  # Python, уровень 4
        (3, 10, 5), # Docker, уровень 5
        (3, 11, 4), # Kubernetes, уровень 4
        (3, 13, 3), # Linux, уровень 3
        # Дмитрий Соколов
        (4, 0, 1),  # Python, уровень 1
        (4, 15, 2), # Machine Learning, уровень 2
        (4, 16, 1), # TensorFlow, уровень 1
    ]
    
    for warrior_idx, skill_idx, level in warrior_skills:
        warrior = created_warriors[warrior_idx]
        skill = created_skills[skill_idx]
        
        skill_of_warrior, created = SkillOfWarrior.objects.get_or_create(
            warrior=warrior,
            skill=skill,
            defaults={"level": level}
        )
        if created:
            print(f"Навык {skill.title} добавлен воину {warrior.name} с уровнем {level}")
    
    print("\nТестовые данные успешно созданы!")
    print(f"Создано профессий: {len(created_professions)}")
    print(f"Создано навыков: {len(created_skills)}")
    print(f"Создано воинов: {len(created_warriors)}")


if __name__ == "__main__":
    create_test_data()
