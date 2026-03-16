from django.urls import path
from .views import (
	SkillAPIView, WarriorListWithProfessionAPIView, 
	WarriorListWithSkillsAPIView, WarriorDetailAPIView,
	WarriorDestroyAPIView, WarriorUpdateAPIView
)

app_name = 'lab32'

urlpatterns = [
	path('skills/', SkillAPIView.as_view(), name='skills'),
	path('warriors/profession/', WarriorListWithProfessionAPIView.as_view(), name='warriors-profession'),
	path('warriors/skills/', WarriorListWithSkillsAPIView.as_view(), name='warriors-skills'),
	path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
	path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view(), name='warrior-destroy'),
	path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
