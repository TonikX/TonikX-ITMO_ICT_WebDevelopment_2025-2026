from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, HomeworkListView, HomeworkDetailView, GradebookView

urlpatterns = [
    path('', HomeworkListView.as_view(), name='home'),
    path('homework/<int:pk>/', HomeworkDetailView.as_view(), name='homework_detail'),
    path('gradebook/', GradebookView.as_view(), name='gradebook'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]