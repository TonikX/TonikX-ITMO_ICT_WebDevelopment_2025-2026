from django.urls import path, include
from .views import RaceListView, RaceDetailView, RegisterToRaceView, add_comment
from .views import RegistrationUpdateView, RegistrationDeleteView, SignUpView

urlpatterns = [
    path('', RaceListView.as_view(), name='race_list'),
    path('race/<int:pk>/', RaceDetailView.as_view(), name='race_detail'),
    path('race/<int:pk>/register/', RegisterToRaceView.as_view(), name='register_race'),
    path('race/<int:pk>/comment/', add_comment, name='add_comment'),
    path('registration/<int:pk>/update/', RegistrationUpdateView.as_view(), name='update_reg'),
    path('registration/<int:pk>/delete/', RegistrationDeleteView.as_view(), name='delete_reg'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]