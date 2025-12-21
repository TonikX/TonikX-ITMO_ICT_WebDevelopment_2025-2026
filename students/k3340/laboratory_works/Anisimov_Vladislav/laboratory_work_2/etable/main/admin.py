from django.contrib import admin
from .models import *
from accounts.models import *

#admin.site.register(Class)
#admin.site.register(Subject)
#admin.site.register(Assignment)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == "admin":
            return qs
        #if request.user.user_type == "teacher":  
        return qs

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name","teacher","classname",]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == "admin":
            return qs
        #if request.user.user_type == "teacher":  
        return qs.filter(teacher=request.user)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["subject","text","penalty_info","date_of_issue","end_date"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == "admin":
            return qs
        #if request.user.user_type == "teacher":
        subjects = Subject.objects.filter(teacher=request.user)
        return qs.filter(subject__in=subjects)
    
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ["assignment","student","grade","link_to_file",]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == "admin":
            return qs
        #if request.user.user_type == "teacher":
        subjects = Subject.objects.filter(teacher=request.user)
        assignments = Assignment.objects.filter(subject__in=subjects)
        return qs.filter(assignment__in=assignments)