from django.urls import path
from .views import (ConferencesListView, 
                    ConferenceDetailView, 
                    RegisterPresentationView,
                    CancelPresentationView,
                    EditPresentationView,
                    ReviewsListView,
                    AddReviewView,
                    PresentationsListView,
                    AddConferenceView,
                    EditConferenceView,
                    DeleteConferenceView)


'''
# Примечание:

Параметр `pk` в conference_detail используется в
`reverse_lazy('conference_detail', kwargs={'pk': self.kwargs['conference_id']})`
в CancelPresentationView (и, возможно, других представлениях).

Изменение названия с `pk` на другое может привести к ошибкам.
'''
urlpatterns = [
     path('list/', ConferencesListView.as_view(), name='conferences_list'),
     path('add/', AddConferenceView.as_view(), name='add_conference'),
     path('<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
     path('<int:pk>/edit/', EditConferenceView.as_view(), name='edit_conference'),
     path('<int:pk>/delete/', DeleteConferenceView.as_view(), name='delete_conference'),
     path('<int:pk>/presentations/register',
          RegisterPresentationView.as_view(), 
          name='register_presentation'),
     path('<int:conference_id>/presentations/<int:presentation_id>/cancel',
          CancelPresentationView.as_view(),
          name='cancel_presentation'),
     path('<int:conference_id>/presentations/<int:presentation_id>/edit',
          EditPresentationView.as_view(),
          name='edit_presentation'),
     path('<int:conference_id>/reviews/list',
          ReviewsListView.as_view(),
          name='reviews_list'),
     path('<int:conference_id>/reviews/add',
          AddReviewView.as_view(),
          name='add_review'),
     path('<int:conference_id>/presentations/list',
          PresentationsListView.as_view(),
          name='presentations_list'),
]
