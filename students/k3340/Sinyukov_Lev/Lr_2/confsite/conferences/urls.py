from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConferenceListView.as_view(), name='conf_list'),
    path('conference/<int:pk>/', views.ConferenceDetailView.as_view(), name='conf_detail'),

    # таблица участников по конференциям
    path('participants/', views.ParticipantsTableView.as_view(), name='participants'),

    # регистрация на выступление
    path('conference/<int:conf_id>/register/', views.RegistrationCreateView.as_view(), name='reg_create'),
    path('registration/<int:pk>/edit/', views.RegistrationUpdateView.as_view(), name='reg_update'),
    path('registration/<int:pk>/delete/', views.RegistrationDeleteView.as_view(), name='reg_delete'),

    # отзывы
    path('conference/<int:conf_id>/review/add/', views.ReviewCreateView.as_view(), name='review_create'),
]