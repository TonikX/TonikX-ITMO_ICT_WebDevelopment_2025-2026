from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:race_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('list/<int:race_id>/', views.comment_list, name='comment_list'),
]