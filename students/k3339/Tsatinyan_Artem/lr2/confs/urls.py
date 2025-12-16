from django.contrib import admin
from django.urls import path, include
from core.views import (
    ConferenceListView, ConferenceDetailView,
    RegistrationCreateView, RegistrationUpdateView, RegistrationDeleteView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    ParticipantsTableView, SignUpView,
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # login/logout/password

    path('signup/', SignUpView.as_view(), name='signup'),

    path('', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),

    path('conferences/<int:pk>/register/', RegistrationCreateView.as_view(), name='registration_create'),
    path('registrations/<int:pk>/edit/', RegistrationUpdateView.as_view(), name='registration_update'),
    path('registrations/<int:pk>/delete/', RegistrationDeleteView.as_view(), name='registration_delete'),

    path('conferences/<int:pk>/reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    path('participants/', ParticipantsTableView.as_view(), name='participants_table'),
]

urlpatterns += staticfiles_urlpatterns()
