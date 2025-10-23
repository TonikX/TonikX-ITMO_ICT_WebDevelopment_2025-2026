from django.urls import path
from .views import (
    HomeworkListView, HomeworkDetailView, SubmitHomeworkView, gradebook_view,
    HomeworkCreateView, SubjectCreateView
)

urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework_list'),
    path('homework/new/', HomeworkCreateView.as_view(), name='homework_create'),
    path('subject/new/', SubjectCreateView.as_view(), name='subject_create'),
    path('homework/<int:pk>/', HomeworkDetailView.as_view(), name='homework_detail'),
    path('homework/<int:pk>/submit/', SubmitHomeworkView.as_view(), name='homework_submit'),
    path('gradebook/', gradebook_view, name='gradebook'),
]
