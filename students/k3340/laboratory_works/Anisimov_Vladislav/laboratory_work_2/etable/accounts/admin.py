from django.contrib import admin
from .models import User

#admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["classname","user_type","username","full_name","password","is_staff"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == "admin":
            return qs
        #if request.user.user_type == "teacher":  
        return qs.filter(user_type="student")