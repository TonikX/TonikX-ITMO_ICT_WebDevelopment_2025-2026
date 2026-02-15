from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

import school.views as school_views  # ← вот так

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',  auth_views.LoginView.as_view(),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', school_views.signup, name='signup'),
    path('', school_views.HomeworkListView.as_view(), name='homework_list'),
    path('homeworks/<int:pk>/', school_views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('homeworks/<int:homework_id>/submit/', school_views.SubmissionCreateView.as_view(), name='submission_create'),
    path('submission/<int:pk>/edit/',   school_views.SubmissionUpdateView.as_view(), name='submission_update'),
    path('submission/<int:pk>/delete/', school_views.SubmissionDeleteView.as_view(), name='submission_delete'),
    path('homeworks/<int:homework_id>/review/', school_views.add_review, name='review_add'),
    path('grades/', school_views.GradesListView.as_view(), name='grades'),
    # path('homeworks/create/', school_views.HomeworkCreateView.as_view(), name='homework_create'),
    path('homeworks/<int:pk>/edit/', school_views.HomeworkUpdateView.as_view(), name='homework_edit'),
    path('homeworks/<int:homework_id>/manage/', school_views.SubmissionsManageView.as_view(), name='manage_submissions'),
    path('submission/<int:pk>/score/', school_views.update_score, name='submission_score'),
]
