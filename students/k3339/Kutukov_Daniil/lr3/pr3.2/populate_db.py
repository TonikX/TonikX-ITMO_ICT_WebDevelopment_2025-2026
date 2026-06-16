"""
Скрипт для наполнения базы данных тестовыми данными
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warriors_project.settings")
django.setup()

from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior

print("=" * 70)
print("НАПОЛНЕНИЕ БАЗЫ ДАННЫХ ТЕСТОВЫМИ ДАННЫМИ")
print("=" * 70)

# Создание профессий
print("\n1. Создание профессий:")
print("-" * 70)

backend = Profession.objects.create(
    title="Backend Developer", description="Специалист по серверной разработке"
)
print(f"Создана профессия: {backend}")

frontend = Profession.objects.create(
    title="Frontend Developer", description="Специалист по клиентской разработке"
)
print(f"Создана профессия: {frontend}")

fullstack = Profession.objects.create(
    title="Fullstack Developer", description="Универсальный разработчик"
)
print(f"Создана профессия: {fullstack}")

devops = Profession.objects.create(
    title="DevOps Engineer", description="Специалист по развертыванию и автоматизации"
)
print(f"Создана профессия: {devops}")

# Создание умений
print("\n2. Создание умений:")
print("-" * 70)

python_skill = Skill.objects.create(title="Python programming")
print(f"Создано умение: {python_skill}")

java_skill = Skill.objects.create(title="Java programming")
print(f"Создано умение: {java_skill}")

js_skill = Skill.objects.create(title="JavaScript programming")
print(f"Создано умение: {js_skill}")

react_skill = Skill.objects.create(title="React")
print(f"Создано умение: {react_skill}")

django_skill = Skill.objects.create(title="Django")
print(f"Создано умение: {django_skill}")

docker_skill = Skill.objects.create(title="Docker")
print(f"Создано умение: {docker_skill}")

kubernetes_skill = Skill.objects.create(title="Kubernetes")
print(f"Создано умение: {kubernetes_skill}")

sql_skill = Skill.objects.create(title="SQL")
print(f"Создано умение: {sql_skill}")

git_skill = Skill.objects.create(title="Git")
print(f"Создано умение: {git_skill}")

# Создание воинов
print("\n3. Создание воинов:")
print("-" * 70)

warrior1 = Warrior.objects.create(
    race="s", name="Николай Леонтьев", level=10, profession=backend
)
print(f"Создан воин: {warrior1}")

warrior2 = Warrior.objects.create(
    race="d", name="Дмитрий Мартынов", level=50, profession=frontend
)
print(f"Создан воин: {warrior2}")

warrior3 = Warrior.objects.create(
    race="t", name="Александр Петров", level=70, profession=fullstack
)
print(f"Создан воин: {warrior3}")

warrior4 = Warrior.objects.create(
    race="d", name="Иван Сидоров", level=45, profession=devops
)
print(f"Создан воин: {warrior4}")

warrior5 = Warrior.objects.create(
    race="s", name="Михаил Козлов", level=15, profession=backend
)
print(f"Создан воин: {warrior5}")

warrior6 = Warrior.objects.create(
    race="d", name="Сергей Новиков", level=55, profession=fullstack
)
print(f"Создан воин: {warrior6}")

# Добавление умений воинам
print("\n4. Добавление умений воинам:")
print("-" * 70)

# Николай Леонтьев - backend студент
SkillOfWarrior.objects.create(warrior=warrior1, skill=python_skill, level=5)
SkillOfWarrior.objects.create(warrior=warrior1, skill=django_skill, level=4)
SkillOfWarrior.objects.create(warrior=warrior1, skill=sql_skill, level=3)
SkillOfWarrior.objects.create(warrior=warrior1, skill=git_skill, level=6)
print(f"Добавлены умения для {warrior1}")

# Дмитрий Мартынов - frontend разработчик
SkillOfWarrior.objects.create(warrior=warrior2, skill=js_skill, level=40)
SkillOfWarrior.objects.create(warrior=warrior2, skill=react_skill, level=35)
SkillOfWarrior.objects.create(warrior=warrior2, skill=git_skill, level=30)
print(f"Добавлены умения для {warrior2}")

# Александр Петров - fullstack тимлид
SkillOfWarrior.objects.create(warrior=warrior3, skill=python_skill, level=60)
SkillOfWarrior.objects.create(warrior=warrior3, skill=js_skill, level=55)
SkillOfWarrior.objects.create(warrior=warrior3, skill=django_skill, level=50)
SkillOfWarrior.objects.create(warrior=warrior3, skill=react_skill, level=45)
SkillOfWarrior.objects.create(warrior=warrior3, skill=docker_skill, level=40)
SkillOfWarrior.objects.create(warrior=warrior3, skill=git_skill, level=65)
print(f"Добавлены умения для {warrior3}")

# Иван Сидоров - DevOps разработчик
SkillOfWarrior.objects.create(warrior=warrior4, skill=python_skill, level=35)
SkillOfWarrior.objects.create(warrior=warrior4, skill=docker_skill, level=50)
SkillOfWarrior.objects.create(warrior=warrior4, skill=kubernetes_skill, level=45)
SkillOfWarrior.objects.create(warrior=warrior4, skill=git_skill, level=40)
print(f"Добавлены умения для {warrior4}")

# Михаил Козлов - backend студент
SkillOfWarrior.objects.create(warrior=warrior5, skill=python_skill, level=8)
SkillOfWarrior.objects.create(warrior=warrior5, skill=sql_skill, level=6)
SkillOfWarrior.objects.create(warrior=warrior5, skill=git_skill, level=7)
print(f"Добавлены умения для {warrior5}")

# Сергей Новиков - fullstack разработчик
SkillOfWarrior.objects.create(warrior=warrior6, skill=python_skill, level=45)
SkillOfWarrior.objects.create(warrior=warrior6, skill=js_skill, level=50)
SkillOfWarrior.objects.create(warrior=warrior6, skill=django_skill, level=40)
SkillOfWarrior.objects.create(warrior=warrior6, skill=react_skill, level=42)
SkillOfWarrior.objects.create(warrior=warrior6, skill=sql_skill, level=38)
SkillOfWarrior.objects.create(warrior=warrior6, skill=git_skill, level=48)
print(f"Добавлены умения для {warrior6}")

# Статистика
print("\n" + "=" * 70)
print("ИТОГОВАЯ СТАТИСТИКА:")
print("=" * 70)
print(f"Создано профессий: {Profession.objects.count()}")
print(f"Создано умений: {Skill.objects.count()}")
print(f"Создано воинов: {Warrior.objects.count()}")
print(f"Создано связей воин-умение: {SkillOfWarrior.objects.count()}")

print("\n" + "=" * 70)
print("Список воинов с профессиями:")
print("=" * 70)
for warrior in Warrior.objects.select_related("profession").all():
    race_display = warrior.get_race_display()
    profession = warrior.profession.title if warrior.profession else "Без профессии"
    skills_count = warrior.warrior_skills_link.count()
    print(
        f"{warrior.name} - {race_display}, {profession}, уровень {warrior.level}, умений: {skills_count}"
    )

print("\n" + "=" * 70)
print("БАЗА ДАННЫХ УСПЕШНО НАПОЛНЕНА!")
print("=" * 70)
