from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('race', 'author', 'comment_type', 'rating', 'created_at')
    list_filter = ('comment_type', 'rating', 'created_at')
    search_fields = ('author__username', 'race__name', 'text')