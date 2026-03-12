from django.contrib import admin
from .models import Hall, Book, Reader, BookIssue


admin.site.register(Hall)
admin.site.register(Book)
admin.site.register(Reader)
admin.site.register(BookIssue)