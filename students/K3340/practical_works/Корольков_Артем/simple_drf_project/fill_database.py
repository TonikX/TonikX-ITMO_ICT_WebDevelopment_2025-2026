import os
import django
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warriors_project.settings')
django.setup()

from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior


def fill_database():
    print("Starting to fill database...")

    # Очищаем существующие данные
    Warrior.objects.all().delete()
    Profession.objects.all().delete()
    Skill.objects.all().delete()
    SkillOfWarrior.objects.all().delete()

    # Создаем профессии
    professions = {
        'dev': Profession.objects.create(title='Разработчик', description='Создает программное обеспечение'),
        'design': Profession.objects.create(title='Дизайнер', description='Создает интерфейсы и графику'),
        'test': Profession.objects.create(title='Тестировщик', description='Тестирует программное обеспечение'),
        'analyst': Profession.objects.create(title='Аналитик', description='Анализирует требования и процессы'),
        'manager': Profession.objects.create(title='Менеджер', description='Управляет проектами и командами'),
    }

    # Создаем навыки
    skills = {
        'programming': Skill.objects.create(title='Программирование'),
        'design': Skill.objects.create(title='Дизайн'),
        'testing': Skill.objects.create(title='Тестирование'),
        'analytics': Skill.objects.create(title='Аналитика'),
        'communication': Skill.objects.create(title='Коммуникация'),
        'leadership': Skill.objects.create(title='Лидерство'),
        'problem_solving': Skill.objects.create(title='Решение проблем'),
        'critical_thinking': Skill.objects.create(title='Критическое мышление'),
    }

    # Создаем воинов
    warriors = [
        Warrior.objects.create(name='Иван Программист', race='d', level=10, profession=professions['dev']),
        Warrior.objects.create(name='Петр Дизайнер', race='d', level=8, profession=professions['design']),
        Warrior.objects.create(name='Мария Тестировщик', race='s', level=9, profession=professions['test']),
        Warrior.objects.create(name='Алексей Аналитик', race='t', level=12, profession=professions['analyst']),
        Warrior.objects.create(name='Ольга Менеджер', race='t', level=11, profession=professions['manager']),
    ]

    # Связываем воинов с навыками
    SkillOfWarrior.objects.create(warrior=warriors[0], skill=skills['programming'], level=8)
    SkillOfWarrior.objects.create(warrior=warriors[0], skill=skills['problem_solving'], level=7)
    SkillOfWarrior.objects.create(warrior=warriors[0], skill=skills['critical_thinking'], level=6)

    SkillOfWarrior.objects.create(warrior=warriors[1], skill=skills['design'], level=9)
    SkillOfWarrior.objects.create(warrior=warriors[1], skill=skills['communication'], level=7)
    SkillOfWarrior.objects.create(warrior=warriors[1], skill=skills['critical_thinking'], level=6)

    SkillOfWarrior.objects.create(warrior=warriors[2], skill=skills['testing'], level=8)
    SkillOfWarrior.objects.create(warrior=warriors[2], skill=skills['analytics'], level=7)
    SkillOfWarrior.objects.create(warrior=warriors[2], skill=skills['communication'], level=6)

    SkillOfWarrior.objects.create(warrior=warriors[3], skill=skills['analytics'], level=9)
    SkillOfWarrior.objects.create(warrior=warriors[3], skill=skills['communication'], level=8)
    SkillOfWarrior.objects.create(warrior=warriors[3], skill=skills['critical_thinking'], level=7)

    SkillOfWarrior.objects.create(warrior=warriors[4], skill=skills['leadership'], level=9)
    SkillOfWarrior.objects.create(warrior=warriors[4], skill=skills['communication'], level=8)
    SkillOfWarrior.objects.create(warrior=warriors[4], skill=skills['problem_solving'], level=7)

    print("Database filled successfully!")
    print(f"Created: {Profession.objects.count()} professions")
    print(f"Created: {Skill.objects.count()} skills")
    print(f"Created: {Warrior.objects.count()} warriors")
    print(f"Created: {SkillOfWarrior.objects.count()} skill assignments")


if __name__ == '__main__':
    fill_database()