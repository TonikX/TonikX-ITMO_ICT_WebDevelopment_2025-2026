from django.contrib import admin
from .models import Warrior, Profession, Skill, SkillOfWarrior


@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "race", "level", "profession")
    list_filter = ("race", "profession")


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(SkillOfWarrior)
class SkillOfWarriorAdmin(admin.ModelAdmin):
    list_display = ("id", "warrior", "skill", "level")
