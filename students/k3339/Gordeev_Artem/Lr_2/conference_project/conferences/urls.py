from django.urls import path

from .views import SignUpView, ConferenceListView, ConferenceDetailView

urlpatterns = [
    # Страницы аутентификации
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    # Страницы конференций
    path('', ConferenceListView.as_view(), name='conference_list'),
    path('conference/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
]
