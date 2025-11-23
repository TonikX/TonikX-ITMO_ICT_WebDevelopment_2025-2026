from django.contrib import admin
from .models import Warrior, Profession, Skill, SkillOfWarrior

# Простая регистрация моделей, чтобы они появились в админке
admin.site.register(Warrior)
admin.site.register(Profession)
admin.site.register(Skill)
admin.site.register(SkillOfWarrior)