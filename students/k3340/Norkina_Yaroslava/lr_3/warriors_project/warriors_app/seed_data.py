from .models import Profession, Skill, Warrior, SkillOfWarrior
from datetime import datetime

def create_initial_data():
    # Создаем профессии
    prof1 = Profession.objects.create(
        title="Разработчик",
        description="Специалист по написанию кода"
    )
    prof2 = Profession.objects.create(
        title="Дизайнер",
        description="Специалист по созданию интерфейсов"
    )
    prof3 = Profession.objects.create(
        title="Менеджер",
        description="Руководитель проектов"
    )
    
    # Создаем умения
    skill1 = Skill.objects.create(title="Python")
    skill2 = Skill.objects.create(title="JavaScript")
    skill3 = Skill.objects.create(title="SQL")
    skill4 = Skill.objects.create(title="React")
    skill5 = Skill.objects.create(title="Django")
    
    # Создаем воинов
    warrior1 = Warrior.objects.create(
        name="Иван Иванов",
        race='d',
        level=5,
        profession=prof1
    )
    
    warrior2 = Warrior.objects.create(
        name="Петр Петров",
        race='s',
        level=3,
        profession=prof2
    )
    
    warrior3 = Warrior.objects.create(
        name="Анна Смирнова",
        race='t',
        level=8,
        profession=prof3
    )
    
    # Создаем связи умений с воинами
    SkillOfWarrior.objects.create(warrior=warrior1, skill=skill1, level=5)
    SkillOfWarrior.objects.create(warrior=warrior1, skill=skill3, level=4)
    SkillOfWarrior.objects.create(warrior=warrior1, skill=skill5, level=5)
    
    SkillOfWarrior.objects.create(warrior=warrior2, skill=skill2, level=4)
    SkillOfWarrior.objects.create(warrior=warrior2, skill=skill4, level=3)
    
    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill1, level=3)
    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill2, level=4)
    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill3, level=5)
    
    print("Тестовые данные созданы успешно!")

if __name__ == "__main__":
    create_initial_data()