from django.urls import path 
from . import views
urlpatterns = [
    path('owner/<int:owner_id>', views.owner),
    path('owner/list/', views.get_owners),
    path('car/list/', views.CarList.as_view()),
    path('car/<int:pk>/', views.CarRetrieveView.as_view()),
    path('owner/create/', views.create_view),
    path('car/create/', views.CarCreateView.as_view()),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view()),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view()),
]