import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_drf_project.settings')
django.setup()

from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior

if __name__ == "__main__":
    SkillOfWarrior.objects.all().delete()
    Warrior.objects.all().delete()
    Skill.objects.all().delete()
    Profession.objects.all().delete()

    # Профессии
    prof1 = Profession.objects.create(title="Рыцарь", description="Тяжелый воин в доспехах")
    prof2 = Profession.objects.create(title="Лучник", description="Мастер дальнего боя")
    prof3 = Profession.objects.create(title="Маг", description="Владеет магией")
    prof4 = Profession.objects.create(title="Вор", description="Мастер скрытности")
    prof5 = Profession.objects.create(title="Паладин", description="Святой воин")

    # Умения
    skill1 = Skill.objects.create(title="Меч")
    skill2 = Skill.objects.create(title="Лук")
    skill3 = Skill.objects.create(title="Огненный шар")
    skill4 = Skill.objects.create(title="Скрытность")
    skill5 = Skill.objects.create(title="Лечение")

    # Воины
    warrior1 = Warrior.objects.create(name="Артур", race="s", level=15, profession=prof1)
    warrior2 = Warrior.objects.create(name="Леголас", race="d", level=12, profession=prof2)
    warrior3 = Warrior.objects.create(name="Гэндальф", race="t", level=25, profession=prof3)
    warrior4 = Warrior.objects.create(name="Бильбо", race="s", level=8, profession=prof4)
    warrior5 = Warrior.objects.create(name="Анна", race="d", level=18, profession=prof5)

    # Добавляем умения воинам
    SkillOfWarrior.objects.create(warrior=warrior1, skill=skill1, level=8)
    SkillOfWarrior.objects.create(warrior=warrior1, skill=skill3, level=5)

    SkillOfWarrior.objects.create(warrior=warrior2, skill=skill2, level=9)
    SkillOfWarrior.objects.create(warrior=warrior2, skill=skill4, level=7)

    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill3, level=10)
    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill5, level=8)
    SkillOfWarrior.objects.create(warrior=warrior3, skill=skill1, level=6)

    SkillOfWarrior.objects.create(warrior=warrior4, skill=skill4, level=8)
    SkillOfWarrior.objects.create(warrior=warrior4, skill=skill1, level=5)

    SkillOfWarrior.objects.create(warrior=warrior5, skill=skill5, level=9)
    SkillOfWarrior.objects.create(warrior=warrior5, skill=skill1, level=6)
    SkillOfWarrior.objects.create(warrior=warrior5, skill=skill4, level=5)