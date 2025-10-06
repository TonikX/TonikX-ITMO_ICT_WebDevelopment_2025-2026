from django.urls import path

from .views import SignUpView, ConferenceListView, ConferenceDetailView, ParticipationCreateView, \
    ParticipationUpdateView, ParticipationDeleteView, ReviewCreateView

urlpatterns = [
    # Страницы аутентификации
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    # Страницы конференций
    path('', ConferenceListView.as_view(), name='conference_list'),
    path('conference/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),

    # Регистрация на конференцию
    path('conference/<int:conf_pk>/participate/', ParticipationCreateView.as_view(), name='participate'),
    # Редактирование регистрации
    path('participation/<int:pk>/edit/', ParticipationUpdateView.as_view(), name='participation_edit'),
    # Отмена регистрации
    path('participation/<int:pk>/delete/', ParticipationDeleteView.as_view(), name='participation_delete'),
    # Добавление отзыва
    path('conference/<int:conf_pk>/review/', ReviewCreateView.as_view(), name='add_review'),
]
