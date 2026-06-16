# URL маршруты Homework Board

## Основные маршруты

```python
urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment_list'),
    path('create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment_update'),
    path('<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
]
```

## Включение в главный urls.py

```python
path('assignments/', include('assignments.urls')),
```