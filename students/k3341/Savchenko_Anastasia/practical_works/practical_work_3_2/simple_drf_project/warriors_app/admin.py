from django.contrib import admin
from .models import *

class SkillOfWarriorInline(admin.TabularInline):
    model = SkillOfWarrior
    extra = 1  # сколько пустых полей показывать для добавления

class WarriorAdmin(admin.ModelAdmin):
    inlines = [SkillOfWarriorInline]
    list_display = ('name', 'race', 'level', 'profession')
    list_filter = ('race', 'profession')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('title',)

class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

class SkillOfWarriorAdmin(admin.ModelAdmin):
    list_display = ('warrior', 'skill', 'level')

admin.site.register(Warrior, WarriorAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillOfWarrior, SkillOfWarriorAdmin)