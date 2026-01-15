from django.contrib import admin
from .models import Conference, Participation, Review

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'talk_title', 'is_recommended')
    list_filter = ('conference', 'is_recommended')
    list_editable = ('is_recommended',) # Можно менять галочку прямо в списке

admin.site.register(Conference)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Review)