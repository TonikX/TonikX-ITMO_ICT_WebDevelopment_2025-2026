from django.contrib import admin
from .models import Warrior, Profession, Skill, SkillOfWarrior

# Регистрируем модели для отображения в админке
@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    list_display = ['name', 'race', 'level', 'profession']
    list_filter = ['race', 'profession']

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(SkillOfWarrior)
class SkillOfWarriorAdmin(admin.ModelAdmin):
    list_display = ['warrior', 'skill', 'level']
